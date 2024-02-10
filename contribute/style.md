# Style Guide

To ensure consistency throughout this tutorial, please follow this style guide when writing the tutorial and submit a Pull Request.

## Files

When you create a new document, please store your file in the correct location.

- Location: Store all documents in the ch-xxx/ directory, where ch is the abbreviation for chapter. Create a directory for each chapter and a .md or .ipynb file for each section.

- Image: Save drawing files in the drawio folder of the project and SVG images in the img folder. Place the images into the corresponding folder.

- Name: Directory and file names should be concise and intuitive, using hyphens (-) as separators and lowercase letters.
    > Example: python-ecosystem.svg 
    > Example: ch-mpi

## Text

This tutorial is aimed at beginners, so please keep the writing style concise and easy to understand. Any markings that help readers understand the text are helpful.

- For the first occurrence of an abbreviation, provide the full form. The abbreviation can be used in subsequent text.
    > Example: API (Application Programming Interface)

## Code

Please make your code as readable as possible. For Python code writing conventions, you can refer to [The Black Code Styles](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html). Here are some specific scenarios:

- Variables should use meaningful English words.

- Variables should have meaningful names to maintain readability. It is recommended to avoid using variables named a, b, c. You can use counters like i, j.

- Function names should use underscore-style naming in lowercase.
    > Example: hello_world()

- Class names should be capitalized, and complex class names should use camel case.
    > Example: class HelloWorld

- Images. It is recommended to use the software [drawio](https://www.drawio.com/) to draw images. Drawio can also be used online. Save the .drawio files in the `drawio` folder of the project and SVG images in the `img` folder.