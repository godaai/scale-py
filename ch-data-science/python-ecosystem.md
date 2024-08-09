(sec-ecosystem)=
# Ecosystem and Content

## Python Ecosystem

Python has become the de-facto programming language for data science. {numref}`fig-python-ecosystem-img` illustrates some of the mainstream tools in data science:

* NumPy and pandas can be used for scientific computing and data processing.
* PyTorch and TensorFlow enable the training and inference of neural networks.
* Libraries such as scikit-learn, XGBoost, and LightGBM implement common machine learning algorithms.

```{figure} ../img/ch-data-science/python-ecosystem.svg
---
width: 800px
name: fig-python-ecosystem-img
---
Python Data Science Ecosystem
```

## Content of This Book

This book assumes that readers already have some understanding of data science and have used Python data science software such as pandas, XGBoost, and PyTorch. It is intended for those who wish to use certain tools to accelerate their data science endeavors. If you are not familiar with data science, you may consider reading the following books:

* "Python for Data Analysis" by Wes McKinney {cite}`mckinney2022python`, the founder of the pandas project, is an excellent introductory book on data science and an entry-level book for the pandas framework.
* Professor Andrew Ng videos and lecture notes on machine learning.
* "Dive into Deep Learning" by Aston Zhang, Mu Li, and others {cite}`zhang2019dive` covers common artificial intelligence algorithms and their applications from the principles to programming practices. It is the best practical book for beginners to deep learning.

Dask, Ray, Xorbits, and mpi4py are extensions to the data science ecosystem, scaling single-machine tasks horizontally to clusters. These frameworks consist of many components. {numref}`tab-lifecycle-module` summarizes the data science lifecycle corresponding to the components of these frameworks.

```{table} Data Science Lifecycle and Framework Components
:name: tab-lifecycle-module
|Lifecycle|Component|
|---|---|
|Data Preprocessing|Dask DataFrame、Dask Array、Ray Data、Modin、Xorbits Data|
|Model Training|Dask-ML、Ray Train、RLib、mpi4py|
|Hyperparameter Tuning|Dask-ML、Ray Tune|
|Model Serving|Ray Serve、Xinference|
```

## Tutorials and Datasets in This Book

This book offers a multitude of reproducible tutorials. Readers can `git clone` or download them, and run them on their local machines, Google colab, or clusters, running them with Jupyter Notebook.

Regarding datasets, this book utilizes datasets such as taxi trips and flights. For the convenience of readers in automatically downloading and decompressing when running the case studies, the book encapsulates the dataset loading code into functions placed in `utils.py`. For example, the function for the taxi dataset is named `nyc_taxi`, and that for the airplane flight dataset is named `nyc_flights`.