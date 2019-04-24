import sys
sys.path.append("..")
import ply.yacc as yacc
import lab2.Mparser as Mparser
import lab3.TreePrinter as TreePrinter
from lab4.TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    # Below code shows how to use visitor
    if not Mparser.has_errors:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
