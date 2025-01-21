(sec-ray-serve)=
# Ray Serve

A production-ready model inference system usually has a long chain:

* External service API: It may be HTTP or based on Remote Procedure Call (RPC). The external service API is also called Ingress. Other users or programs access the model inference service through Ingress. HTTP service can be based on [FastAPI](https://fastapi.tiangolo.com/), and RPC can be based on [gRPC](https://grpc.io/).
* Model inference engine: Given a model and input, perform model inference. The model inference engine may be a mature deep learning framework, such as PyTorch or TensorFlow; it may be a high-performance inference framework for a certain field, such as [vLLM](https://github.com/vllm-project/vllm) for large language models, or a framework developed by the manufacturer.
* Input and output processing module: perform necessary feature preprocessing on input data, or perform certain post-processing on model output. Taking input data preprocessing as an example, data may be stored in a database and need to be preprocessed before it can be delivered to the machine learning model.
* Multimodal: Large projects usually require multiple models to work together. For example, a short video recommendation system has multiple modules: recalling a small amount of content that users are most interested in from a large amount of video material, using different models to predict the user's click probability or stay time, and combining a variety of different indicators to sort the recalled content.

Ray Serve is a model reasoning service framework based on Ray. Ray Serve solves the pain points in model reasoning based on Ray's parallel capabilities:

* Based on Ray's parallel computing capabilities, the underlying layer can encapsulate any Python reasoning engine and support horizontal expansion and load balancing.

* The characteristics of the glue language can define complex model reasoning links, glue different data sources, reasoning engines and models together, allowing developers to perform agile development.

* Common Ingress, such as FastAPI and gRPC, are integrated.

## Key concepts

There are two key concepts in Ray Serve: deployment and application.

* [`Application`](https://docs.ray.io/en/latest/serve/api/doc/ray.serve.Application.html) is a complete reasoning application.
* [`Deployment`](https://docs.ray.io/en/latest/serve/api/doc/ray.serve.Deployment.html) can be understood as a submodule of the entire reasoning application, for example, preprocessing input data or using machine learning models for prediction. An Application can consist of many Deployments, each executes a certain business logic.
* Ingress is a special kind of Deployment. It is the access point of the inference service, and all access traffic flows in from Ingress. Ray Serve's Ingress uses [Starlette](https://www.starlette.io/) by default, and also supports FastAPI and gRPC.

## Example: Large language model reasoning

We will demonstrate how to use Ray Serve in conjunction with the large language model reasoning task. Specifically, we use [Transformers](https://github.com/huggingface/transformers) to implement the chat function. The Transformers library is the reasoning engine, and Ray Serve encapsulates Ingress, etc.

### Server

Model inference based on the Transformers library requires loading the tokenizer and model weights, and the model generates answers based on the input content. As shown in {numref}`code-llm`, we first implement an `LLM` class: its `__init__()` method loads the tokenizer and model weights; its `chat()` method generates content based on user input. Ray Serve adds three places on this basis:

* Add the [`ray.serve.deployment`](https://docs.ray.io/en/latest/serve/api/doc/ray.serve.deployment_decorator.html) decorator to the class, which is somewhat similar to `ray.remote`, indicating that the class is a `Deployment`.
* Define an `async def __call__()` method. When the user's HTTP request arrives, the `__call__()` method will be automatically triggered. The parameter of the `__call__()` method is `starlette.requests.Request`, which is the request sent by the user via HTTP.
* Generate this `Application` through `chat = LLM.bind()`. `chat` is the entry point of this `Application`.

```{code-block} python
:caption: llm.py
:name: code-llm
:emphasize-lines: 7,24-26,28

from transformers import AutoTokenizer, AutoModelForCausalLM
from starlette.requests import Request

import ray
from ray import serve

@serve.deployment(ray_actor_options={"num_cpus": 8, "num_gpus": 1})
class LLM:
    def __init__(self):
        self.model_dir = "AI-ModelScope/gemma-2b-it"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_dir,
            device_map="auto"
        )

    def chat(self, input_text: str) -> str:
        input_ids = self.tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**input_ids, max_new_tokens=1024)
        generated_text = self.tokenizer.decode(outputs[0])

        return generated_text
    
    async def __call__(self, http_request: Request) -> str:
        user_message: str = await http_request.json()
        return self.chat(user_message)

chat = LLM.bind()
```

Save this code as `llm.py`, and then use Ray Serve's command line tool `serve` to start this `Application`:

```bash
serve run llm:chat
```

Before running this command line, we must ensure that there is a file `llm.py` in the current working directory. `chat` in `llm:chat` is the `Application` generated by the `chat = LLM.bind()` method in the `llm.py` file. After running the command, Ray Serve will provide the inference service of the model at http://localhost:8000.

### Client

The `Application` defined above is a simple large language model inference service. It provides an HTTP interface, but there is no graphical interface and it cannot be opened using a browser. We need to send a request to the server to access this inference service, as shown in {numref}`code-client-chat`.

```{code-block} python
:caption: client-chat.py
:name: code-client-chat

import requests

prompt = "Could you explain what is dask?"

response = requests.post("http://localhost:8000/", json=prompt)
print(response.text)
```

Execute this client in the command line, and it will print out the content generated by the language model.

```bash
python client-chat.py
```

### Deployment parameters

`ray.serve.deployment` has some parameters to config model deployment. Ray Serve models run in Ray Actor, and `ray_actor_options` defines the computing resources required for each model replica. In particular, if the model needs to run on GPU, `{"num_gpus": n}` must be defined here, otherwise Ray will not allocate GPU for this task. The way to define resources here is consistent with the way in {numref}`sec-ray-computing-resource`.

Another important parameter of `ray.serve.deployment` is `num_replicas`, which is used to define how many `Deployment` replicas are generated.

### Configuration file

In addition to writing code definitions in `ray.serve.deployment`, you can also define these deployment parameters in the configuration file. The configuration file is a YAML file, as shown in {numref}`code-config-yaml`.

```{code-block} yaml
:caption: config.yaml
:name: code-config-yaml

proxy_location: EveryNode

http_options:
  host: 0.0.0.0
  port: 8901

grpc_options:
  port: 9000
  grpc_servicer_functions: []

applications:
- name: llm
  route_prefix: /
  import_path: llm:chat
  runtime_env: {}
  deployments:
  - name: LLM
    num_replicas: 1
    ray_actor_options:
      num_cpus: 8
      num_gpus: 1
```

For example, under `http_options`, set the IP address (`host`) and port number (`port`) of the external service. Ray Serve uses `0.0.0.0` and `8000` by default to start the service. `0.0.0.0` makes the service publicly accessible. Similar to `http_options`, `grpc_options` is for gRPC.

Under `applications` is a list, where multiple `Application`s can be defined. Each `Application` needs to define `import_path` and `route_prefix`. `import_path` is the entry point of this `Application`, and `route_prefix` corresponds to the routing prefix of the HTTP service. Each `Application` has one or more `Deployments`, and the definition of `Deployments` is consistent with `ray.serve.deployment`.

If settings are made in both the configuration file and `ray.serve.deployment`, Ray Serve will give priority to the parameters in the configuration file.