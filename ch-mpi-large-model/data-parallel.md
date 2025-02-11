(sec-data-parallel)=

# Data Parallelism

Data parallelism is one of the most common methods of large model parallelism, and compared to other parallel methods, data parallelism is simpler and more intuitive to implement. As shown in {numref}`fig-data-parallel-img`, copies of the model are loaded onto different GPU devices, and the training data is split into multiple parts, each of which is independently trained by a different GPU. This programming model is known as Single Program Multiple Data (SPMD).

```{figure} ../img/ch-mpi-large-model/data-parallel.svg
---
width: 500px
name: fig-data-parallel-img
---
Data Parallelism Diagram
```

## Non-Parallel Training

{numref}`sec-machine-learning-intro` introduces the process of training neural network models. We will first discuss the non-parallel scenario, using the MNIST handwritten digit recognition example for demonstration. As shown in {numref}`fig-data-parallel-single`, this example illustrates one forward pass and one backward pass.

```{figure} ../img/ch-mpi-large-model/data-parallel-single.svg
---
width: 600px
name: fig-data-parallel-single
---
Training a neural network on a single GPU
```

## Data Parallelism

Data parallelism involves splitting the dataset into multiple parts and replicating the model weights on different GPUs. As shown in {numref}`fig-data-parallel-distributed`, suppose there are two GPUs, each with a copy of the model weights and a corresponding subset of the input data. On each GPU, the forward and backward propagation processes are carried out **independently**: forward propagation calculates the output values of each layer, while backward propagation computes the gradients of the model weights. These computations are independent and do not interfere with each other across different GPUs.

```{figure} ../img/ch-mpi-large-model/data-parallel-distributed.svg
---
width: 600px
name: fig-data-parallel-distributed
---
Training a neural network on two GPUs
```

At least during the forward and backward propagation stages, there is no communication cost. However, when it comes to updating the model weights, synchronization is necessary because the gradients obtained on each GPU are different. The gradients can be averaged to obtain the final gradient. Here, we only demonstrate $\boldsymbol{W}$, where $\boldsymbol{\frac{\partial L}{\partial W}}^{i}$ is the gradient on a single GPU, and $\boldsymbol{{\frac{\partial L}{\partial W}}^{sync}}$ is the synchronized average.

$$
\boldsymbol{
    {\frac{\partial L}{\partial W}}^{sync} = \frac{1}{\# GPUs} \sum_{i=0}^{\# GPUs} {\frac{\partial L}{\partial W}}^{i}
}
$$

To synchronize the gradients across different GPUs, you can use the `AllReduce` primitive provided by MPI. MPI's `AllReduce` collects the independently computed gradients from each GPU, averages them, and then broadcasts the averaged gradient back to each GPU.

As shown in {numref}`fig-data-parallel-all-reduce`, during the gradient synchronization stage, MPI's `AllReduce` primitive ensures the consistency of gradients across all GPUs.

```{figure} ../img/ch-mpi-large-model/data-parallel-all-reduce.svg
---
width: 600px
name: fig-data-parallel-all-reduce
---
When updating model weights, you need to use MPI's `AllReduce` primitive to synchronize the gradients across all GPUs.
```