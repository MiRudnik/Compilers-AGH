class Symbol:   # class to inherit below
    pass


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return str(self.type)


class VectorType(object):

    def __init__(self, dims, sizes, type):
        self.dims = dims
        self.sizes = sizes
        self.type = type

    def __str__(self):
        return 'vector'


class SymbolTable(object):

    def __init__(self, parent, name):   # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.variables = {}

    def put(self, name, symbol):    # put variable symbol or fundef under <name> entry
        self.variables[name] = symbol

    def get(self, name):    # get variable symbol or fundef from <name> entry
        try:
            return self.variables[name]
        except KeyError:
            if self.parent is not None:
                return self.getParentScope().get(name)
            else:
                return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent
