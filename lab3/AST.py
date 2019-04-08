class Node(object):
    pass


class Program(Node):
    def __init__(self, instructions_opt=None):
        self.instructions_opt = instructions_opt


class Instructions(Node):
    def __init__(self, list):
        self.list = list

    def addInstruction(self, value):
        self.list.append(value)


class InstructionSet(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Transpose(Node):
    def __init__(self, name):
        self.name = name


class UMinus(Node):
    def __init__(self, name):
        self.name = name


class Values(Node):
    def __init__(self, list):
        self.list = list

    def addValue(self, value):
        self.list.append(value)


class Rows(Node):
    def __init__(self, list):
        self.list = list

    def addValue(self, value):
        self.list.append(value)


class MatrixFunc(Node):
    def __init__(self, func, value):
        self.func = func
        self.value = value


class Range(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Ref(Node):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class While(Node):
    def __init__(self, assignable, instruction):
        self.assignable = assignable
        self.instruction = instruction


class For(Node):
    def __init__(self, name, range, instruction):
        self.name = name
        self.range = range
        self.instruction = instruction


class If(Node):
    def __init__(self, condition, if_expression, else_expression=None):
        self.condition = condition
        self.if_expression = if_expression
        self.else_expression = else_expression


class Error(Node):
    def __init__(self):
        pass


class Break(Node):
    def __init__(self):
        self.name = 'BREAK'


class Continue(Node):
    def __init__(self):
        self.name = 'CONTINUE'


class Print(Node):
    def __init__(self, content):
        self.content = content


class Return(Node):
    def __init__(self, content):
        self.content = content


class Args(Node):
    def __init__(self, list):
        self.list = list

    def addArg(self, arg):
        self.list.append(arg)
