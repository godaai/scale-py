(sec-deep-learning-intro)=
# Deep Learning

## Deep Neural Networks

Deep learning is a shorthand term for deep neural networks. Basically, a neural network is composed of many instances of the following formula, and a deep neural network is made up of a stack of many neural network layers.

$$ 
\begin{aligned} 
\boldsymbol{z} &= \boldsymbol{W} \cdot \boldsymbol{x} + \boldsymbol{b} \\
\boldsymbol{a} &= f(\boldsymbol{z}) 
\end{aligned} 
$$

Here, $\boldsymbol{x}$ is the input, $\boldsymbol{W}$ represents the parameters (also known as weights) of the neural network. The training of a neural network involves continuously updating the parameters $\boldsymbol{W}$. Once trained, the model can be used for inference and predicting unknown data.

$f$ represents the activation function. The multiplication of $\boldsymbol{W}$ and $\boldsymbol{x}$ is a linear transformation. Even with multiple multiplications combined, it remains a linear transformation. In other words, a multi-layer network without an activation function would degrade into a single-layer linear model. Activation functions introduce non-linearity, allowing multi-layer neural networks to theoretically fit any input-output pattern. From a biological perspective, activation functions serve to activate or deactivate certain neurons. Common activation functions include Sigmoid and ReLU. We have visualized the Sigmod function in {numref}`sec-machine-learning-intro`, and the formula for ReLU is: $ f(x) = \max (0, x) $.

## Forward Propagation

{numref}`fig-forward-pass` represents the simplest form of a neural network: stacking $\boldsymbol{z^{[n]}} = \boldsymbol{W^{[n]}} \cdot \boldsymbol{a^{[n-1]}} + \boldsymbol{b^{[n]}}$ and $\boldsymbol{a^{[n]}} = f(\boldsymbol{z^{[n]}})$, where the previous layer's output $\boldsymbol{a^{[n-1]}}$ becomes the input of the next layer. This type of network is known as a feedforward neural network (FFN) or a multilayer perceptron (MLP). To make different layers clear, square bracket superscripts are used to differentiate between layers. For example, $\boldsymbol{a^{[1]}}$ represents the output of the first layer, and $\boldsymbol{W^{[1]}}$ represents the parameters of the first layer.

```{figure} ../img/ch-data-science/forward-pass.svg
---
width: 800px
name: fig-forward-pass
---
Forward propagation in a neural network
```

{numref}`fig-forward-pass` illustrates the process of forward propagation in a neural network. Assuming the input $\boldsymbol{x}$ is a 3-dimensional vector, each circle in {numref}`fig-forward-pass` represents an element (a scalar value) of the vector. The diagram also demonstrates the vectorized calculation of $\boldsymbol{a^{[1]}}$ in the first layer and the scalar calculation of $z^{[1]}_1$. In practice, modern processors' vectorized engines are often utilized for such computations.

## Backpropagation

The training of a neural network is updating the $\boldsymbol{W}$ and $\boldsymbol{b}$ of each layer.

First, initialize the $\boldsymbol{W}$ and $\boldsymbol{b}$ of each layer using some random initialization method, such as initializing them from a normal distribution.

Then, define a loss function $L$. The loss function measures the difference between the predicted values $\hat{y}$ of the neural network and the true values $y$. The goal of training is to minimize the loss function. For example, in a housing price prediction case, the squared error is commonly used as the loss function, where the loss function for a single sample is defined as $L = (y - \hat{y})^2$.

Next, calculate the derivatives of the loss function with respect to the parameters of each layer. The derivatives of $L$ with respect to the $\boldsymbol{W^{[l]}}$ and $\boldsymbol{b^{[l]}}$ of the $l$-th layer are denoted as $\frac{\partial L}{\partial \boldsymbol{W^{[l]}}}$ and $\frac{\partial L}{\partial \boldsymbol{b^{[l]}}}$, respectively. The $\boldsymbol{W^{[l]}}$ and $\boldsymbol{b^{[l]}}$ are then updated using the following formulas:

$$ 
\begin{aligned} 
\boldsymbol{W^{[l]}} &= \boldsymbol{W^{[l]}}-\alpha\frac{\partial L}{\partial \boldsymbol{W^{[l]}}} \\
\boldsymbol{b^{[l]}} &= \boldsymbol{b^{[l]}}-\alpha\frac{\partial L}{\partial \boldsymbol{b^{[l]}}}\ 
\end{aligned} 
$$

