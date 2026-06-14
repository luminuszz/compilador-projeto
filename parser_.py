from lexer import Token

class ASTNode:
    """Nó base para todos os nós da AST."""
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

class Programa(ASTNode):
    def __init__(self, declaracoes):
        self.declaracoes = declaracoes

class DeclaracaoVariavel(ASTNode):
    def __init__(self, tipo, nome_variavel, expressao):
        self.tipo = tipo
        self.nome_variavel = nome_variavel
        self.expressao = expressao

class Atribuicao(ASTNode):
    def __init__(self, nome_variavel, expressao):
        self.nome_variavel = nome_variavel
        self.expressao = expressao

class ComandoPrint(ASTNode):
    def __init__(self, expressao):
        self.expressao = expressao

class ComandoRead(ASTNode):
    def __init__(self, nome_variavel):
        self.nome_variavel = nome_variavel

class OperacaoBinaria(ASTNode):
    def __init__(self, esquerda, op, direita):
        self.esquerda = esquerda
        self.op = op
        self.direita = direita

class Numero(ASTNode):
    def __init__(self, token: Token):
        self.token = token
        self.valor = int(token.value)

class Booleano(ASTNode):
    def __init__(self, token: Token):
        self.token = token
        self.valor = (token.type == 'TRUE')

class Identificador(ASTNode):
    def __init__(self, token: Token):
        self.token = token
        self.nome = token.value

class Bloco(ASTNode):
    def __init__(self, declaracoes):
        self.declaracoes = declaracoes

class ComandoIf(ASTNode):
    def __init__(self, condicao, bloco_then, bloco_else=None):
        self.condicao = condicao
        self.bloco_then = bloco_then
        self.bloco_else = bloco_else

class ComandoWhile(ASTNode):
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        if not tokens:
            raise ParserError("A lista de tokens não pode estar vazia.")
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def _avancar(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.token_atual = self.tokens[self.pos]

    def _consumir(self, tipo_esperado):
        if self.token_atual.type == tipo_esperado:
            token_consumido = self.token_atual
            self._avancar()
            return token_consumido
        else:
            raise ParserError(f"Erro de sintaxe: Esperado '{tipo_esperado}', mas encontrou '{self.token_atual.type}' na linha {self.token_atual.line}")

    def parse(self):
        return self.programa()

    def programa(self):
        declaracoes = []
        while self.token_atual.type != 'EOF':
            declaracoes.append(self.statement())
        return Programa(declaracoes)

    def statement(self):
        if self.token_atual.type in ('INT', 'BOOL'):
            return self.declaracao_variavel()
        elif self.token_atual.type == 'IF':
            return self.comando_if()
        elif self.token_atual.type == 'WHILE':
            return self.comando_while()
        elif self.token_atual.type == 'PRINT':
            return self.comando_print()
        elif self.token_atual.type == 'READ':
            return self.comando_read()
        elif self.token_atual.type == 'IDENTIFICADOR':
            return self.atribuicao()
        elif self.token_atual.type == 'LCHAVE':
            return self.comando_bloco()
        else:
            raise ParserError(f"Comando ou declaração inesperado(a): {self.token_atual.type} na linha {self.token_atual.line}")

    def comando_print(self):
        self._consumir('PRINT')
        self._consumir('LPAREN')
        expr = self.expressao()
        self._consumir('RPAREN')
        self._consumir('PONTO_VIRGULA')
        return ComandoPrint(expr)

    def comando_read(self):
        self._consumir('READ')
        self._consumir('LPAREN')
        id_node = self.identificador()
        self._consumir('RPAREN')
        self._consumir('PONTO_VIRGULA')
        return ComandoRead(id_node)

    def atribuicao(self):
        id_node = self.identificador()
        self._consumir('IGUAL')
        expr = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return Atribuicao(id_node, expr)

    def comando_while(self):
        self._consumir('WHILE')
        self._consumir('LPAREN')
        condicao = self.expressao()
        self._consumir('RPAREN')
        bloco = self.statement()
        return ComandoWhile(condicao, bloco)

    def comando_if(self):
        self._consumir('IF')
        self._consumir('LPAREN')
        condicao = self.expressao()
        self._consumir('RPAREN')
        bloco_then = self.statement()
        
        bloco_else = None
        if self.token_atual.type == 'ELSE':
            self._consumir('ELSE')
            bloco_else = self.statement()
            
        return ComandoIf(condicao, bloco_then, bloco_else)

    def comando_bloco(self):
        self._consumir('LCHAVE')
        declaracoes = []
        while self.token_atual.type != 'RCHAVE' and self.token_atual.type != 'EOF':
            declaracoes.append(self.statement())
        self._consumir('RCHAVE')
        return Bloco(declaracoes)
        
    def declaracao_variavel(self):
        tipo = self._consumir(self.token_atual.type)
        nome_variavel = self.identificador()
        expressao = None
        if self.token_atual.type == 'IGUAL':
            self._consumir('IGUAL')
            expressao = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return DeclaracaoVariavel(tipo=tipo, nome_variavel=nome_variavel, expressao=expressao)

    def expressao(self):
        return self.igualdade()

    def igualdade(self):
        node = self.comparacao()
        while self.token_atual.type in ('DIFERENTE', 'IGUAL_COMP'):
            op = self.token_atual
            self._consumir(op.type)
            direita = self.comparacao()
            node = OperacaoBinaria(esquerda=node, op=op, direita=direita)
        return node

    def comparacao(self):
        node = self.termo()
        while self.token_atual.type in ('MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL'):
            op = self.token_atual
            self._consumir(op.type)
            direita = self.termo()
            node = OperacaoBinaria(esquerda=node, op=op, direita=direita)
        return node

    def termo(self):
        node = self.fator()
        while self.token_atual.type in ('MAIS', 'MENOS'):
            op = self.token_atual
            self._consumir(op.type)
            direita = self.fator()
            node = OperacaoBinaria(esquerda=node, op=op, direita=direita)
        return node

    def fator(self):
        node = self.unario()
        while self.token_atual.type in ('MULT', 'DIV'):
            op = self.token_atual
            self._consumir(op.type)
            direita = self.unario()
            node = OperacaoBinaria(esquerda=node, op=op, direita=direita)
        return node
    
    def unario(self):
        return self.primario()

    def primario(self):
        token = self.token_atual
        if token.type == 'NUMERO':
            self._consumir('NUMERO')
            return Numero(token)
        elif token.type in ('TRUE', 'FALSE'):
            self._consumir(token.type)
            return Booleano(token)
        elif token.type == 'IDENTIFICADOR':
            return self.identificador()
        elif token.type == 'LPAREN':
            self._consumir('LPAREN')
            node = self.expressao()
            self._consumir('RPAREN')
            return node
        else:
            raise ParserError(f"Fator inesperado na expressão: {token.type}")
    
    def identificador(self):
        token = self.token_atual
        self._consumir('IDENTIFICADOR')
        return Identificador(token)
