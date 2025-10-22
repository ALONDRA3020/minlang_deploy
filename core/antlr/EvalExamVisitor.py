from .MiniLangVisitor import MiniLangVisitor
from .MiniLangParser import MiniLangParser

class EvalExamVisitor(MiniLangVisitor):
    def _init_(self):
        super()._init_()
        self.memory = {}

    def visitProgram(self, ctx: MiniLangParser.ProgramContext):
        result = None
        for st in ctx.statement():
            result = self.visit(st)
        return result

    def visitStatement(self, ctx: MiniLangParser.StatementContext):
        if ctx.assign():
            return self.visit(ctx.assign())
        elif ctx.print():
            return self.visit(ctx.print())
        return None

    def visitAssign(self, ctx: MiniLangParser.AssignContext):
        var_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[var_name] = value
        return value

    def visitPrint(self, ctx: MiniLangParser.PrintContext):
        value = self.visit(ctx.expr())
        print(value)
        return value

    def visitExpr(self, ctx: MiniLangParser.ExprContext):
        # Si tiene operador (*, /, +, -)
        if ctx.op:
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            if ctx.op.text == '*':
                return left * right
            elif ctx.op.text == '/':
                if right == 0:
                    raise ValueError("División por cero")
                return left / right
            elif ctx.op.text == '+':
                return left + right
            elif ctx.op.text == '-':
                return left - right

        # Si es un número entero
        if ctx.INT():
            return int(ctx.INT().getText())

        # Si es una variable
        if ctx.ID():
            var_name = ctx.ID().getText()
            if var_name not in self.memory:
                raise NameError(f"Variable '{var_name}' no definida")
            return self.memory[var_name]

        # Si tiene paréntesis
        if len(ctx.expr()) == 1:
            return self.visit(ctx.expr(0))

        return None