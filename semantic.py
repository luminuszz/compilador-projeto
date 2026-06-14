class SemanticError(Exception):
    """Exceção para erros semânticos."""
    pass

class Symbol:
    """Representa um símbolo na tabela (variável, função, etc.)."""
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable:
    """Gerencia os símbolos e escopos."""
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        """Entra em um novo escopo (ex: dentro de um bloco if/while)."""
        self.scopes.append({})

    def leave_scope(self):
        """Sai do escopo atual."""
        self.scopes.pop()

    def declare(self, symbol):
        """Declara um novo símbolo no escopo atual."""
        scope = self.scopes[-1]
        if symbol.name in scope:
            raise SemanticError(
                f"Erro: Variável '{symbol.name}' já declarada neste escopo."
            )
        scope[symbol.name] = symbol

    def lookup(self, name):
        """Busca por um símbolo em todos os escopos, do mais interno para o mais externo."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticAnalyzer:
    """Percorre a AST e realiza a análise semântica."""
    def __init__(self):
        self.symtab = SymbolTable()

    def visit(self, node):
        """Método de despacho para visitar o nó correto."""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Método genérico para visitar nós que não têm um método 'visit_' específico."""
        raise Exception(f"Nenhum método visit_{node.__class__.__name__} encontrado")

    def visit_Programa(self, node):
        for statement in node.declaracoes:
            self.visit(statement)
        return None

    def visit_DeclaracaoVariavel(self, node):
        received_type = None
        if node.expressao:
            received_type = self.visit(node.expressao)

        expected_type = node.tipo.type
        if received_type and received_type != expected_type:
            raise SemanticError(
                f"Erro: Tipo incompatível para a variável '{node.nome_variavel.nome}'. Esperado '{expected_type}', mas recebeu '{received_type}'."
            )

        symbol = Symbol(name=node.nome_variavel.nome, type=expected_type)
        self.symtab.declare(symbol)
        return expected_type

    def visit_Atribuicao(self, node):
        symbol_name = node.nome_variavel.nome
        symbol = self.symtab.lookup(symbol_name)
        if not symbol:
            raise SemanticError(f"Erro: Variável '{symbol_name}' não declarada.")

        received_type = self.visit(node.expressao)

        if symbol.type != received_type:
            raise SemanticError(
                f"Erro: Tipo incompatível na atribuição para '{symbol_name}'. Esperado '{symbol.type}', mas recebeu '{received_type}'."
            )

        return symbol.type

    def visit_ComandoPrint(self, node):
        self.visit(node.expressao)
        return None

    def visit_ComandoRead(self, node):
        symbol_name = node.nome_variavel.nome
        if not self.symtab.lookup(symbol_name):
            raise SemanticError(f"Erro: Variável '{symbol_name}' não declarada.")
        return None

    def visit_OperacaoBinaria(self, node):
        type_left = self.visit(node.esquerda)
        type_right = self.visit(node.direita)
        op_type = node.op.type

        if op_type in ("MAIS", "MENOS", "MULT", "DIV"):
            if type_left == "INT" and type_right == "INT":
                return "INT"
            else:
                raise SemanticError(
                    f"Erro: Operação aritmética '{op_type}' exige operandos do tipo 'INT'."
                )

        if op_type in ("MAIOR", "MENOR", "MAIOR_IGUAL", "MENOR_IGUAL"):
            if type_left == "INT" and type_right == "INT":
                return "BOOL"
            else:
                raise SemanticError(
                    f"Erro: Operação de comparação '{op_type}' exige operandos do tipo 'INT'."
                )

        if op_type in ("IGUAL_COMP", "DIFERENTE"):
            if type_left == type_right:
                return "BOOL"
            else:
                raise SemanticError(
                    f"Erro: Operação de igualdade '{op_type}' exige operandos do mesmo tipo."
                )

        return None

    def visit_ComandoIf(self, node):
        cond_type = self.visit(node.condicao)
        if cond_type != "BOOL":
            raise SemanticError(
                f"Erro: A condição do 'if' deve ser 'BOOL', mas recebeu '{cond_type}'."
            )

        self.visit(node.bloco_then)
        if node.bloco_else:
            self.visit(node.bloco_else)
        return None

    def visit_ComandoWhile(self, node):
        cond_type = self.visit(node.condicao)
        if cond_type != "BOOL":
            raise SemanticError(
                f"Erro: A condição do 'while' deve ser 'BOOL', mas recebeu '{cond_type}'."
            )

        self.visit(node.bloco)
        return None

    def visit_Bloco(self, node):
        self.symtab.enter_scope()
        for statement in node.declaracoes:
            self.visit(statement)
        self.symtab.leave_scope()
        return None

    def visit_Identificador(self, node):
        symbol_name = node.nome
        symbol = self.symtab.lookup(symbol_name)
        if not symbol:
            raise SemanticError(f"Erro: Variável '{symbol_name}' não declarada.")
        return symbol.type

    def visit_Numero(self, node):
        return "INT"

    def visit_Booleano(self, node):
        return "BOOL"
