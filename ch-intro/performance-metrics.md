(performance-metrics)=
# Performance Metrics

In order to objectively evaluate the performance of parallel programs, there need to be some standards. FLOPS and speedup ratio are the most common metrics, and there are also specific benchmarks for certain applications, such as artificial intelligence and big data applications.

## FLOPS

Traditional high-performance computing often uses FLOPS (Floating Point Operations per Second) to measure the performance of software and hardware.

:::{note} 
Floating-point numbers refer to decimal numbers represented by a certain number of bits in a computer. The more bits used, the more accurate and precise the values, but the higher the computational cost. The Institute of Electrical and Electronics Engineers (IEEE) has defined the representation of 16-bit floating-point numbers (FP16), 32-bit floating-point numbers (FP32), and 64-bit floating-point numbers (FP64) in computers. Most scientific computing tasks require FP64, while tasks like deep learning only need FP32, FP16, or even lower precision. It is important to specify whether FLOPS is calculated using FP32 or FP64 precision, as different hardware can provide significantly different FP32 and FP64 computational capabilities. 
:::

FLOPS refers to the number of floating-point operations that can be completed per second. For example, if performing an $n$-dimensional vector addition: $a + b$, the number of floating-point calculations required is $n$. Dividing the number of floating-point calculations by time gives the FLOPS.

The FLOPS metric depends on both hardware performance and software/algorithm design. As mentioned in {numref}`thread-process`, thread safety is a concern, and {numref}`serial-parallel` describes the task distribution process. If the software algorithm design is not optimal and a large amount of computational resources are idle, the FLOPS of the application may be low.

## Speedup Ratio

In theory, parallel programs should be faster and take less time than their corresponding serial programs. The reduction in execution time can be measured using the speedup ratio (SR):

$$ 
SR = \frac{t_s}{t_p} 
$$

where $t_s$ is the execution time of the serial program and $t_p$ is the execution time of the parallel program.

Based on the speedup ratio metric, there is another measure called efficiency (E):

$$ 
E = \frac{SR}{N} = \frac{t_s}{N \cdot {t_p}} 
$$

where $N$ is the number of computational cores used by the parallel program. When the speedup ratio is $N$, the serial program can be linearly scaled to multiple computational cores, achieving linear speedup.

Linear speedup is the most ideal case but is difficult to achieve in practice. As shown in {numref}`serial-parallel`, the diagram illustrates that parallel programs require a scheduler to distribute different tasks to multiple workers, and there is also communication between the workers.

Additionally, when using GPUs, there is some controversy over the value of $N$ for the computation efficiency metric. GPUs have thousands of computational cores, making it difficult to obtain $t_s$ on a single GPU core. Since GPUs and CPUs work together, should the CPU time be considered when calculating the speedup ratio or efficiency?