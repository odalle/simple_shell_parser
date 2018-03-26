# Simple Shell Parser

A simple shell parser in pure Python that interprets shell pipelined commands and redirections such as the following:

```
foo toto > bar 2>> baz | fizz >> fuzzz << EOF | goo > gooo < gaa 2> ga | dummy
```

This parser is meant for educational purpose and, therefore, should not be relied on for advanced projects.
It is built using the very nice [https://github.com/igordejanovic/parglare](parglare) python parser.


The parsing of a command like the previous one produces a simple Abstract Syntax Tree: a collection of objects that reflect the syntax structure of the line being parsed.

At the root level, we find the object associated to the whole line, the pipeline. It is a simple python List.
The list elements are intances of the PROCESS class defined in the parser module. Each process owns attributes for the arguments and redirections. They can also be displayed using an explicit string representation as follows:

```python
import simple_shell_parser.lexer as ssp

result = ssp.get_parser().parse('foo toto > bar 2>> baz | fizz >> fuzzz << EOF | goo > gooo < gaa 2> ga | dummy')

for p in result: print(p)
```

which produces the following output:

```
Proc(cmd=foo [toto], redirs=[OUTREDIR(bar), ERRREDIR(baz,append=True)])
Proc(cmd=fizz [], redirs=[INREDIR(EOF,here=True), OUTREDIR(fuzzz,append=True)])
Proc(cmd=goo [], redirs=[INREDIR(gaa), OUTREDIR(gooo), ERRREDIR(ga)])
Proc(cmd=dummy [], redirs=[])
```

All elements displayed in the previous output are objects of the following classes:
* PROCESS
* CMD
* REDIR (INREDIR, OUTREDIR, ERREDIR)

The pipeline is list of PROCESS objects and the command args are also a list object attribute of the CMD class.

See the `lexer.py` source code or the python doc for more details ...

## INSTALL

This python module is available through [https://pypi.org/](PyPi) using the following command:

```
pip install simple-shell-parser
```




