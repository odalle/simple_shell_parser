# Simple Shell Parser

A simple shell parser that interprets pipeline commands and redirections such as the following:

```
foo toto > bar 2>> baz | fizz >> fuzzz << EOF | goo > gooo < gaa 2> ga | dummy
```

The parsing of a command like the previous one produces a list of the cooresponding PROCESSes (a PROCESS is a command with redirections) as follows:

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




