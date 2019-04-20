from collections import defaultdict
import lab3.AST as AST
from lab4.SymbolTable import VariableSymbol, VectorSymbol


typ = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
standard_ops = ['+', '-', '*', '/']
matrix_ops = ['.+', '.-', '.*', './']
relation_ops = ['<', '>', '>=', '<=', '==', '!=']
assign_ops = ['+=', '-=', '*=', '/=']

for op in standard_ops + assign_ops:
    typ[op]['int']['float'] = 'float'
    typ[op]['float']['int'] = 'float'
    typ[op]['float']['float'] = 'float'
    typ[op]['int']['int'] = 'int'
    typ[op]['vector']['vector'] = 'vector'

for op in matrix_ops:
    typ[op]['vector']['vector'] = 'vector'

for op in relation_ops:
    typ[op]['int']['float'] = 'float'
    typ[op]['float']['int'] = 'float'
    typ[op]['float']['float'] = 'float'
    typ[op]['int']['int'] = 'int'
    typ[op]['vector']['vector'] = 'vector'

for op in standard_ops:
    typ[op]['vector']['float'] = 'vector'
    typ[op]['vector']['int'] = 'vector'
    typ[op]['float']['vector'] = 'vector'
    typ[op]['int']['vector'] = 'vector'

typ['+']['string']['string'] = 'string'


class ErrorType:

    def __str__(self):
        return 'ErrorType'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    # TODO get line number to print somehow

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Vector(self, node):
        contents = node.elements
        initial_type = type(contents[0])
        if initial_type == AST.Vector:
            # 2 dimensions
            if all(len(x) == len(contents[0]) for x in contents):
                initial_type = type(contents[0][0])
                if all(all(type(x) == initial_type for x in vector) for vector in contents):
                    return VectorSymbol(2, [len(contents[0]), len(contents)], initial_type)
                else:
                    print("[Semantic Error] Incorrect vector types!")
                    return ErrorType()
            else:
                print("[Semantic Error] Incorrect vector sizes!")
                return ErrorType()
        else:
            # 1 dimension
            if all(type(x) == initial_type for x in contents):
                return VectorSymbol(1, [len(contents)], initial_type)
            else:
                print("[Semantic Error] Incorrect vector types!")
                return ErrorType()

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        operand = node.op
        if type1 == ErrorType or type2 == ErrorType:
            return ErrorType()
        result_type = typ[operand][type1][type2]
        if result_type is not None:
            return result_type
        else:
            print("[Semantic Error] Incorrect types of operands!")
            return ErrorType()

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        operand = node.op
        if type1 == ErrorType or type2 == ErrorType:
            return ErrorType()
        result_type = typ[operand][type1][type2]
        if result_type is not None:
            return result_type
        else:
            print("[Semantic Error] Incorrect types of operands!")
            return ErrorType()

    # TODO finish