Here, $\alpha$ is the learning rate, which controls the speed of parameter updates. If the learning rate is too large, the algorithm may oscillate and fail to converge. If the learning rate is too small, the convergence speed may be too slow.

The derivatives of each layer are also referred to as gradients. The parameters are updated in the descenting direction of the gradients, which is known as gradient descent. When computing the derivatives of each layer, it starts from the loss function and calculates the gradients layer by layer in a backward manner, using the chain rule. {numref}`fig-back-propagation` illustrates the process of backpropagation in a neural network.

```{figure} ../img/ch-data-science/back-propagation.svg
---
width: 800px
name: fig-back-propagation
---
Backpropagation in a neural network
```

## Hyperparameters

During the neural network training phase, several parameters need to be manually set before training the model. These parameters cannot be learned automatically through the model's backpropagation and require manual selection and adjustment. These parameters are called hyperparameters, and their selection is usually based on experience or trial and error. Here are some examples of hyperparameters:

* Learning rate, which was mentioned earlier as $\alpha$, controls the step size of each parameter update.
* Network architecture: the number of layers in the model, the number of neurons in each layer, the choice of activation functions, etc. Different network architectures may have different performance for different tasks.

## Implementation Details

Neural network training includes the following three steps:

1. Forward pass
2. Backward pass (backpropagation)
3. Update of the model's weights

{numref}`fig-model-training-input-output` illustrates the inputs and outputs for the training of the i-th layer of a neural network, as outlined in the three steps above.

```{figure} ../img/ch-data-science/model-training-input-output.svg
---
width: 800px
name: fig-model-training-input-output
---
Forward, Backward, and Model Weight Update: Inputs and Outputs
```

### Forward Pass

- **Input:** The input for forward pass consists of two parts: the output of layer $ i-1 $, denoted as $ \boldsymbol{a^{[i-1]}} $, and the model weights and biases for layer $ i $, denoted as $ \boldsymbol{W^{[i]}} $ and $ \boldsymbol{b^{[i]}} $, respectively.
- **Output:** The output, also known as the activation, is produced after applying the weights and biases to the input and passing it through an activation function.

### Backward Propagation

- **Input:** The input for backward propagation includes three parts: the output of layer $ i $, $ \boldsymbol{a^{[i]}} $; the model weights and biases for layer $ i $, $ \boldsymbol{W^{[i]}} $ and $ \boldsymbol{b^{[i]}} $; and the gradient of the loss with respect to the output of layer $ i $, given as $ \frac{\partial L}{\partial a^{[i]}} $.
- **Output:** By applying the chain rule, the output is the gradient of the loss with respect to the model weights and biases of layer $ i $, expressed as $ \frac{\partial L}{\partial W^{[i]}} $ and $ \frac{\partial L}{\partial b^{[i]}} $.

### Model Weight Update

The input for updating the model weights includes the calculated gradients from the backward propagation and the learning rate $ \alpha $, which is a hyperparameter that determines the step size in the direction opposite to the gradient. The simplest gradient descent is: $\boldsymbol{W^{[l]}} = \boldsymbol{W^{[l]}} - \alpha \frac{\partial L}{\partial \boldsymbol{W^{[l]}}}$. For more complex optimizers, such as Adam {cite}`kingma2015Adam`, which introduces momentum that is the exponentially weighted average of the gradient. There is an additional matrix for maintaining the moving average of the gradients. This matrix is the state of the optimizer.
Therefore, the optimizer state, the model weights, and the gradients together serve as inputs to obtain the updated model weights.

### Neural Network Training Process

The training process for a neural network is depicted in {numref}`fig-model-training`. {numref}`fig-model-training` illustrates a 3-layer neural network, with the forward process denoted by FWD and the backward process denoted by BWD.

```{figure} ../img/ch-data-science/model-training.svg
---
width: 600px
name: fig-model-training
---
Forward (denoted by FWD) and Backward (denoted by BWD), and Model Weight Update.
```

## Inference

Model training involves both forward and backward propagation, while model inference only requires forward propagation, where the input is the data that needs to be predicted.