(serial-parallel)=
# Serial Execution v.s. Parallel Execution

If computing tasks are not parallelized and accelerated, most of them are executed serially, as shown in {numref}`serial-timeline`. Here, the worker can be a computing core or a node in a cluster.

```{figure} ../img/ch-intro/serial-timeline.svg
---
width: 600px
name: serial-timeline
---
Timeline Illustrating Serial Execution
```

In serial execution, tasks are executed one after another, with each task depending on the completion of the previous task. This sequential execution can lead to longer overall execution time, as tasks cannot be executed concurrently.

Cluster and heterogeneous computing provide more available computing cores, and parallel programming distributes computing tasks to multiple workers, as shown in {numref}`distributed-timeline`. Whether it is multi-core on a single machine or multi-machine clustering, a scheduler is needed to distribute computing tasks to different workers. With more workers involved, the total time for task completion is reduced, and the saved time can be used for other tasks.

集群和异构计算提供了更多可利用的计算核心，并行计算将计算任务分布到多个 Worker 上，如 {numref}`distributed-timeline` 所示。无论是在单机多核编程，还是在集群多机，都需要一个调度器（Scheduler）将计算任务分布到不同的 Worker 上。随着更多 Worker 参与，任务总时间缩短，节省的时间可用于其他任务。

```{figure} ../img/ch-intro/distributed-timeline.svg
---
width: 600px
name: distributed-timeline
---
Timeline Illustrating Distributed Execution
```