(sec-ray-cluster-resource)=
# Ray Cluster

## Ray Cluster

As shown in {numref}`fig-ray-cluster`, a Ray cluster consists of a series of computing nodes, including two key types of nodes: head nodes and worker nodes. These nodes can be deployed on virtual machines, containers, or bare metal servers.

```{figure} ../img/ch-ray-cluster/ray-cluster.svg
---
width: 800px
name: fig-ray-cluster
---
A Ray cluster consists of a head node and multiple worker nodes, with some management processes running on the head node.
```

In the Ray distributed computing environment, some key processes are running on all nodes.

* Worker

Each compute node runs one or more Worker processes, which are responsible for executing computing tasks. Worker processes can be stateless, meaning they can repeatedly execute tasks corresponding to Tasks; they can also be stateful Actors, which execute methods of remote classes. By default, the number of Workers is equal to the number of CPU cores of the compute node where they are located.

* Raylet

A Raylet runs on each compute node. Each compute node may run multiple Worker processes, but there is only one Raylet process on each compute node, or Raylet is shared by multiple Worker processes. Raylet mainly consists of two components: one is the scheduler, which is responsible for resource management and task allocation; the other is the shared-memory object store, which is responsible for local data storage. The Object Store on each compute node together constitutes the distributed object storage of the Ray cluster.

We can also see from {numref}`fig-ray-cluster` that there are more things head nodes:

* Global Control Service（GCS）

GCS is the global metadata management service of the Ray cluster, responsible for storing and managing metadata information such as which Actor is assigned to which computing node. These metadata are shared by all Workers.

* Driver

Driver is the entry point for executing a program. The entry point refers to Python's `__main__` function. Usually, `__main__` should not perform large-scale calculations at runtime, but is responsible for scheduling Tasks and Actors to Workers with sufficient resources.

Ray's head node also runs some other management services, such as automatic scaling of computing resources, job submission, and other services.

## Start the Ray cluster

Previously, the `ray.init()` method was used in the Python code to start a single-machine Ray cluster locally. In reality, the Ray cluster includes the head node and the working node, which should be started separately. Start on the head node first:

```bash
ray start --head --port=6379
```

It will start a head node process on the physical node. The default port number is 6379. You can also use `--port` to specify the port number. After executing the above command, the command line will have some prompts, including the address of the current node and how to shut it down. Start the working node:

```bash
ray start --address=<head-node-address>:<port>
```

Replace `<head-node-address>:<port>` with the address of the Ray head node that you just started.

In addition, Ray also provides a cluster startup command called `ray up`, which accepts a yaml file as a parameter and defines the head node address and the working node address in the yaml file. Example of a yaml file [example.yaml](https://raw.githubusercontent.com/ray-project/ray/master/python/ray/autoscaler/local/example-full.yaml)：

```yaml
cluster_name: default

provider:
    type: local
    head_ip: YOUR_HEAD_NODE_HOSTNAME
    worker_ips: [WORKER_NODE_1_HOSTNAME, WORKER_NODE_2_HOSTNAME, ... ]
```

Use the following command, which will help us start the Ray cluster:

```
ray up example.yaml
```

You can use the `ray status` command to view the status of the started Ray cluster.

:::{note}
Ray's head node exposes three port numbers, which are 6379, 8265, and 10001 by default. When starting Ray, the port number of the Ray head node is set, which defaults to 6379. This port number is the port for communication between the head node and the working nodes. After the Ray head node is started, a Ray dashboard port number is also provided, which defaults to 8265. This port number can be used to receive jobs submitted by the Ray command line. In addition, there is a port `10001`, which defaults to `ray.init()` when connecting.
:::

The above method can deploy a Ray cluster on multiple virtual machines or physical machines. Ray also provides Kubernetes and supporting tools for automatic scaling.