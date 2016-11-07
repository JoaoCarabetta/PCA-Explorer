# PCA-Explorer

This is a tool to explore [PCA (Principal Component Analysis)] (https://en.wikipedia.org/wiki/Principal_component_analysis) of surveys. 

To understand what this tool does, you have to understand what is a PCA. The PCA plots people that answered the survey by proximity of opinion. So it analyses the answer matrix of n X A dimensions, to generate a smaller dimension matrix (usually n X 2) that contains crucial information about the data. The process for a n X 3 matrix to a n x 2 matrix looks like this:

(n is the number of people, A is the number of answers)

![PCA Example](http://www.nlpca.org/fig_pca_principal_component_analysis.png)

The point of this tool is to check if a person that disagree with some people on a certain subject can have similar opinions on other topics. Essentially, it works like, 
- Select a question
- Select a person 
- See the PCA for everyone that desagrees with this selected person (with the person included)


---------

To install what is needed run

```
pip install -r requirements.txt
```
then, just 
```
python plot.py
```
The program is setted to run with [Polis](www.Pol.is) data.
