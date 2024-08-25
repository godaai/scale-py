(sec-dask-ml-preprocessing)=
# Data Preprocessing

In {numref}`sec-data-science-lifecycle`, we mention that the core of data science work lies in understanding and processing data. Dask is capable of scaling many single-machine tasks onto clusters, and can be combined with data visualization libraries.

In terms of distributed data preprocessing, we may rely more on the capabilities of Dask DataFrame and Dask Array, which will not be elaborated here.

On the feature engineering part, Dask-ML has implemented many APIs from `sklearn.preprocessing`, such as [`MinMaxScaler`](https://ml.dask.org/modules/generated/dask_ml.preprocessing.MinMaxScaler.html). One area where Dask differs slightly is in its implementation of one-hot encoding. As of the writing of this book, Dask uses [`DummyEncoder`](https://ml.dask.org/modules/generated/dask_ml.preprocessing.DummyEncoder.html) for one-hot encoding of categorical features, with `DummyEncoder` serving as the Dask alternative to scikit-learn's `OneHotEncoder`. We will present a case study on categorical features in {numref}`sec-dask-ml-hyperparameter`.