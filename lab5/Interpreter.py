import lab3.AST as AST
from lab4.SymbolTable import *
from lab5.Memory import *
from lab5.Exceptions import  *
from lab5.visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assign)
    def visit(self, node):
        pass

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
