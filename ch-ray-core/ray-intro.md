# Introduction to Ray

Ray is a computing framework initially designed for reinforcement learning, gradually evolving into a framework catering to data science and artificial intelligence.

As depicted in {numref}`ray-ecosystem`, Ray consists of the foundational Ray Core and various Ray AIR (Artificial Intelligence Runtime) components at the higher levels. Ray Core comprises a set of low-level APIs, enabling the horizontal scaling of Python functions or classes across multiple computing nodes. On top of Ray Core, Ray encapsulates several libraries tailored for data science and artificial intelligence within the Ray AIR ecosystem. These include functionalities for data processing (Ray Data), model training (Ray Train), hyperparameter tuning (Ray Tune), model serving (Ray Serve), reinforcement learning (RLib), and more.

```{figure} ../img/ch-ray-core/ray.svg
---
width: 800px
name: ray-ecosystem
---
Ray ecosystem
```

Ray Core provides APIs that horizontally scale Python tasks across a cluster. The key APIs include two computation interfaces and one data interface, as illustrated in {numref}`ray-core-apis`.

* **Task**: Python functions that can be scaled across the cluster.
* **Actor**: Python classes that can be scaled across the cluster.
* **Object**: Immutable distributed objects used for transferring data between Tasks and Actors.

Ray AIR ecosystem is built upon the Ray Core APIs.

```{figure} ../img/ch-ray-core/ray-apis.svg
---
width: 800px
name: ray-core-apis
---
Ray Core APIs
```