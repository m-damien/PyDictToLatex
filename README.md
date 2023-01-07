# PyDict To LaTeX
Make python dictionaries accessible in LaTeX. Useful to keep a LaTeX document in-sync with data but without having to edit the document every time the data changes.

This is similar to Cameron Devine's [json2latex library](https://github.com/CameronDevine/json2latex). The main difference is that the macro to access data is [*fully expandable*](https://www.overleaf.com/learn/latex/Articles/How_does_%5Cexpandafter_work%3A_The_meaning_of_expansion). This means the values retrieved from the dictionary can be used everywhere, including arguments to other macros, in conditions (e.g., to have paragraphs only showing depending on a value), and to draw tikz data visualizations.

## How to use?

Python:
```python
from pydict2latex import PyDictToLatex

dictionary = {
    "foo": "bar",
    "sub dict": {
        "a": 42,
    }
}
PyDictToLatex("mydata", dictionary).save("mydata.tex")
```

LaTeX:
```LaTeX
\input{mydata}
The value of \mydata{foo} is \mydata{sub dict}{a}.
```

Will result in a document with content `The value of bar is 42`

## Installation
```
git clone repo
cd repo
pip install .
```

## More Examples
Because the macro is fully expandable, it can be used pretty much anywhere.

For example, to conditonally show a paragraph:
```LaTeX
\ifnum\pdfstrcmp{\mydata{sub dict}{a}}{42}=0
   The variable is equal to 42
\else
   The variable is different from 42
\fi
```

to loop through the data:
```LaTeX
\foreach \x in {\mydata{a list}} {
     \x
}
```


or to draw tikz graphics:
```LaTeX
\begin{tikzpicture}
\draw[gray, thick] (\mydata{x1},\mydata{y1}) -- (\mydata{x2},\mydata{y2});
\end{tikzpicture}
```

## Variables To Dict
Two functions can help generate dictionaries from array of values.

`continuous_variables_to_dict` generates a dictionary with common descriptivie statistics from an array of numerical values:
```python
from pydict2latex import continuous_variables_to_dict

continuous_variables_to_dict([5, 1, 7, 3, 2, 8, 9, 5])
# {'values': [5, 1, 7, 3, 2, 8, 9, 5], 'min': 1, 'max': 9, 'mean': '5', 'median': '5', 'std': '2.7', 'count': 8, 'sum': 40}
```

`categorical_variables_to_dict` generates a dictionary from an array of categorical values:
```python
categorical_variables_to_dict(["cherry", "cherry", "pineapple", "apple", "cherry", "apple"])
# {'unique': 3, 'count': 6, 'descending': {'1': 'cherry', '2': 'apple', '3': 'pineapple'}, 'ascending': {'3': 'cherry', '2': 'apple', '1': 'pineapple'}, 'cherry': {'count': 3, 'percent': '50'}, 'apple': {'count': 2, 'percent': '33.3'}, 'pineapple': {'count': 1, 'percent': '16.7'}}
```


## Known Issues
- `TeX capacity exceeded` This might happen with dictionaries having large 'nodes'. Often, this can be solved by re-organizing the dictionary: 'nodes' in the dictionary tree should be kept relatively small (<15 sub-trees). This can be done by spreading the sub-trees into multiple nodes, or by having multiple dictionaries (you can \include multiple dictionaries as long as their names do not collide). No limitations for nodes containing only values (i.e., having no sub-trees), those can contain a virtually infinite number of values.
For a more technical explanation of the issue: to make the macro fully expandable, I rely on a lot of \expandafter. The issue is that, the more sub-trees in a node, the more \expandafter are needed which might exceed TeX's capacity. There are probably some optimizations that could minimize the issue, or some clever tricks to get rid of the issue. PRs are welcome.

## Credits
- Cameron Devine for [json2latex](https://github.com/CameronDevine/json2latex) which inspired this project
- Joseph Wright for the [\replicate](https://tex.stackexchange.com/a/16192) macro