# tests/test_parser.py
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexer import Lexer
from parser_ import (
    Parser, DeclaracaoVariavel, Numero, Identificador, OperacaoBinaria, 
    ComandoIf, Bloco, ComandoWhile, ComandoPrint, ComandoRead, Atribuicao, Booleano
)

class TestParser(unittest.TestCase):

    def test_declaracao_variavel(self):
        code = "int x = 10;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertIsNotNone(ast)
        self.assertEqual(len(ast.declaracoes), 1)
        
        decl = ast.declaracoes[0]
        self.assertIsInstance(decl, DeclaracaoVariavel)
        self.assertEqual(decl.tipo.type, 'INT')
        self.assertEqual(decl.nome_variavel.nome, 'x')
        self.assertIsInstance(decl.expressao, Numero)
        self.assertEqual(decl.expressao.valor, 10)

    def test_expressao_binaria_simples(self):
        code = "int result = 10 + 5;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        self.assertEqual(len(ast.declaracoes), 1)
        decl = ast.declaracoes[0]
        expr = decl.expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MAIS')
        self.assertEqual(expr.esquerda.valor, 10)
        self.assertEqual(expr.direita.valor, 5)

    def test_precedencia_operadores(self):
        code = "int result = 10 + 5 * 2;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        expr = ast.declaracoes[0].expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MAIS')
        self.assertEqual(expr.esquerda.valor, 10)

        expr_mult = expr.direita
        self.assertIsInstance(expr_mult, OperacaoBinaria)
        self.assertEqual(expr_mult.op.type, 'MULT')
        self.assertEqual(expr_mult.esquerda.valor, 5)
        self.assertEqual(expr_mult.direita.valor, 2)

    def test_expressao_com_parenteses(self):
        code = "int result = (10 + 5) * 2;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        expr = ast.declaracoes[0].expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MULT')
        self.assertEqual(expr.direita.valor, 2)

        expr_add = expr.esquerda
        self.assertIsInstance(expr_add, OperacaoBinaria)
        self.assertEqual(expr_add.op.type, 'MAIS')
        self.assertEqual(expr_add.esquerda.valor, 10)
        self.assertEqual(expr_add.direita.valor, 5)

    def test_expressao_comparacao(self):
        code = "bool result = 10 > 5;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        expr = ast.declaracoes[0].expressao
        self.assertIsInstance(expr, OperacaoBinaria)
        self.assertEqual(expr.op.type, 'MAIOR')
        self.assertEqual(expr.esquerda.valor, 10)
        self.assertEqual(expr.direita.valor, 5)

    def test_comando_if_simples(self):
        code = "if (x > 0) { int y = 1; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoIf)
        self.assertEqual(comando.condicao.op.type, 'MAIOR')
        self.assertIsInstance(comando.bloco_then, Bloco)
        self.assertEqual(len(comando.bloco_then.declaracoes), 1)

    def test_comando_if_else(self):
        code = "if (x == 0) { print(1); } else { print(0); }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoIf)
        self.assertIsNotNone(comando.bloco_else)
        self.assertIsInstance(comando.bloco_then, Bloco)
        self.assertIsInstance(comando.bloco_else, Bloco)

    def test_comando_while(self):
        code = "while (i < 10) { i = i + 1; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoWhile)
        self.assertEqual(comando.condicao.op.type, 'MENOR')
        self.assertIsInstance(comando.bloco, Bloco)

    def test_comando_print(self):
        code = "print(42);"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoPrint)
        self.assertIsInstance(comando.expressao, Numero)
        self.assertEqual(comando.expressao.valor, 42)

    def test_comando_read(self):
        code = "read(var_name);"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, ComandoRead)
        self.assertEqual(comando.nome_variavel.nome, 'var_name')

    def test_atribuicao_simples(self):
        code = "x = y + 1;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        comando = ast.declaracoes[0]
        self.assertIsInstance(comando, Atribuicao)
        self.assertEqual(comando.nome_variavel.nome, 'x')
        self.assertIsInstance(comando.expressao, OperacaoBinaria)

if __name__ == '__main__':
    unittest.main()
