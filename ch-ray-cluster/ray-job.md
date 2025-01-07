(sec-ray-job)=
# Ray Job

After deploying a Ray cluster, we can submit jobs to the cluster. Ray jobs refer to specific computing tasks written by users based on Task, Actor or various Ray ecosystems (Ray Train, Ray Tune, Ray Serve, RLlib, etc.). Ray clusters try to provide multi-tenant services, which can execute multiple users' different computing tasks at the same time. Since Ray clusters provide multi-tenant services, different Ray jobs may have different source code, configuration files and software package environments. Therefore, when submitting a job, in addition to specifying the entry point of the `__main__` function of the current job, you also need to specify:

* Working directory: Contains Python source code and configuration files required for this job

* Software environment: Python packages and environment variables that this job depends on

There are three main ways to submit jobs to a Ray cluster, and all three require specifying the above job-related information.

* Ray Jobs command line

* Python Software Development Kit (SDK)

* Ray client

## Ray Jobs command line

### `ray job`

The `ray job` command line is a set of tools for managing Ray jobs. After installing Ray in the Python environment (via the command `pip install "ray[default]"`), the command line tools will be installed at the same time. `ray job` can be responsible for managing the entire life cycle of the job.

First, we need to write a Ray-based script and save it in the current directory with the file name `scripy.py`:
```python
import os

import ray

ray.init()

print('''This cluster consists of
    {} nodes in total
    {} CPU resources in total
'''.format(len(ray.nodes()), ray.cluster_resources()['CPU']))

@ray.remote
def generate_fibonacci(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1] + fibonacci[i-2])
    return len(fibonacci)

sequence_size = 10
results = ray.get([generate_fibonacci.remote(sequence_size) for _ in range(os.cpu_count())])
print(results)
```

Submit this job using `ray job submit`:

```bash
RAY_ADDRESS='http://127.0.0.1:8265' ray job submit --working-dir ./ -- python script.py
```

`RAY_ADDRESS` is set according to the address of the head node. If there is only a local Ray cluster, the head node's IP address is `127.0.0.1`, and the default port is 8265, then this address is `http://127.0.0.1:8265`; if there is a remote cluster, the address shall be changed to the IP or host name of the remote cluster.

The Ray Job command package the source code under the working directory `./`, submit the job to the cluster, and print the following information:
```
Job submission server address: http://127.0.0.1:8265
INFO dashboard_sdk.py:338 -- Uploading package gcs://_ray_pkg_bd62811ee3a826e8.zip.
INFO packaging.py:530 -- Creating a file package for local directory './'.

-------------------------------------------------------
Job 'raysubmit_VTRVfy8VEFY8vCdn' submitted successfully
-------------------------------------------------------
```

The format of `ray job submit` is: `ray job submit [OPTIONS] ENTRYPOINT...`. `[OPTIONS]` can specify some parameters. `--working-dir` is the working directory. Ray will package the contents of this directory and distribute them to each node of the Ray cluster. `ENTRYPOINT` refers to the Python script to be executed. In this case, it is `python script.py`. We can also pass parameters to this Python script, just like executing a Python script on a single machine: `python script.py --arg=val`.

The `--no-wait` parameter can submit the job to the Ray cluster first and return, instead of waiting for the job to end. The result of the job can be viewed through `ray job logs <jobid>`.
:::{note}
There is a space between `ENTRYPOINT` and `[OPTIONS]`.
:::

### Entrypoint

`ENTRYPOINT` is the entry point of the program. In the example above, the entry point of the program is the Ray Task that calls `generate_fibonacci`, and the Ray Task will be scheduled to the Ray cluster. By default, the entry point in `ENTRYPOINT` runs on the head node, because the resources of the head node are limited and cannot perform various complex calculations. It can only serve as an entry point. Various complex calculations should be performed in Tasks or Actors. By default, without additional configuration, Ray will schedule these calculations to the computing nodes according to the resource requirements set by Tasks or Actors. However, if the entry point of `ENTRYPOINT` (before calling Tasks or Actors) uses various resources, such as GPUs, then additional resources need to be allocated to this entry script. You need to set `--entrypoint-num-cpus`, `--entrypoint-num-gpus` or `--entrypoint-resources` in `[OPTIONS]`. For example, the following example allocates 1 GPU to the entry point.
```
RAY_ADDRESS='http://127.0.0.1:8265' ray job submit --working-dir ./ --entrypoint-num-gpus 1 -- python gpu.py
```

The code of `gpu.py` is as follows:

