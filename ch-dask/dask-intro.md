# Introduction to Dask

Dask is a parallel computing framework for Python that allows you to scale your computational tasks to multiple cores and clusters. It provides two types of APIs: high-level DataFrame and Array APIs that mimic the APIs of pandas and NumPy, and low-level task graph-based APIs that can be combined with many Python packages. With these two APIs, Dask has built an ecosystem to handle large datasets and various data science tasks.

The core idea of Dask is to build a task graph, which breaks down a large computational task into smaller tasks. Each task calls the Python packages (such as pandas and NumPy) as execution backends.

{numref}`dask-overview` shows a schematic diagram of the Dask APIs, task graph, and how it is finally scheduled on computing nodes.

```{figure} ../img/ch-dask/dask-overview.svg
---
width: 800px
name: dask-overview
---
Dask Architecture
```

:::{note} 
Dask is a parallel computing framework designed for big data. However, Dask Team recommends that if your data can fit into memory on a single machine, it is recommended to use traditional single-machine Python packages. This is because not all computations are easily parallelizable, and some tasks may even perform worse after parallelization. 
:::

Installing Dask is straightforward. You can use `pip` or `conda` to install the necessary packages:

```
pip install dask[complete]
```

Once installed, you can run Dask on multiple cores of a single machine. This book will start with single-machine scenarios, and for multi-machine scenarios, you only need to modify the scheduler.