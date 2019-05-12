class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)


class IntNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __repr__(self):
        return '{}'.format(self.value)


class FloatNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __repr__(self):
        return '{}'.format(self.value)


class String(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def __repr__(self):
        return '{}'.format(self.value)


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return '{}'.format(self.name)


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class RelExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class Transpose(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return 'TRANSPOSE {}'.format(self.name)


class UMinus(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __repr__(self):
        return '- {}'.format(self.name)


class Vector(Node):
    def __init__(self, elements, line):
        self.elements = elements
        self.line = line

    def __repr__(self):
        return '{}'.format(self.elements)

    def addValue(self, value):
        self.elements.append(value)


class MatrixFunc(Node):
    def __init__(self, func, args, line):
        self.func = func
        self.args = args
        self.line = line


class Range(Node):
    def __init__(self, left, right, line):
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return '{}:{}'.format(self.left, self.right)


class Assign(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)


class Ref(Node):
    def __init__(self, name, args, line):
        self.name = name
        self.args = args
        self.line = line

    def __repr__(self):
        return '{} {}'.format(self.name, self.args)


class While(Node):
    def __init__(self, assignable, instruction, line):
        self.assignable = assignable
        self.instruction = instruction
        self.line = line

    def __repr__(self):
        return 'WHILE {} DO {}'.format(self.assignable, self.instruction)


class For(Node):
    def __init__(self, variable, range, instruction, line):
        self.variable = variable
        self.range = range
        self.instruction = instruction
        self.line = line

    def __repr__(self):
        return 'FOR {} IN {} DO {}'.format(self.variable, self.range, self.instruction)


class If(Node):
    def __init__(self, condition, if_expression, line, else_expression=None):
        self.condition = condition
        self.if_expression = if_expression
        self.else_expression = else_expression
        self.line = line

    def __repr__(self):
        basic = 'IF {} THEN {}'.format(self.condition, self.if_expression)
        elsePart = ' ELSE {}'.format(self.else_expression) if self.else_expression else ''

        return basic + elsePart


class Error(Node):
    pass


class Break(Node):
    def __init__(self, line):
        self.name = 'BREAK'
        self.line = line

    def __repr__(self):
        return self.name


class Continue(Node):
    def __init__(self, line):
        self.name = 'CONTINUE'
        self.line = line

    def __repr__(self):
        return self.name


class Print(Node):
    def __init__(self, content, line):
        self.content = content
        self.line = line

    def __repr__(self):
        return 'PRINT {}'.format(self.content)


class Return(Node):
    def __init__(self, line, content=None):
        self.content = content
        self.line = line

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

    def accept(self, visitor):
        visitor.visit(self)


class Program(Node):
    def __init__(self, instructions=None):
        self.instructions = instructions

    def __repr__(self):
        return '{}'.format(self.instructions) if self.instructions else ''

    def accept(self, visitor):
        visitor.visit(self)