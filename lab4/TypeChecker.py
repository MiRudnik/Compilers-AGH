from collections import defaultdict
import lab3.AST as AST
from lab4.SymbolTable import SymbolTable, VariableSymbol, VectorType


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

# for op in standard_ops:
#     typ[op]['vector']['float'] = 'vector'
#     typ[op]['vector']['int'] = 'vector'
#     typ[op]['float']['vector'] = 'vector'
#     typ[op]['int']['vector'] = 'vector'

typ['+']['string']['string'] = 'string'

typ['\'']['vector'][None] = 'vector'
typ['-']['vector'][None] = 'vector'
typ['-']['int'][None] = 'int'
typ['-']['float'][None] = 'float'

range_types = ['int', 'float']


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

    def __init__(self):
        self.symbol_table = SymbolTable(None, 'main')
        self.nesting = 0

    def visit_Variable(self, node):
        variable_type = self.symbol_table.get(node.name)
        if variable_type is None:
            print("[Semantic Error at line {}] Unknown variable!".format(node.line))
            return ErrorType()
        return variable_type.type

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
            if all(len(vector.elements) == len(contents[0].elements) for vector in contents):
                initial_type = type(contents[0].elements[0])
                if all(all(type(x) == initial_type for x in vector.elements) for vector in contents):
                    return VectorType(2, [len(contents), len(contents[0].elements)], initial_type)
                else:
                    print("[Semantic Error at line {}] Incorrect vector types!".format(node.line))
                    return ErrorType()
            else:
                print("[Semantic Error at line {}] Incorrect vector sizes!".format(node.line))
                return ErrorType()
        else:
            # 1 dimension
            if all(type(x) == initial_type for x in contents):
                return VectorType(1, [len(contents)], initial_type)
            else:
                print("[Semantic Error at line {}] Incorrect vector types!".format(node.line))
                return ErrorType()

    def visit_Transpose(self, node):
        var_type = self.visit(node.name)
        result_type = typ['\''][str(var_type)][None]
        if result_type is not None:
            if var_type.dims != 2:
                print("[Semantic Error at line {}] Transpose only for matrices!".format(node.line))
                return ErrorType()
            var_type.sizes.reverse()
            return result_type
        else:
            print("[Semantic Error at line {}] Incorrect type for transpose!".format(node.line))
            return ErrorType()

    def visit_UMinus(self, node):
        var_type = self.visit(node.name)
        result_type = typ['-'][str(var_type)][None]
        if result_type is not None:
            return result_type
        else:
            print("[Semantic Error at line {}] Incorrect type for uminus!".format(node.line))
            return ErrorType()

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        operand = node.op
        if isinstance(type1, ErrorType) or isinstance(type2, ErrorType):
            return ErrorType()
        result_type = typ[operand][str(type1)][str(type2)]
        if result_type is not None:
            if result_type == 'vector':
                if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                    if type1.sizes != type2.sizes or type1.type != type2.type:
                        print("[Semantic Error at line {}] Different sizes of operands!".format(node.line))
                        return ErrorType()
                    else:
                        result_type = type1
            return result_type
        else:
            print("[Semantic Error at line {}] Incorrect types of operands!".format(node.line))
            return ErrorType()

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        operand = node.op
        if isinstance(type1, ErrorType) or isinstance(type2, ErrorType):
            return ErrorType()
        result_type = typ[operand][str(type1)][str(type2)]
        if result_type is not None:
            return result_type
        else:
            print("[Semantic Error at line {}] Incorrect types of operands!".format(node.line))
            return ErrorType()

    def visit_MatrixFunc(self, node):
        if len(node.args) != 1:
            print("[Semantic Error at line {}] Function takes only one parameter!".format(node.line))
            return ErrorType()
        type = self.visit(node.args[0])
        if type == 'int':
            value = 3   # we cant evaluate expressions while only checking types
            if isinstance(node.args[0], AST.IntNum):
                value = node.args[0].value
            return VectorType(2, [value, value], 'int')
        else:
            print("[Semantic Error at line {}] Supporting only integers in matrix functions!".format(node.line))
            return ErrorType()

    def visit_Range(self, node):
        type = self.visit(node.left)
        if isinstance(type, ErrorType) or type not in range_types:
            print("[Semantic Error at line {}] Incorrect range expression type!".format(node.line))
            return ErrorType()
        type = self.visit(node.right)
        if isinstance(type, ErrorType) or type not in range_types:
            print("[Semantic Error at line {}] Incorrect range expression type!".format(node.line))
            return ErrorType()
        return type

    def visit_Assign(self, node):
        type2 = self.visit(node.right)
        operand = node.op
        if isinstance(type2, ErrorType):
            return ErrorType()
        if operand == '=':
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.name, type2))
            node.left = node.right
        if operand in assign_ops:
            type1 = self.visit(node.left)
            result_type = typ[operand][str(type1)][str(type2)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                        if type1.sizes != type2.sizes or type1.type != type2.type:
                            print("[Semantic Error at line {}] Different sizes of operands!".format(node.line))
                            return ErrorType()
                        else:
                            result_type = type1
                return result_type
            else:
                print("[Semantic Error at line {}] Incorrect types of operands!".format(node.line))
                return ErrorType()

    def visit_Ref(self, node):
        if len(node.args) > 2:
            print("[Semantic Error at line {}] Too many dimensions provided!".format(node.line))
            return ErrorType()
        var_type = self.visit(node.name)
        if str(var_type) != 'vector':
            print("[Semantic Error at line {}] Variable not a vector!".format(node.line))
            return ErrorType()
        types = [self.visit(x) for x in node.args]
        if len(types) == 1:
            # vector
            if types == ['int']:
                value = 0  # we cant evaluate expressions while only checking types
                if isinstance(node.args[0], AST.IntNum):
                    value = node.args[0].value
                if var_type.dims != 1:
                    print("[Semantic Error at line {}] Vector has different dimensions!".format(node.line))
                    return ErrorType()
                if value >= var_type.sizes[0] or value < 0:
                    print("[Semantic Error at line {}] Index out of bounds!".format(node.line))
                    return ErrorType()
                return var_type.type
            else:
                print("[Semantic Error at line {}] Reference only supports integer parameters!".format(node.line))
                return ErrorType()
        else:
            # matrix
            if types == ['int', 'int']:
                value = [0, 0]  # we cant evaluate expressions while only checking types
                if isinstance(node.args[0], AST.IntNum) and isinstance(node.args[1], AST.IntNum):
                    value[0] = node.args[0].value
                    value[1] = node.args[1].value
                if var_type.dims != 2:
                    print("[Semantic Error at line {}] Vector has different dimensions!".format(node.line))
                    return ErrorType()
                if value[0] >= var_type.sizes[0] or value[1] >= var_type.sizes[1]:
                    print("[Semantic Error at line {}] Index out of bounds!".format(node.line))
                    return ErrorType()
                return var_type.type
            else:
                print("[Semantic Error at line {}] Reference only supports integer parameters!".format(node.line))
                return ErrorType()

    def visit_While(self, node):
        self.nesting += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.assignable)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()
        self.nesting -= 1

    def visit_For(self, node):
        self.nesting += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        type = self.visit(node.range)
        self.symbol_table.put(node.name, VariableSymbol(node.name, type))
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()
        self.nesting -= 1

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table.pushScope('if')
        self.visit(node.if_expression)
        self.symbol_table.popScope()
        if node.else_expression is not None:
            self.symbol_table.pushScope('else')
            self.visit(node.else_expression)
            self.symbol_table.popScope()

    def visit_Break(self, node):
        if self.nesting <= 0:
            print("[Semantic Error at line {}] Break outside loop statement!".format(node.line))

    def visit_Continue(self, node):
        if self.nesting <= 0:
            print("[Semantic Error at line {}] Continue outside loop statement!".format(node.line))

    def visit_Print(self, node):
        self.visit(node.content)

    def visit_Return(self, node):
        if node.content is not None:
            self.visit(node.content)

    def visit_Args(self, node):
        for arg in node.list:
            self.visit(arg)

    def visit_Instructions(self, node):
        for instruction in node.list:
            self.visit(instruction)

    def visit_Program(self, node):
        self.visit(node.instructions)
