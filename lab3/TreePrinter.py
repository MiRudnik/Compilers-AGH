from __future__ import print_function
import lab3.AST as AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    ''' @DynamicAttrs - suppresses attribute warnings '''

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Error)
    def printTree(self):
        raise Exception("An error has occured!")

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("TRANSPOSE")
        self.name.printTree(indent + 1)

    @addToClass(AST.UMinus)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("-")
        self.name.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("VECTOR")
        for el in self.elements:
            el.printTree(indent + 1)

    @addToClass(AST.MatrixFunc)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.func)
        self.value.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("RANGE")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("REF")
        self.name.printTree(indent + 1)
        for item in self.args:
            item.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("WHILE")
        self.assignable.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("FOR")
        self.name.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("IF")
        self.condition.printTree(indent + 1)
        for _i in range(indent):
            print("|    ", end='')
        print("THEN")
        self.if_expression.printTree(indent + 1)
        if self.else_expression:
            for _i in range(indent):
                print("|    ", end='')
            print("ELSE")
            self.else_expression.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.name)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print(self.name)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("PRINT")
        self.content.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        for _i in range(indent):
            print("|    ", end='')
        print("RETURN")
        if self.content:
            self.content.printTree(indent + 1)

    @addToClass(AST.Args)
    def printTree(self, indent=0):
        for val in self.list:
            val.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.list:
            instruction.printTree(indent)

    @addToClass(AST.Program)
    def printTree(self):
        self.instructions.printTree()
