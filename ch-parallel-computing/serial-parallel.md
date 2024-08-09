(serial-parallel)=
# Serial Execution v.s. Parallel Execution

If computing tasks are not parallelized, most of them are executed serially, as shown in {numref}`serial-timeline`. Here, the worker can be a computing core or a node in a cluster.

```{figure} ../img/ch-parallel-computing/serial-timeline.svg
---
width: 600px
name: serial-timeline
---
Timeline Illustrating Serial Execution
```

In serial execution, tasks are executed one after another, with each task depending on the completion of the previous task. This sequential execution can lead to longer overall execution time, as tasks cannot be executed concurrently.

Cluster and heterogeneous computing provide more available computing cores, and parallel programming distributes computing tasks to multiple workers, as shown in {numref}`distributed-timeline`. Whether it is multi-core on a single machine or multi-machine cluster, a scheduler is needed to distribute computing tasks to different workers. With more workers involved, the total time is reduced, and the saved time can be used for other tasks.

```{figure} ../img/ch-parallel-computing/distributed-timeline.svg
---
width: 600px
name: distributed-timeline
---
Timeline Illustrating Distributed Execution
```