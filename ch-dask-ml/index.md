# Machine Learning with Dask

This chapter will focus on machine learning with Dask, and introduces the Dask-ML library. Dask-ML is based on Dask's distributed computing capabilities and can seamlessly integrate with machine learning libraries such as scikit-learn and XGBoost. In comparison, Dask-ML is more suitable for traditional machine learning training and inference, such as regression, decision trees, etc., while deep learning are based on frameworks like PyTorch or TensorFlow.

In summary, Dask and Dask-ML are suitable for the following scenarios:

* Raw data cannot fit into a single machine's memory, requiring distributed data preprocessing and feature engineering;
* Training data and models can fit into a single machine's memory, but hyperparameter tuning can be run in parallel across multiple machines;
* Training data cannot fit into a single machine's memory, necessitating distributed training.

On one hand, the Dask community primarily focuses on the development of Dask DataFrame, with relatively less investment in Dask-ML and distributed training. On the other hand, deep learning has had a significant impact on traditional machine learning algorithms, and Dask was not specifically designed for deep learning. After reading this chapter and understanding Dask's capabilities in machine learning, readers can choose the most suitable framework according to their actual needs.

```{tableofcontents}
```