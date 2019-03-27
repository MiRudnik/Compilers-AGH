class Node(object):
    pass


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


class Error(Node):
    def __init__(self):
        pass
