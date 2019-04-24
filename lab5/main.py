import sys
import ply.yacc as yacc
import lab2.Mparser as Mparser
import lab3.TreePrinter as TreePrinter
from lab4.TypeChecker import TypeChecker
from lab5.Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "../lab4/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    result = typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    if result is None:
        ast.accept(Interpreter())
        # in future
        # ast.accept(OptimizationPass1())
        # ast.accept(OptimizationPass2())
        # ast.accept(CodeGenerator())