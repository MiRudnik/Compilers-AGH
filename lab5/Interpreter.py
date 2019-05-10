import lab3.AST as AST
from lab4.SymbolTable import *
from lab5.Memory import *
from lab5.Exceptions import  *
from lab5.visit import *
import sys

sys.setrecursionlimit(10000)

binExprOp = {
    "+": (lambda x, y: x + y),
    "+=": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "-=": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "*=": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
    "/=": (lambda x, y: x / y),
}

matrixExprOp = {}

relExprOp = {
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
    ">": (lambda x, y: x > y),
    "<": (lambda x, y: x < y),
    "<=": (lambda x, y: x <= y),
    ">=": (lambda x, y: x >= y)
}

assign_ops = ['+=', '-=', '*=', '/=']

class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if type(left) is not list and type(right) is not list:
            return binExprOp[node.op](left, right)

    @when(AST.RelExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return relExprOp[node.op](r1, r2)

    @when(AST.Vector)
    def visit(self, node):
        return [element.accept(self) for element in node.elements]

    @when(AST.Range)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        return (left, right)

    @when(AST.Assign)
    def visit(self, node):
        right = node.right.accept(self)

        if node.op == '=':
            if isinstance(node.left, AST.Variable):
                if self.memoryStack.get(node.left.name) is None:
                    self.memoryStack.insert(node.left.name, right)
                else:
                    self.memoryStack.set(node.left.name, right)
            elif isinstance(node.left, AST.Ref):
                matrix = self.memoryStack.get(node.left.name.name)
                args = node.left.args

                if len(args) == 1:
                    arg = args[0].accept(self)
                    matrix[arg] = right
                elif len(args) == 2:
                    leftArg = args[0].accept(self)
                    rightArg = args[1].accept(self)
                    matrix[leftArg][rightArg] = right
        if node.op in assign_ops:
            if isinstance(node.left, AST.Variable):
                left = self.memoryStack.get(node.left.name)
                result = None

                if type(left) is not list and type(right) is not list:
                    result = binExprOp[node.op](left, right)
                elif type(left) is list and type(right) is list:
                    result = matrix[node.op](left, right)

                self.memoryStack.set(node.left.name, result)
            elif isinstance(node.left, AST.Ref):
                matrix = self.memoryStack.get(node.left.name)
                args = node.left.args.accept(self)
                left = None

                if len(args) == 1:
                    left = matrix[args[0]]
                elif len(args) == 2:
                    left = matrix[args[0]][args[1]]

    @when(AST.Ref)
    def visit(self, node):
        matrix = self.memoryStack.get(node.name)
        args = node.args.accept(self)

        if len(args) == 1:
            return matrix[args[0]]
        elif len(args) == 2:
            return matrix[args[0]][args[1]]

    @when(AST.While)
    def visit(self, node):
        while node.assignable.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            return node.if_expression.accept(self)
        else:
            if node.else_expression is not None:
                return node.else_expression.accept(self)
            else:
                pass

    @when(AST.Error)
    def visit(self, node):
        pass

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Print)
    def visit(self, node):
        print(str(node.content.accept(self)))

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.content.accept(self))

    @when(AST.Args)
    def visit(self, node):
        return [arg.accept(self) for arg in node.list]

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.list:
            instruction.accept(self)

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

