(sec-ray-computing-resource)=
# Computing resources and resource groups

## Computing resources

Ray can manage computing resources, including various accelerators such as CPU, memory, and GPU. The computing resources here are logical, compared to physical computing resources. When each node of the Ray cluster starts, it will detect physical computing resources and map them to logical computing resources based on certain rules. Each node of the Ray cluster can be a virtual machine, container, or bare metal server.

* CPU: The number of physical CPUs in each node (`num_cpus`)

* GPU: The number of physical GPUs in each node (`num_gpus`)

* Memory: 70% of the available memory of each node (`memory`)

The above are the default rules. You can also manually specify these resources when starting the Ray cluster. For example, there are 64 CPU cores and 8 GPUs on a physical node. When starting the Ray worker node, we can only register a part of the computing resources.
```
ray start --num-cpus=32 --num-gpus=4
```

## Resource requirements

By default, Ray Task uses 1 logical CPU, which is used for both task scheduling and computing tasks; Ray Actor uses 1 logical CPU for task scheduling and 0 CPU for computing tasks.

When a Task or Actor is executed, Ray will schedule it to a node that can meet its resource requirements. By default, the resource requirements of Ray Task are relatively clear, while the default CPU resource requirement of Ray Actor is 0. If no additional settings are made, it will create an illusion that Ray Actor does not need computing resources, resulting in a large number of Actors being scheduled to the same computing node. In order to better control resource usage and avoid potential risks, it is recommended to specify the required number of computing resources when defining a Task or Actor. Specifically, when using `ray.remote()` to a function or class, you can specify the computing resources required by Task and Actor by passing the `num_cpus` and `num_gpus` parameters.

```
@ray.remote(num_cpus=4)
def func():
    ...

@ray.remote(num_cpus=16, num_gpus=1)
class Actor:
    pass
```

Or call `task.options()` or `actor.options()` to specify the resources required for a specific computing task, where `task` is a distributed function with `ray.remote()`, and `actor` is an instance of a distributed class with `ray.remote()`.

```
func.options(num_cpus=4).remote()
```

## Other Resources

In addition to general-purpose CPUs and GPUs, Ray also supports many other types of computing resources, such as various accelerators. You can use key-value pairs like `--resources={"special_hardware": 1}` to manage these computing resources. The usage is similar to `num_gpus` to manage GPU resources. For example, Google's TPU: `resources={"TPU": 2}` and Huawei's Ascend: `resources={"NPU": 2}`. For a cluster has both x86 and ARM CPU architectures, the ARM nodes can be defined as follows: `resources={"arm64": 1}`.

## Automatic scaling

Ray clusters can be automatically scaled, mainly for the following scenarios:

* When the Ray cluster has insufficient resources, create new worker nodes.
* When a working node is idle or cannot be started, shut down the working node.

Automatic scaling mainly satisfies the computing resource requests defined in the Task or Actor code (for example, the computing resources requested by `task.options()`), rather than automatically scaling based on the actual resource utilization of the computing nodes.

## Placement Group

Regarding the configuration of computing resources and clusters, Ray provides a feature called Placement Group, which can be understood as "resource group". Placement Group allows users to use computing resources of multiple nodes on the cluster atomically. The so-called atomic means that resources are either fully allocated to users or not allocated at all, and there will be no situation where only some resources are allocated.

Placement Group is mainly applicable to the following scenarios:

* Gang Scheduling: A job requires a group of resources that need to work together to complete the task. Either allocate or not allocate. If only some resources are allocated to this job, the entire task will not be completed. For example, in large-scale distributed training, multiple computing nodes and multiple GPUs may be required. At this time, these resources can be applied for and allocated in the Ray cluster.

* Load balancing: Jobs need to be load balanced on multiple nodes, and each node takes on a small part of the task. Placement Group can ensure that jobs are distributed to multiple computing nodes as much as possible. For example, in a distributed inference scenario, if a job requires 8 GPUs, each GPU is responsible for loading the model and performing inference independently. In order to achieve load balancing, the job should be scheduled to 8 computing nodes, with each node using 1 GPU. The advantage of this is that if a node fails, it will not cause the entire inference service to be unavailable, because other nodes can still continue to work.

