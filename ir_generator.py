class IRGenerator:
    """Gera Código de Três Endereços (TAC) a partir da AST."""

    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        """Cria um novo nome de variável temporária."""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        """Cria um novo nome de label."""
        self.label_count += 1
        return f"L{self.label_count}"

    def visit(self, node):
        """Método de despacho para visitar o nó correto."""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Método genérico para visitar nós sem visitor específico."""
        raise Exception(f'Nenhum método visit_{node.__class__.__name__} encontrado no IRGenerator')

    def visit_Programa(self, node):
        for statement in node.declaracoes:
            self.visit(statement)
        return self.instructions

    def visit_DeclaracaoVariavel(self, node):
        if node.expressao:
            value = self.visit(node.expressao)
            self.instructions.append(('ASSIGN', value, None, node.nome_variavel.nome))
        return None

    def visit_Atribuicao(self, node):
        value = self.visit(node.expressao)
        self.instructions.append(('ASSIGN', value, None, node.nome_variavel.nome))
        return None

    def visit_ComandoPrint(self, node):
        value = self.visit(node.expressao)
        self.instructions.append(('PRINT', value, None, None))
        return None

    def visit_ComandoRead(self, node):
        self.instructions.append(('READ', None, None, node.nome_variavel.nome))
        return None

    def visit_ComandoIf(self, node):
        label_false = self.new_label()
        label_end = self.new_label()

        cond_res = self.visit(node.condicao)
        self.instructions.append(('JUMP_IF_FALSE', cond_res, None, label_false))
        
        self.visit(node.bloco_then)
        self.instructions.append(('JUMP', None, None, label_end))
        
        self.instructions.append(('LABEL', label_false, None, None))
        if node.bloco_else:
            self.visit(node.bloco_else)
            
        self.instructions.append(('LABEL', label_end, None, None))
        return None

    def visit_ComandoWhile(self, node):
        label_start = self.new_label()
        label_end = self.new_label()

        self.instructions.append(('LABEL', label_start, None, None))
        
        cond_res = self.visit(node.condicao)
        self.instructions.append(('JUMP_IF_FALSE', cond_res, None, label_end))
        
        self.visit(node.bloco)
        
        self.instructions.append(('JUMP', None, None, label_start))
        self.instructions.append(('LABEL', label_end, None, None))
        return None

    def visit_Bloco(self, node):
        for statement in node.declaracoes:
            self.visit(statement)
        return None

    def visit_OperacaoBinaria(self, node):
        left = self.visit(node.esquerda)
        right = self.visit(node.direita)
        temp = self.new_temp()
        self.instructions.append((node.op.type, left, right, temp))
        return temp

    def visit_Numero(self, node):
        return str(node.valor)

    def visit_Identificador(self, node):
        return node.nome

    def visit_Booleano(self, node):
        return 'true' if node.valor else 'false'
