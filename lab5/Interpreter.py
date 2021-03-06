import lab3.AST as AST
from lab4.SymbolTable import *
from lab5.Memory import *
from lab5.Exceptions import  *
from lab5.visit import *
import sys
import numpy

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

matrixExprOp = {
    '+': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '+=': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '.+': (lambda x, y: (numpy.matrix(x) + numpy.matrix(y)).tolist()),
    '-': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '-=': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '.-': (lambda x, y: (numpy.matrix(x) - numpy.matrix(y)).tolist()),
    '*': (lambda x, y: numpy.array(numpy.matmul(x, y)).tolist()),
    '*=': (lambda x, y: numpy.array(numpy.matmul(x, y)).tolist()),
    '.*': (lambda x, y: numpy.multiply(numpy.array(x), numpy.array(y)).tolist()),
    './': (lambda x, y: numpy.divide(numpy.array(x), numpy.array(y)).tolist()),
}


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
        else:
            return matrixExprOp[node.op](left, right)

    @when(AST.RelExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return relExprOp[node.op](r1, r2)

    @when(AST.Transpose)
    def visit(self, node):
        matrix = numpy.array(self.memoryStack.get(node.name.name))
        return matrix.transpose().tolist()

    @when(AST.UMinus)
    def visit(self, node):
        return - node.name.accept(self)

    @when(AST.Vector)
    def visit(self, node):
        return [element.accept(self) for element in node.elements]

    @when(AST.MatrixFunc)
    def visit(self, node):
        arg = node.args[0].accept(self)

        if node.func == "zeros":
            return [[0 for _ in range(arg)] for _ in range(arg)]
        elif node.func == "ones":
            return [[1 for _ in range(arg)] for _ in range(arg)]
        elif node.func == "eye":
            eye = [[0 for _ in range(arg)] for _ in range(arg)]
            for i in range(0, arg):
                eye[i][i] = 1
            return eye

    @when(AST.Range)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        return left, right

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
                    result = matrixExprOp[node.op](left, right)

                self.memoryStack.set(node.left.name, result)
            elif isinstance(node.left, AST.Ref):
                matrix = self.memoryStack.get(node.left.name.name)
                args = node.left.args
                left = None

                if len(args) == 1:
                    left = matrix[args[0].accept(self)]
                elif len(args) == 2:
                    left = matrix[args[0].accept(self)][args[1].accept(self)]

                result = None

                if type(left) is not list and type(right) is not list:
                    result = binExprOp[node.op](left, right)

                if len(args) == 1:
                    arg = args[0].accept(self)
                    matrix[arg] = result
                elif len(args) == 2:
                    leftArg = args[0].accept(self)
                    rightArg = args[1].accept(self)
                    matrix[leftArg][rightArg] = result

    @when(AST.Ref)
    def visit(self, node):
        matrix = self.memoryStack.get(node.name.name)
        args = node.args

        if len(args) == 1:
            return matrix[args[0].accept(self)]
        elif len(args) == 2:
            return matrix[args[0].accept(self)][args[1].accept(self)]

    @when(AST.While)
    def visit(self, node):
        while node.assignable.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.For)
    def visit(self, node):
        range = node.range.accept(self)

        if self.memoryStack.get(node.variable.name) is None:
            self.memoryStack.insert(node.variable.name, range[0])
        else:
            self.memoryStack.set(node.variable.name, range[0])

        while self.memoryStack.get(node.variable.name) <= range[1]:
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

            iterator = self.memoryStack.get(node.variable.name) + 1
            self.memoryStack.set(node.variable.name, iterator)

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
        print(*node.content.accept(self), sep=", ")

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

