(sec-pipeline-parallel)=
# Pipeline Parallelism

Pipeline parallelism is a common method for large model parallelism. When the model size does not exceed the memory capacity of a single GPU, data parallelism becomes the simplest and most convenient option, which involves replicating the model weights on each GPU. However, modern models have become so large that they cannot fit into a single GPU, such as GPT-3 with 175B parameters. Even using FP16 format storage, it requires 350GB of storage space, while a single NVIDIA A100 or H100 GPU has only 80GB of memory. Pipeline parallelism provides a solution to this problem by assigning different layers of the large model to different GPUs. This core idea is detailed in {numref}`fig-pipeline-parallel-img`.

```{figure} ../img/ch-mpi-large-model/pipeline-parallel.svg
---
width: 600px
name: fig-pipeline-parallel-img
---
Simple Pipeline Parallelism Diagram
```

## Simple Pipeline Parallelism

Suppose the model is split into two parts, with the first part on GPU 0 and the second part on GPU 1. Each GPU computes forward and backward propagation, as shown in {numref}`fig-pipeline-parallel-distributed`.

* During forward propagation, the output needs to be transferred between GPUs.
* During backward propagation, the gradient of the loss regarding the output needs to be transferred between GPUs.

```{figure} ../img/ch-mpi-large-model/pipeline-parallel-distributed.svg
---
width: 600px
name: fig-pipeline-parallel-distributed
---
Using pipeline parallelism on two GPUs
```

In this simple pipeline parallelism scenario, only point-to-point communication (`MPI.Send` and `MPI.Recv`) is needed, without any collective communication.

Simple pipeline parallelism has a critical drawback, which is **low GPU utilization**. This is mainly reflected in:

* At any given time, only one GPU is performing computation, while other GPUs are waiting for the upstream or downstream computation results. If the time cost of communication is not considered, the GPU utilization is only $\frac{1}{\# GPUs}\%$.
* If the time cost of communication is considered, the GPU waits for data transmission from the network card, and there is no overlap between GPU computation and GPU-to-GPU communication. GPU devices and network devices are independent of each other; while the GPU is performing the current batch of computations, the network device could be transmitting the previous batch of data, allowing both to work simultaneously.

To address these issues, researchers have proposed several methods to optimize pipeline parallelism from the perspectives of data partitioning and overlapping to improve GPU utilization. These methods are improvements based on simple pipeline parallelism. Readers can refer to the original papers for more details, which will not be elaborated here.

* GPipe {cite}`huang2019GPipe`。
* PipeDream {cite}`narayanan2019PipeDream`。
* Megatron-LM {cite}`narayanan2021Efficient`。

## Pipeline Parallelism + Data Parallelism

Pipeline parallelism and data parallelism are two orthogonal methods that can be combined to improve computational efficiency. To avoid errors during data transmission, MPI's Communicator shall be used for isolation and coordination. As mentioned in {numref}`sec-mpi-hello-world`, a Communicator in MPI can be understood as a communication group, allowing the same GPU to participate in multiple different Communicators.

As shown in {numref}`fig-pipeline-parallel-data-parallel`, we created two types of Communicators: the red ones for pipeline parallelism and the blue ones for data parallelism. The same GPU can belong to both Communicators simultaneously, enabling it to handle communication between model layers in pipeline parallelism and participate in gradient synchronization in data parallelism.

```{figure} ../img/ch-mpi-large-model/pipeline-parallel-data-parallel.svg
---
width: 600px
name: fig-pipeline-parallel-data-parallel
---
Pipeline parallelism combined with data parallelism
```

So far, we have introduced two of the most basic methods for large model parallel training: data parallelism and pipeline parallelism. The implementation of industrial-grade distributed training libraries is far more complex, but the underlying principles remain the same.