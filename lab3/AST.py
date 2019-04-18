class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{}'.format(self.value)


class FloatNum(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{}'.format(self.value)


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '{}'.format(self.value)


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class Transpose(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'TRANSPOSE {}'.format(self.name)

    def accept(self, visitor):
        visitor.visit(self)


class UMinus(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '- {}'.format(self.name)


class Values(Node):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return '{}'.format(self.list)

    def addValue(self, value):
        self.list.append(value)


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return '{}'.format(self.elements)

    def addValue(self, value):
        self.elements.append(value)


class Rows(Node):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return '{}'.format(self.list)

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

    def __repr__(self):
        return '{}:{}'.format(self.left, self.right)


class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class Ref(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return '{} {}'.format(self.name, self.args)


class While(Node):
    def __init__(self, assignable, instruction):
        self.assignable = assignable
        self.instruction = instruction

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.assignable, self.instruction)


class For(Node):
    def __init__(self, name, range, instruction):
        self.name = name
        self.range = range
        self.instruction = instruction

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.name, self.range, self.instruction)


class If(Node):
    def __init__(self, condition, if_expression, else_expression=None):
        self.condition = condition
        self.if_expression = if_expression
        self.else_expression = else_expression

    def __repr__(self):
        basic = 'IF {} THEN {}'.format(self.condition, self.if_expression)
        elsePart = ' ELSE {}'.format(self.else_expression) if self.else_expression else ''

        return basic + elsePart


class Error(Node):
    pass


class Break(Node):
    def __init__(self):
        self.name = 'BREAK'

    def __repr__(self):
        return self.name


class Continue(Node):
    def __init__(self):
        self.name = 'CONTINUE'

    def __repr__(self):
        return self.name


class Print(Node):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return 'PRINT {}'.format(self.content)


class Return(Node):
    def __init__(self, content=None):
        self.content = content

    def __repr__(self):
        return 'RETURN {}'.format(self.content) if self.content else 'RETURN'


class Args(Node):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return '{}'.format(self.list)

    def addArg(self, arg):
        self.list.append(arg)


class Instructions(Node):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return '{}'.format(self.list)

    def addInstruction(self, value):
        self.list.append(value)


class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions

    def __repr__(self):
        return '{}'.format(self.instructions) if self.instructions else ''