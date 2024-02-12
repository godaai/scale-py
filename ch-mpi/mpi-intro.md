(mpi-intro)=
# Introduction to MPI

Message Passing Interface (MPI) is a classic parallel computing tool. Due to its age, it may be unfamiliar to new generations of programmers who often overlook its importance. However, with the advent of large neural models, MPI or communication libraries based on the MPI philosophy have regained attention. This is because large models necessitate parallel computing frameworks for multi-machine communication. For instance, the [DeepSpeed](https://github.com/microsoft/DeepSpeed) framework utilizes mpi4py for multi-node communication.

## History

The development of MPI dates back to the late 1980s and early 1990s, with the emergence of supercomputers primarily used for scientific and engineering computations in fields such as weather forecasting, nuclear research, molecular dynamics, etc. Before MPI, to enable programs running in parallel, various research groups and organizations independently developed their communication libraries. However, this led to interoperability and portability issues. Consequently, there was a pressing need for a standardized approach to writing parallel applications.

In 1992, Jack Dongarra, who won the Turing Award, along with other scholars, proposed the first draft of parallel computing: MPI1. The initial standard version MPI 1.0 was eventually released in 1994. Subsequently, MPI-2 and MPI-3 were released, with contributions from academia and industry.

## Standard and Implementations

MPI is a standard, not a compiler or programming language, nor is it a specific implementation or product. Frameworks like Dask and Ray are specific implementations, whereas MPI is different; it is a standard, and different vendors can have their implementations under this standard. "Standard" means that MPI defines standardized functions or methods that all vendors must follow, while "implementation" means that different software and hardware vendors can implement low-level communication based on the standard. For example, if there is a need to implement data sending, the MPI standard defines the `MPI_Send` method that all vendors must adhere to.

The MPI standard defines:

* The function name and parameter list for each function.
* The semantics of each function, indicating the expected functionality, what each function can or cannot do.

Commonly used implementations include Open MPI, MPICH, Intel MPI, Microsoft MPI, and NVIDIA HPC-X. Since MPI is a standard, the same code can be compiled by OpenMPI or Intel MPI. Each implementation is developed by specific vendors or open-source communities, leading to some differences in usage.

## High-Speed Networks

For multi-node parallelism, high-speed interconnects are essential. MPI can efficiently utilize the high bandwidth and low latency networks. These networks typically have bandwidths exceeding 100 Gbps, but at a higher cost.

Cloud data centers often deploy 10/25 Gigabit Ethernet networks, which operate at a bandwidth level of 10/25 Gbps. MPI can also be used in such environments.

MPI can also run on a single machine, leveraging multiple computing cores on a single node.

## Installation

As mentioned earlier, MPI has different implementations, and different MPI vendors generally provide:

* Compilers: `mpicc`, `mpicxx`, and `mpifort` used to compile source code written in C, C++, and Fortran, respectively.
* `mpirun` or `mpiexec` for launching parallel programs on multiple nodes.

:::{note}
In many MPI implementations, `mpirun` and `mpiexec` have nearly identical functionalities and can both launch parallel programs. In some MPI implementations, `mpirun` and `mpiexec` are backed by the same program. However, strictly speaking, the MPI standard only defines `mpiexec`, not `mpirun`. Therefore, `mpiexec` is more portable.
:::

Here are the steps for C/C++ or Fortran developers: (1) write your source code; (2) use `mpicc` to compile the source code and obtain an executable; and (3) use `mpiexec` to launch the parallel program on multiple nodes. However, mpi4py developers do not need to compile the source code.

If your cluster already has MPI installed, you can load MPI into your environment and then use `pip` to install mpi4py:

```bash
pip install mpi4py
```

If your cluster does not have MPI, and you are not familiar with compiling MPI from source code, you can install MPI using `conda`. 

```bash
conda install -c conda-forge mpich
conda install -c conda-forge mpi4py
```