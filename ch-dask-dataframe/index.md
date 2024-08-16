# Dask DataFrame

While pandas has become the standard for DataFrames, it lacks the ability to harness the power of multiple cores and distributed computing. Dask DataFrame aims to address the challenges of parallel computing with pandas. While striving to offer a consistent API with pandas, Dask DataFrame introduces several differences. 
The Dask DataFrame partitions large datasets into smaller blocks, with each block being a pandas DataFrame. Dask records the metadata of the DataFrame and stores it in `_meta`. Information about multiple partitions is stored in the built-in variables `partitions` and `divisions`. 
Dask manages the computation graph using a Task Graph.
This chapter assumes that users are already familiar with pandas and focuses on discussing the distinctions between Dask DataFrame and pandas.

```{tableofcontents}
```