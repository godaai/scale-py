(ray-data-intro)=
# Ray Data Overview

Ray Data is a data processing framework built on top of Ray Core, primarily addressing data preparation and processing tasks related to machine learning training or inference, or the "last mile" from storage to distributed applications.

Ray Data provides an abstract class for data, [`ray.data.Dataset`](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.html), offering common primitives for big data processing on the `Dataset`. It covers most stages of data processing, including:

* Data loading, such as reading Parquet files.
* Transformation operations on data, such as [`map_batches()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html).
* Grouping and aggregation operations, such as [`groupby()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.groupby.html).
* Data shuffling, such as [`random_shuffle()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.random_shuffle.html) and [`repartition()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.repartition.html).

## Key Concepts

Ray Data is tailored for machine learning, and its design philosophy aligns closely with the machine learning workflow. It mainly encompasses:

* Data loading and storage
* Data transformation
* Machine learning feature preprocessing
* Tight integration of datasets and machine learning models

## Dataset

Ray Data is based on the `ray.data.Dataset` object. The `Dataset` is a distributed data object, with the basic unit being a `Block`. The `Dataset` is a distributed `ObjectRef[Block]` consisting of multiple `Block`s. A `Block` is a data structure based on the Apache Arrow format.

{numref}`ray-dataset-arch` is illustrative of a dataset composed of three `Block`s, each containing 1,000 rows of data.

```{figure} ../img/ch-ray-data/dataset-arch.svg
---
width: 600px
name: ray-dataset-arch
---
Ray Dataset
```

We can use `from_*()` APIs to import data from other systems or formats into a `Dataset`, such as [`from_pandas()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.from_pandas.html), [`from_spark()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.from_spark.html). We can use `read_*()` APIs to read data from persistent file systems, such as [`read_parquet()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.read_parquet.html), [`read_json()`](https://docs.ray.io/en/latest/data/api/doc/ray.data.read_json.html), and so on.

## Data Operations and Underlying Implementation

### Data Reading and Writing

As shown in {numref}`ray-dataset-read`, Ray Data utilizes Ray tasks to read and write data in parallel. The concept behind Ray tasks is straightforward—each task reads a small portion of data, yielding multiple `Block`s. The parallelism during reading can be adjusted by setting the `parallelism`.

```{figure} ../img/ch-ray-data/dataset-read.svg
---
width: 600px
name: ray-dataset-read
---
Illustration of Reading in Ray Data
```

### Data Transformation

As illustrated in {numref}`ray-dataset-map`, data transformation operations utilize Ray tasks or Ray actors to operate on each `Block`. For stateless transformation operations, the underlying implementation is Ray tasks, while for stateful transformation operations, Ray actors are used.

```{figure} ../img/ch-ray-data/dataset-map.svg
---
width: 600px
name: ray-dataset-map
---
Illustration of transformations in Ray Data
```

Next, we will delve into the details of several types of data operations.