There are several key concepts in Placement Group:

* Bundle: A Bundle is a key-value pair that defines the required computing resources, such as `{"CPU": 2}`, or `{"CPU": 8, "GPU": 4}`. A Bundle must be schedulable to a single computing node; for example, if a computing node has only 8 GPUs, a Bundle like `{"GPU": 10}` is unreasonable.

* Placement Group: A Placement Group is a group of Bundles. For example, `{"CPU": 8} * 4` will request 4 Bundles from the Ray cluster, with 8 CPUs reserved for each Bundle. The scheduling of multiple Bundles will follow some scheduling policies. After the Placement Group is created by the Ray cluster, it can be used to run Ray Tasks and Ray Actors.

We can use [`placement_group()`](https://docs.ray.io/en/latest/ray-core/api/doc/ray.util.placement_group.html) to create a Placement Group. `placement_group()` is asynchronous. If you need to wait for the creation to succeed, you need to call [`PlacementGroup.ready()`](https://docs.ray.io/en/latest/ray-core/api/doc/ray.util.placement_group.PlacementGroup.ready.html).

If you want a Ray Task or Ray Actor to be scheduled to a Placement Group, you can set it in `options(scheduling_strategy=PlacementGroupSchedulingStrategy(...))`.

Below is a complete example. Before running this example, a Ray cluster with multiple GPUs is created in advance. If there is no GPU, you can also change it to CPU.
```python
from ray.util.placement_group import (
    placement_group,
    placement_group_table,
    remove_placement_group,
)
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
import ray

ray.init()

print('''Available Resources: {}'''.format(ray.available_resources()))

@ray.remote(num_gpus=2)
def gpu_task():
    print("GPU ids: {}".format(ray.get_runtime_context().get_accelerator_ids()["GPU"]))

# Create Placement Group
pg = placement_group([{"CPU": 16, "GPU": 2}])

# Wait till Placement Group is created
ray.get(pg.ready(), timeout=10)
# Alternatively, we can use ray.wait
ready, unready = ray.wait([pg.ready()], timeout=10)

print('''Placement Group: {}'''.format(placement_group_table(pg)))

# Put this Ray Task into the Placement Group
ray.get(gpu_task.options(
    scheduling_strategy=PlacementGroupSchedulingStrategy(placement_group=pg)
).remote())

# Remove this Placement Group
remove_placement_group(pg)
```

The `placement_group()` method that creates a Placement Group also accepts a `strategy` parameter to set different scheduling strategies: either to concentrate these reserved resources on a few computing nodes as much as possible, or to spread these reserved resources on multiple computing nodes as much as possible. There are the following strategies:

* `STRICT_PACK`: All bundles must be scheduled to a single computing node.

* `PACK`: All bundles are scheduled to a single computing node first. If the conditions cannot be met, they are scheduled to other computing nodes, as shown in {numref}`fig-ray-pg-pack`. `PACK` is the default scheduling strategy.

* `STRICT_SPREAD`: Each bundle must be scheduled to a different computing node.

* `SPREAD`: Each bundle is scheduled to a different computing node first. If the conditions cannot be met, some bundles can share a computing node, as shown in {numref}`fig-ray-pg-spread`.

```{figure} ../img/ch-ray-cluster/pg-pack.svg
---
width: 600px
name: fig-ray-pg-pack
---
The `PACK` strategy prioritizes scheduling all bundles to a single compute node.
```

Since the calculation is scheduled to a small number of computing nodes as much as possible, the scheduling strategies of `STRICT_PACK` and `PACK` ensure the locality of data, and the computing tasks can quickly access local data.

```{figure} ../img/ch-ray-cluster/pg-spread.svg
---
width: 600px
name: fig-ray-pg-spread
---
The `SPREAD` strategy prioritizes scheduling each bundle to a different compute node.
```

The `STRICT_SPREAD` and `SPREAD` scheduling strategies make the computation more load-balanced.

:::{note}
Multiple Ray Tasks or Actors can run on the same Bundle, and any Task or Actor using the same Bundle will always run on that compute node. 
:::