```python
import os
import ray

ray.init()

@ray.remote(num_gpus=1)
class GPUActor:
    def ping(self):
        print("GPU ids: {}".format(ray.get_runtime_context().get_accelerator_ids()["GPU"]))
        print("CUDA_VISIBLE_DEVICES: {}".format(os.environ["CUDA_VISIBLE_DEVICES"]))

@ray.remote(num_gpus=1)
def gpu_task():
    print("GPU ids: {}".format(ray.get_runtime_context().get_accelerator_ids()["GPU"]))
    print("CUDA_VISIBLE_DEVICES: {}".format(os.environ["CUDA_VISIBLE_DEVICES"]))

print("ENTRYPOINT CUDA_VISIBLE_DEVICES: {}".format(os.environ["CUDA_VISIBLE_DEVICES"]))
gpu_actor = GPUActor.remote()
ray.get(gpu_actor.ping.remote())
ray.get(gpu_task.remote())
```

Before calling Actor and Task, Ray allocates one GPU to the program entry. After calling Actor and Task, it allocates one GPU to gpu_actor and gpu_task respectively.

:::{note}
When submitting a job to an existing Ray cluster, the `num_cpus` and `num_gpus` parameters cannot be set in `ray.init()`.
:::

### Dependency Management

Ray cluster is multi-tenant. Different users' jobs may run on it with different requirements for Python dependency versions. To solve this, Ray provides runtime environment functions. For example, when starting this job, set `--runtime-env-json`, which is a JSON, including: Python packages that need to be installed by `pip`, or environment variables (`env_vars`), or working directory (`working_dir`). The runtime environment of Ray cluster is roughly based on creating an independent virtual environment ([virtualenv](https://virtualenv.pypa.io/)) for each job.

```json
{
    "pip": ["requests==2.26.0"],
    "env_vars": {"TF_WARNINGS": "none"}
}
```

## Python SDK

The function of Python SDK is similar to that of command line, except that various parameters for submitting jobs are written in Python code, and Python code is executed to submit jobs. SDK provides a client, and users call `ray.job_submission.JobSubmissionClient` on the client to pass job parameters.

```python
import time
from ray.job_submission import JobSubmissionClient, JobStatus

client = JobSubmissionClient("http://127.0.0.1:8265")
job_id = client.submit_job(
    entrypoint="python script.py",
    runtime_env={"working_dir": "./"}
)
print(job_id)

def wait_until_status(job_id, status_to_wait_for, timeout_seconds=5):
    start = time.time()
    while time.time() - start <= timeout_seconds:
        status = client.get_job_status(job_id)
        print(f"status: {status}")
        if status in status_to_wait_for:
            break
        time.sleep(1)


wait_until_status(job_id, {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED})
logs = client.get_job_logs(job_id)
print(logs)
```

[`JobSubmissionClient.submit_job()`](https://docs.ray.io/en/latest/cluster/running-applications/job-submission/doc/ray.job_submission.JobSubmissionClient.submit_job.html) will sumbit the job asynchronously. After calling this method, Ray will immediately return the job ID. If you want to check the running status of the job, you can use the `wait_until_status()` function. This function will continuously request the Ray cluster to check the current status of the job.

Similar to the command line operation, in the `submit_job()` method, you can specify the working directory of the job or the required Python package by passing in the `runtime_env` parameter. In addition, `entrypoint_num_cpus` and `entrypoint_num_gpus` are used to specify the computing resources required for the entry point (`__main()__` function).

## Ray Client

Ray client refers to using the `ray.init()` function in Python to directly specify the address of the Ray cluster: `ray.init("ray://<head-node-host>:<port>")`.

:::{note}
Note that the default client service port of the Ray cluster is 10001. If you need to use a different port, you can set it by using the `--ray-client-server-port` parameter when starting the Ray cluster head node.
:::

The client can be run on a personal computer, allowing users to interactively call the computing resources of a Ray cluster. However, it should be noted that some features of the client may not be as comprehensive as the command line tool and Python SDK. For performing complex tasks, it is recommended to use the command line or Python SDK.

`ray.init()` also accepts a `runtime_env` parameter, which is used to specify the Python package version or working directory. Like the Ray Jobs command line tool, Ray will transfer the data in the specified working directory to the Ray cluster.

If the client loses connection to the Ray cluster, all distributed objects or references created by the client will be destroyed. In the event that the client is unexpectedly disconnected from the Ray cluster, Ray will try to reconnect after 30 seconds. If the reconnection fails, Ray will destroy all related references. Users can customize the time interval for this reconnection attempt by setting the environment variable `RAY_CLIENT_RECONNECT_GRACE_PERIOD`.