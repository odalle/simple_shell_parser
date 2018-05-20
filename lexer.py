from parglare import Parser, Grammar




class PROCESS():
    """
    A Process.

    A process object is composed of two elements: a command (a programm with 
    parameters) and file redirections.

    NB: Pipe redirections are NOT part of the process object. 
    """
    def __init__(self,cmd,redirs=None):
        self._cmd = cmd
        if redirs is None: 
            redirs = REDIRS()
        self._redirs = redirs

    def __str__(self):
        return "Proc(cmd={}, redirs=[{}])".format(self._cmd,self._redirs)

    def getCommand(self):
        return self._cmd

    def getRedirs(self):
        return self._redirs

    

class CMD():
    """
    A Command.

    A command object is composed of a program name and command line arguments and
    parameters.
    """
    def __init__(self,program,args=None):
        self._program = program
        if args is None:
            args =[]
        self._args = args

    def getProgram(self):
        return self._program

    def getArgs(self):
        return self._args

    def __str__(self):
        return self._program + ' [' + ' '.join(self._args) + ']'

class REDIRS():
    """ A redirection container.

    A wrapper to the set type that prevent duplicates.
    Assumes the added items have identical hash function when they are assumed to be identical.
    """
    def __init__(self):
        self._redirs=set()

    def add(self,redir):
        self._redirs.add(redir)
        return self

    def pop(self,redir):
        return self._redirs.pop()

    def __iter__(self):
        return iter(self._redirs)

    def __str__(self):
        retval = ""
        sep = ""
        for redir in self._redirs:
            retval += sep + str(redir)
            sep=", "
        return retval

class REDIR():
    """ Base type for redirection object.

    When added to a set type container, "identical" redirections are automagically discarded
    (only the first one is kept)
    """
    def __init__(self,filespec):
        self._filespec = filespec

    def getFileSpec(self):
        return self._filespec

    def isOutput(self):
        return False

    def isInput(self):
        return False

    def isError(self):
        return False

    def __eq__(self, other):
        """ To avoid duplicates, object with same type are evalutaed as equal. """
        if isinstance(other,self.__class__):
            return True
        return False

    def __hash__(self):
        """ Prevents duplicates in sets: 
        Two redirections with same type will be mutually exclusive when added to
        a set container. """
        return self.__class__.__name__.__hash__()

    def __str__(self,extra=""):
        """ Extra flag can be used by derived class to pass extra details. """
        return "{}({}{})".format(self.__class__.__name__,self._filespec,extra)

    

class OUTREDIR(REDIR):
    """ Output redirection. (Appendable) """
    def __init__(self,filespec, append=False):
        super().__init__(filespec)
        self._append = append

    def isAppend(self):
        return self._append

    def isOutput(self):
        return True

    def __str__(self):
        extra = ""
        if self._append: 
            extra=",append=True"
        return super().__str__(extra)


class ERRREDIR(OUTREDIR):
    """ Error redirection.

        Identical to OUTREDIR, but with a different type name.
    """
    def __init__(self,filespec, append=False):
        super().__init__(filespec,append)

    def isError(self):
        return True

    def isOutput(self):
        return False

class INREDIR(REDIR):
    """ Input redirection. ("Here"-able )
    """
    def __init__(self,filespec, here=False):
        super().__init__(filespec)
        self._here = here

    def isHere(self):
        return self._here

    def isInput(self):
        return True

    def __str__(self):
        extra = ""
        if self._here: 
            extra=",here=True"
        return super().__str__(extra)


def get_parser():
    global _parser
    return _parser

## 
## Private methods not to be imported from other modules
##

_grammar = r"""
PIPELINE: PIPELINE '|' PROCESS  {left, 1}
| PROCESS ;
PROCESS: CMD REDIRS 
| CMD;
CMD: filespec ARGS
| filespec;
ARGS: arg+
| EMPTY;
REDIRS: REDIRS IN_REDIR 
| REDIRS OUT_REDIR 
| REDIRS ERR_REDIR 
| EMPTY;
IN_REDIR: '<' filespec 
| '<<' keyword;
OUT_REDIR: '>' filespec 
| OUTAPPEND_REDIR;
OUTAPPEND_REDIR: '>>' filespec;
ERR_REDIR: '2>' filespec 
| ERRAPPEND_REDIR;
ERRAPPEND_REDIR: '2>>' filespec;
space: /[\t ]+/;
arg: /([^">< ]+|"[^"]+")+/;
keyword: /\w+/;
filespec: /([^<>\| ]|\\[<]|\\>|\\\|)+/;
"""

def _onPipeAdd(_,nodes):
    return nodes[0] + [nodes[2]]
    
def _onPipeCreate(_,nodes):
    return [nodes[0]]

def _onProcessWithRedir(_,nodes):
    return PROCESS(nodes[0],nodes[1])

def _onProcessWithoutRedir(_,nodes):
    return PROCESS(nodes[0])

def _onCmdCreateWithArgs(_,nodes):
    return CMD(nodes[0],nodes[1][0])

def _onCmdCreateNoArgs(_,nodes):
    return CMD(nodes[0])

def _onArgsList(_,nodes):
    args =[]
    for i in range(0,len(nodes),2):
        args.append(nodes[i])
    return args

def _onEmptyList(_,nodes):
    return []

def _onFileSpecCreate(_,value):
    return value

def _onNewRedirs(_,nodes):
    return REDIRS()

def _onRedirsAdd(_,nodes):
    return nodes[0].add(nodes[1])

def _onOutRedir(_,value):
    return OUTREDIR(value[1])

def _onOutAppendRedir(_,value):
    return OUTREDIR(value[1],True)

def _onErrRedir(_,value):
    return ERRREDIR(value[1])

def _onErrAppendRedir(_,value):
    return ERRREDIR(value[1],True)

def _onInRedir(_,value):
    return INREDIR(value[1])

def _onHereRedir(_,value):
    return INREDIR(value[1],True)

def _forwardUpstream(_,value):
    return value[0]

_actions = {
    "PIPELINE": [
        _onPipeAdd,
        _onPipeCreate
    ],
    "PROCESS": [
        _onProcessWithRedir,
        _onProcessWithoutRedir
    ],
    "CMD": [
        _onCmdCreateWithArgs,
        _onCmdCreateNoArgs
    ],
    "ARGS": [
        _onArgsList,
        _onEmptyList
    ],
    "REDIRS": [
        _onRedirsAdd,
        _onRedirsAdd,
        _onRedirsAdd,
        _onNewRedirs
    ],
    "IN_REDIR": [
        _onInRedir,
        _onHereRedir
    ],
    "OUT_REDIR": [
        _onOutRedir,
        _forwardUpstream,
    ],
    "ERR_REDIR": [
        _onErrRedir,
        _forwardUpstream,
    ],
    "OUTAPPEND_REDIR": [
        _onOutAppendRedir
    ],
    "ERRAPPEND_REDIR": [
        _onErrAppendRedir
    ],
    "filespec": _onFileSpecCreate
}

_g = Grammar.from_string(_grammar)
_parser = Parser(_g, debug=False, actions=_actions)

if __name__ == "__main__":
    result = get_parser().parse("toto titi tata/toto >> abc/def < toto > tutu << discard| titi > abcdef 2>> errappend| truc 2> err | bidule << EOF")

    for job in result:
        print(job)