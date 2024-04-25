# Build Guide

This book is built using [Jupyter Book](https://jupyterbook.org/) and deployed on GitHub Pages. The content of this book is saved in .ipynb and .md files. Jupyter Book can convert .ipynb or .md files into HTML format.

## Style Guide for Text and Code

Please refer to the [Style Guide](style.md) for guidelines on the formatting and style of text and code.

## Cloning the Repository

Refer to the [Git Tutorial](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project) to create a Fork and clone the code repository to your local machine.

```bash
git clone https://github.com/<username>/scale-py.git
```

## Environment Setup

Prepare the environment:

* Choose a package management tool, such as `conda`.
* Install Python >= 3.8
* Install the dependencies listed in requirements.txt and requirements-web.txt. This includes tools like pandas needed for the examples in this book, as well as the Jupyter Book used to build this ebook:

```bash
conda create -n dispy
source activate dispy
conda install python=3.11 anaconda::graphviz
pip install -r requirements.txt
pip install -r requirements-web.txt
```

## Build the HTMLs

Navigate to the project folder and build the project:

```bash
sphinx-build -b html ./ ./_build/html
```

Web-related files will be generated in the `_build` directory.

## Start HTTP Server

After building the HTML files, you can use the built-in HTTP Server in Python and open http://127.0.0.1:8000 in your browser to view the result:

```bash
cd _build/html
python -m http.server 8000
```