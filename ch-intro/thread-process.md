(thread-process)=
# Threads and Processes

CPUs, GPUs, NICs, etc., are all hardware concepts. At the software level, threads and processes are often used to describe the execution process of a program.

## Processes and Threads

CPUs, GPUs, NICs, etc., are managed by the operating system (OS). The operating system manages the hardware and provides services to users through various applications. The running software is called a process. For example, when browsing web pages using a browser on a personal laptop, the operating system creates a process for the browser; when writing text content using the Word text editing software, the operating system creates a Word process. The Activity Monitor on macOS (as shown in {numref}`mac-process`) and the Task Manager on Windows can display the currently running processes of the operating system and the resources, such as CPU and memory, occupied by each process.

```{figure} ../img/ch-intro/mac-process.png
---
width: 600px
name: mac-process
---
The Activity Monitor on macOS
```
The operating system manages the execution of all processes and allocates resources to them. Specifically, the operating system allocates main memory space to processes, and each process has its own address space, data stack, and so on.

In most programming languages, a process contains multiple threads, as shown in {numref}`process-thread`. Each thread runs on a physical computing core, and multiple threads of a process can utilize multiple physical computing cores.

```{figure} ../img/ch-intro/process-thread.svg
---
width: 500px
name: process-thread
---
Processes and Threads
```

From {numref}`process-thread`, it can be seen that a process has multiple concurrent execution threads. Multiple threads share the same context (data, files, etc.), making data sharing and communication between threads easier.

Processes are isolated from each other. If multiple processes need to exchange data, they must use inter-process communication (IPC) mechanisms to achieve data sharing, such as shared memory (`multiprocessing.shared_memory`) or the message passing interface (MPI) that will be discussed in {numref}`mpi-intro`.

## Thread Safety

Since multiple threads share the same context (data, files, etc.), accessing the same data from different threads can easily lead to thread safety issues. Taking this code as an example:

```
x = x + 1
x = x * 2
x = x - 1
```

If these three operations are scheduled on three threads, the data `x` is shared by the three threads, and the execution order of the three threads will significantly affect the calculation results. {numref}`thread-safe` shows three different possible execution orders, and the calculation results of the three orders may be different. Different scheduling orders can lead to unexpected results in parallel computing, which is thread-unsafe.

```{figure} ../img/ch-intro/thread-safe.svg
---
width: 600px
name: thread-safe
---
Thread Safety
```

The simplest way to solve thread safety is to use locks. As shown in {numref}`thread-lock`, for shared data, each thread acquires a lock before modifying it and releases the lock after modification.

```{figure} ../img/ch-intro/thread-lock.svg
---
width: 500px
name: thread-lock
---
Thread Lock
```

## Global Interpreter Lock

The CPython interpreter employs a radical approach to address thread safety: the Global Interpreter Lock (GIL).

:::{note} 
CPython is one of the implementations of the Python interpreter and is the most widely used one. CPython is implemented in C. The Python installed via Anaconda is CPython.

In addition to CPython, there are Jython, which is implemented in Java, and IronPython, which is implemented in C#. 
:::

The GIL in CPython allows only one thread to run in a Python process. Under the GIL, a Python process can only have one thread running and can only utilize one CPU core. One advantage of the GIL is thread safety, but the disadvantages are also apparent. On modern multi-core computers, Python and many libraries, such as NumPy, pandas, and scikit-learn, can only utilize one core.

The GIL is closely tied to the entire Python ecosystem. It is closely related to libraries like NumPy and pandas. Removing the GIL can have far-reaching impacts. Therefore, it is not easy to fully utilize the multiple cores of modern computers with Python. Fortunately, the Python community is actively working on this issue, and in the near future, the GIL will be removed from CPython.