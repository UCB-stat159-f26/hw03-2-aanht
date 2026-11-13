# HW3: Tennis Player Cleaning and Visualization Package

**Author:** Anh Tran (UC Berkeley)  
**Course:** STAT 159 - Collaborative and Reproducible Statistical Data Science  

## About
This Python package retrieves the matches of professional tennis players over the course of their career from Tennis Abstract and generates a scatterplot visualization inspired by a New York Times article. The plot shows match outcomes against the age gap between the player and their opponents.

## Reflections
Going from mostly working in Jupyter Notebooks to writing a package was a bit confusing at first. I'm used to working interactively in Jupyter Notebooks, where we can just run a cell, print the output we want to see if your code worked. However, there are definitely flaws to this printing and checking method because just reading the output is prone to human error.

I also saw the value in automated testing. In a notebook, I would rely heavily on visual checks to see if my data looks right. Writing actual `pytest` assertions using the mock JavaScript strings gave me more confidence that my logic and how I implemented the code for handling the male vs. female data was sound without needing to constantly ping the Tennis Abstract servers. It is definitely a much more robust and professional way to ensure data integrity and computational reproducibility.

Going through this homework helped me see how efficient packages are. For example, I thought the 20-line limit on functions felt constraining at first, but it forced me to be more organize and intentional with the code I'm writing. I had to break the data cleaning pipeline into structured, step-by-step components. Having smaller, modular helper functions managed by one main public function makes the codebase vastly easier to read, maintain, and reuse. 