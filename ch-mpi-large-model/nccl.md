# Introduction to NCCL

With the wide adoption of GPUs in high-performance computing, especially in deep learning and large model training, the needs for latency and bandwidth computing have become increasingly stringent and achieving efficient data transfer between multiple GPUs has become increasingly important. In GPU programming, data often needs to be copied between the CPU and GPU. 

The existing tool, MPI, was initially designed for CPU clusters and does not fully adapt to the application scenarios of large-scale GPU clusters. For example, in traditional MPI, data transfer occurs between processes. But on a single-machine multi-GPU server, a large amount of data transfer is usually required between multiple GPUs. As shown in {numref}`fig-mpi-wo-gpu-direct`, GPU communication across multiple nodes may requires the following steps: first, data is copied from the GPU to the CPU, and then MPI is used for data sending and receiving. To better serve the needs of large-scale GPU clusters and deep learning applications, NVIDIA designed the NVIDIA Collective Communications Library (NCCL), which aims to address various issues encountered by MPI on large-scale GPU clusters.

```{figure} ../img/ch-mpi-large-model/mpi-wo-gpu-direct.svg
---
width: 800px
name: fig-mpi-wo-gpu-direct
---
First, copy the data from the GPU to the CPU, and then perform communication
```

MPI and NCCL are not designed to replace each other. Many communication primitives in NCCL, such as point-to-point communication and collective communication, are influenced by MPI design. We can say that NCCL is an extension based on MPI, and it is more suitable for GPU cluster environments. {numref}`fig-gpu-communication` shows the communication primitives implemented by NCCL.

```{figure} ../img/ch-mpi-large-model/gpu-communication.svg
---
width: 800px
name: fig-gpu-communication
---
Common communication primitives with NCCL implementation
```

Similarly, other accelerator manufacturers have also proposed their own communication libraries, such as:

* AMD provides RCCL (ROCm Communication Collectives Library) for ROCm
* Huawei provides HCCL (Huawei Collective Communication Library)

These collective communication libraries are tailored for specific hardware, aiming to address communication challenges in specific cluster environments.

NCCL mainly provides C/C++ programming interfaces. For developers in the Python community who need to use NCCL, they can use PyTorch's `torch.distributed` library. NCCL is also the recommended GPU parallel computing backend for PyTorch. This book will not delve into the usage details of `torch.distributed`, but will continue to use MPI to demonstrate various communication patterns involved in large model training and inference.