import sys
sys.path.append("..")
import lab2.Mparser as Mparser
from lab4.TypeChecker import TypeChecker
from lab5.Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner.lexer)

    if not Mparser.has_errors:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
        if not typeChecker.has_errors:
            ast.accept(Interpreter())
            # ast.accept(OptimizationPass1())
            # ast.accept(OptimizationPass2())
            # ast.accept(CodeGenerator())
        else:
            print("File has semantic errors!")
    else:
        print("File has syntax errors!")
