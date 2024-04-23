(parallel-program-design)=
# Parallel Programming Design Methods

## PCAM

How to design software and algorithms so that programs can run in parallel on multiple cores or clusters? As early as 1995, Ian Foster proposed the PCAM method in his book {cite}`foster1995designing`, which can guide the design of parallel algorithms. PCAM mainly consists of four steps: Partitioning, Communication, Agglomeration, and Mapping; {numref}`fig-pcam` illustrates these four steps.

```{figure} ../img/ch-intro/pcam.svg
---
width: 600px
name: fig-pcam
---
PCAM method
```

* Partitioning: Divide the entire problem into multiple sub-problems or sub-tasks.
* Communication: Define the communication between different sub-tasks, including data structures and communication algorithms.
* Agglomeration: Considering the current hardware performance and programming difficulty, further integrate the above two steps to aggregate fine-grained tasks into more efficient tasks.
* Mapping: Distribute the integrated tasks to multiple processors.

For example, consider a very large matrix, with a size of $M \times M$, which is too large to be computed on a single computing node. Now we want to find the maximum value in this matrix. When designing a parallel algorithm, we can consider the following approach:

* Divide the matrix into submatrices, each of size $m \times m$, and execute the `max()` function on each computing node to find the maximum value of the submatrix.
* Gather the maximum values of each submatrix to a single computing node, and then execute `max()` again on that node to find the maximum value of the entire matrix.
* The `max()` operation of $m \times m$ submatrix can be executed on a single computing node.
* Distribute the above computations to multiple nodes.

## Partitioning Methods

The most difficult and crucial part of designing parallel programs is how to perform partitioning. Common partitioning methods include:

* Task parallelism: A complex program often consists of multiple tasks, and different tasks are assigned to different workers. If there are not too many complex dependencies between tasks, this approach can be well parallelized.
* Data decomposition: The processed data is structured, such as a matrix that can be divided into one or multiple dimensions and assigned to different workers. The example mentioned earlier of finding the maximum value of a matrix is an example.

## Case Study: MapReduce

Google proposed MapReduce in 2004 {cite}`dean2004MapReduce`, which is a typical parallel computing paradigm for big data. {numref}`map-reduce` illustrates the processing flow of using MapReduce for word count.

```{figure} ../img/ch-intro/map-reduce.svg
---
width: 600px
name: map-reduce
---
Word count with MapReduce
```

MapReduce mainly involves four stages:

* Split: Divide the large data into many small data pieces, each of which can be computed on a single worker.
* Map: Perform the Map operation on each small data piece. Map is a programming function, and the developer needs to define the Map function, which outputs a key-value pair. In the example of word count, each occurrence of a word is counted as 1, with the word as the key and 1 as the value. In other words, the output of Map should be (word, 1).
* Shuffle: Group the same keys to the same worker. This stage involves data exchange. In the example of word count, the same words are sent to the same worker.
* Reduce: Aggregate all the same keys. The developer needs to define the Reduce function. In the example of word count, after the Shuffle stage, the same keys have been grouped together, and now we just need to sum up all the word frequencies.

The programming paradigm of MapReduce has deeply influenced open-source projects such as Apache Hadoop, Apache Spark, and Dask.