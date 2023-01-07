
class PyDictToLatex:
    """
    Convert a python dictionary to latex code.

    Example:
    converter = PyDictToLatex("data", {
        "foo": "bar",
        "sub dict": {
            "a": 1,
            "b": 42
        }
    })
    
    converter.save("data.tex")

    Then you can access the dictionary in your latex code using \input{data.tex} and then:
    \data{foo} #=> bar
    \data{sub dict}{b} #=> 42
    """
    def __init__(self, name, dictionary, generate_documentation=True):
        # Define a helper \@replicate function. Credit: Joseph Wright (see https://tex.stackexchange.com/a/16192) 
        self.header = '''\\makeatletter\\relax
\\long\\def\\@replicate#1{%
	\\romannumeral
	\\expandafter\\replicate@first@aux\\number#1%
	\\endcsname
}
\\long\\def\\replicate@first@aux#1{%
	\\csname replicate@first@#1\\replicate@aux
}
\\chardef\\rm@end=0 %
\\long\\expandafter\\def\\csname replicate@first@-\\endcsname
#1{\\rm@end\\NegativeReplication}
\\long\\expandafter\\def\\csname replicate@first@0\\endcsname
#1{\\rm@end}
\\long\\expandafter\\def\\csname replicate@first@1\\endcsname
#1{\\rm@end #1}
\\long\\expandafter\\def\\csname replicate@first@2\\endcsname
#1{\\rm@end #1#1}
\\long\\expandafter\\def\\csname replicate@first@3\\endcsname
#1{\\rm@end #1#1#1}
\\long\\expandafter\\def\\csname replicate@first@4\\endcsname
#1{\\rm@end #1#1#1#1}
\\long\\expandafter\\def\\csname replicate@first@5\\endcsname
#1{\\rm@end #1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@first@6\\endcsname
#1{\\rm@end #1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@first@7\\endcsname
#1{\\rm@end #1#1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@first@8\\endcsname
#1{\\rm@end #1#1#1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@first@9\\endcsname
#1{\\rm@end #1#1#1#1#1#1#1#1#1}
\\def\\replicate@aux#1{%
	\\csname replicate@#1\\replicate@aux
}
\\long\\expandafter\\def\\csname replicate@\\endcsname#1{\\endcsname}
\\long\\expandafter\\def\\csname replicate@0\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}}
\\long\\expandafter\\def\\csname replicate@1\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1}
\\long\\expandafter\\def\\csname replicate@2\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1}
\\long\\expandafter\\def\\csname replicate@3\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1}
\\long\\expandafter\\def\\csname replicate@4\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@5\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@6\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@7\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@8\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1#1#1#1#1}
\\long\\expandafter\\def\\csname replicate@9\\endcsname
#1{\\endcsname{#1#1#1#1#1#1#1#1#1#1}#1#1#1#1#1#1#1#1#1}\n''' 

        if generate_documentation:
            self.header = self.generate_doc(name, dictionary) + "\n" + self.header

        self.commands = self.dict_to_tex_cmds(name, dictionary)
        self.footer = "\n\\makeatother" # Disable @ as a function (used only to hide internal functions that should not be used by end-users)

    def generate_all_cases(self, dictionary):
        """
        Generate a list with all possible combination of parameters to access the dictionary
        """
        parameters = []
        cases = []
        for k, v in dictionary.items():
            if isinstance(v, dict):
                sub_cases = self.generate_all_cases(v)
                for sub_case in sub_cases:
                    cases.append([[k]] + sub_case)
            else:
                cases.append(parameters + [[k]])

        return cases

    def factorize_cases(self, cases, idx=0):
        """
        Factorize a list of cases (i.e., a combination of parameters to access data)
        """
        factorized_cases = []

        while len(cases) > 0:
            case = cases.pop()
            factorizable_cases = cases.copy()

            while len(factorizable_cases) > 0:
                factorizable_case = factorizable_cases.pop()

                if len(case) > idx and len(case) == len(factorizable_case) and case[idx] != factorizable_case[idx] and case[:idx] == factorizable_case[:idx] and case[idx+1:] == factorizable_case[idx+1:]:
                    case = case[:idx] + [case[idx]+factorizable_case[idx]] + case[idx+1:]
                    cases.remove(factorizable_case)


            factorized_cases.append(case)

        return factorized_cases

    def generate_doc(self, name, dictionary):
        """
        Generate a documentation to explain how to access the data by showing all possible combination of parameters
        """
        # Calculate all the possible combination and then factorize them to make the doc consise.
        factorized_cases = self.generate_all_cases(dictionary)
        depth = max(map(len, factorized_cases))

        for i in range(0, depth):
            factorized_cases = self.factorize_cases(factorized_cases, i)
                

        # Pretty print all the combinations to generate the doc
        doc = "% How to use:\n"
        for case in factorized_cases:
            line = "% \\" + name
            for attribute in case:
                line += "{" + "/".join(attribute) + "}"
        
            doc += line + "\n"

        return doc 


    def tex_strcmp(self, a, b, content_if_true):
        """
        Return the latex code to execute content_if_true if a is identical to b
        """
        return "\\ifnum\\pdfstrcmp{{{}}}{{{}}}=0 %\n{}%\n\\fi%".format(a, b, content_if_true)

    def tex_define_cmd(self, name, n_args, content):
        """
        Return the latex code to define a command name, with n_args arguments and content as its content
        """
        return "\\newcommand\\{}[{}]{{%\n{}\n}}".format(name, n_args, content)

    def dict_to_tex_cmds(self, name, dictionary):
        """
        Convert a python dictionary recursively to a list of latex commands.
        Only one command 'name' should be used, others being used internally.
        """
        leaves = []
        redirections = []
        sub_dicts = []
        n_expandafters = 1
        for key, value in dictionary.items():
            if isinstance(value, dict):
                sub_dict_name = name+"@"+("i"*(len(redirections)+1)) # Cannot use key directly as it might contain invalid characters
                sub_dicts += self.dict_to_tex_cmds(sub_dict_name, value)
                expandafters = "\\@replicate{" + str(n_expandafters) + "}{\\expandafter}"
                #TODO: Consider using nested \@replicate to avoid stack overflow (e.g., \@replicate{100}{\@replicate{100}{\expandafter}})
                n_expandafters = n_expandafters*2+1
                comparison = self.tex_strcmp("#1", key, expandafters+"\\"+sub_dict_name)
                redirections = [comparison] + redirections
            else:
                leaves.append(self.tex_strcmp("#1", key, str(value)))

        return sub_dicts + [self.tex_define_cmd(name, 1, "\n".join(leaves + redirections))]
        
    def __repr__(self):
        """
        Return the latex code corresponding to the dictionary
        """
        return self.header + "\n\n".join(self.commands) + self.footer

    def save(self, filename):
        """
        Save the latex code to a filename
        """
        with open(filename, 'w') as f:
            f.write(str(self))