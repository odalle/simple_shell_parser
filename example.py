import lexer as ssp

result = ssp.get_parser().parse('foo toto > bar 2>> baz | fizz >> fuzzz << EOF | goo > gooo < gaa 2> ga | dummy')

for p in result: 
    print(p)
    for redir in p.getRedirs():
        print('\t', redir, sep='', end='')
        if redir.isOutput(): print(' is:OUTPUT')
        if redir.isInput(): print(' is:INPUT')
        if redir.isError(): print(' is:ERROR')
