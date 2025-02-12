# MPI and Large Models

This chapter mainly talks about the parallel methods for large models. Large models refer to neural networks with a vast number of parameters that must be trained and inferred in parallel. Large model parallelism has the following characteristics:

* Computation runs on accelerators like GPUs, which are designed to improve computational efficiency.
* The cost of accelerators is very high, so efforts should be made to maximize their utilization to ensure a return on investment.
* Due to the enormous number of model parameters, a large amount of data may need to be transferred between accelerators during training or inference, requiring high bandwidth and low latency to ensure efficiency.

This chapter will provide a detailed explanation of the concepts and principles, while specific implementation details can be found in other academic papers and open-source libraries.

```{tableofcontents}
```