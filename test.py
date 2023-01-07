from pydict2latex import PyDictToLatex, categorical_variables_to_dict, continuous_variables_to_dict

dictionary = {
    "foo": "bar",
    "continuous": continuous_variables_to_dict([0, 1, 2, 4, 2, 1, 0], bins=[0, 1, 2, 3, 4, 5]),
    "categorical": categorical_variables_to_dict(["cherry", "cherry", "pineapple", "apple", "cherry", "apple"]),
    "sub dict": {
        "a": 42,
        "subsub dict": {
            "1": {'a': 1},
        }
    }
}

print(dictionary)

PyDictToLatex("mydata", dictionary).save("mydata.tex")