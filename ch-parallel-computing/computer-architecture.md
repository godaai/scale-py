(computer-architecture)=
# Modern Computer Architecture

The increasing demand for computing power in big data and artificial intelligence applications has led chip and hardware manufacturers to focus on the development of multicore, cluster, and heterogeneous computing. {numref}`computer-arch` shows the architecture of modern computers.

```{figure} ../img/ch-parallel-computing/computer-arch.svg
---
width: 600px
name: computer-arch
---
Modern Computer Architecture
```

Multicore refers to a computer that has multiple Central Processing Units (CPUs), each with multiple computing cores. The CPU has its own cache, such as Level 1 Cache (L1 Cache) or Level 2 Cache (L2 Cache), and the main memory is located outside the CPU.

Cluster refers to multiple computers connected through a high-speed network, with each computer equipped with a Network Interface Card (NIC).

In recent years, heterogeneous computing, represented by GPUs, has emerged as the core of artificial intelligence computing. Heterogeneous computing refers to microarchitectures other than CPUs, such as graphics processing units (GPUs), field-programmable gate arrays (FPGAs). In heterogeneous computing, CPUs are still responsible for traditional processing and scheduling, while devices such as GPUs are used to accelerate specific tasks such as graphics, image processing, artificial intelligence, and blockchain.

## CPU

Modern CPUs usually have multiple computing cores. For example, laptops and desktops can have up to a dozen cores, while data center servers can have hundreds of cores. However, distributing computing tasks to multiple cores is not simple and requires developers to schedule the tasks to different cores properly when programming.

## Network Interface Card

The computing power of a single computer node is limited. To build a high-speed interconnected cluster, data center servers are usually equipped with high-speed networks such as RDMA over Converged Ethernet (RoCE) or InfiniBand. Each computer is equipped with at least one high-speed NIC, and multiple computers are interconnected by fiber optics to achieve low latency and high throughput. This allows data access between different nodes as if data are on a single node.

## Heterogeneous Computing

In heterogeneous computing, the CPUs and main memory are usually referred to as the host, while various specialized accelerators are referred to as devices. Although heterogeneous computing is a broad concept, GPU-based heterogeneous computing is currently mainstream, especially with NVIDIA GPUs dominating a significant market share. Therefore, this section mainly focuses on GPUs as an example of heterogeneous computing. Compared to CPUs, GPUs have different chip microarchitectures and software stacks. In terms of software, NVIDIA GPUs provide the CUDA (Compute Unified Device Architecture) programming interface, and in terms of hardware, GPUs have multiple specialized computing cores (CUDA Cores and Tensor Cores) and GPU memory. Typically, there is a time cost in moving data from main memory to GPU memory.