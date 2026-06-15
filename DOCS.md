# 📖 Documentação Técnica Completa: ASLAN

## 1. Arquitetura Geral e Fluxo de Dados (Pipeline)

O sistema segue a arquitetura de **Compilador de Passagem Única com Fases Independentes** (embora estruturado em múltiplos arquivos para modularidade). A comunicação entre os módulos é estritamente sequencial, garantindo alta coesão e baixo acoplamento.

```text
[Código Fonte: String] 
         │
         ▼
  (1) LEXER (src/lexer.py) ─────────────> [Fluxo de Tokens]
         │
         ▼
  (2) PARSER (src/parser_.py) ──────────> [AST (Árvore de Sintaxe Abstrata)]
         │
         ▼
  (3) SEMÂNTICA (src/semantic.py) ──────> [AST Validada (Tipos e Escopos ok)]
         │
         ▼
  (4) OTIMIZADOR (src/optimizer.py) ────> [AST Simplificada (Constant Folding)]
         │
         ▼
  (5) IR GENERATOR (src/ir_generator.py) > [TAC (Código de Três Endereços)]
         │
         ▼
  (6) CODE GENERATOR (src/code_generator.py) > [Bytecode (Endereços Resolvidos)]
         │
         ▼
  (7) VIRTUAL MACHINE (src/vm.py) ──────> [Execução na Memória / Saída I/O]
```

---

## 2. Especificação e Gramática da Linguagem (EBNF Simplificada)

O parser foi construído com base na seguinte gramática livre de contexto:

```ebnf
<programa>   ::= <statement>* EOF
<statement>  ::= <declaracao> | <atribuicao> | <comando_if> | <comando_while> 
               | <comando_print> | <comando_read> | <bloco>
<declaracao> ::= ("int" | "bool") IDENTIFICADOR ("=" <expressao>)? ";"
<atribuicao> ::= IDENTIFICADOR "=" <expressao> ";"
<comando_if> ::= "if" "(" <expressao> ")" <statement> ("else" <statement>)?
<comando_while>::= "while" "(" <expressao> ")" <statement>
<bloco>      ::= "{" <statement>* "}"
<expressao>  ::= <igualdade>
<igualdade>  ::= <comparacao> (("==" | "!=") <comparacao>)*
<comparacao> ::= <termo> ((">" | "<" | ">=" | "<=") <termo>)*
<termo>      ::= <fator> (("+" | "-") <fator>)*
<fator>      ::= <primario> (("*" | "/") <primario>)*
<primario>   ::= NUMERO | "true" | "false" | IDENTIFICADOR | "(" <expressao> ")"
```

---

## 3. Detalhamento dos Módulos

### 3.1. Analisador Léxico (`src/lexer.py`)
*   **Responsabilidade:** Converter a *string* do código fonte em uma lista estruturada de `Tokens`, descartando espaços, quebras de linha e comentários (`//`).
*   **Classes e Estruturas:**
    *   `Token(type, value, line, column)`: Objeto de transporte contendo os metadados do léxico.
    *   `LexerError(Exception)`: Exceção customizada para caracteres inválidos.
*   **Como funciona (Método `tokenize`):** Utiliza a biblioteca `re` do Python. Constrói uma Mega-Regex usando *Named Capture Groups* (`(?P<TIPO>regex)`). O método usa `match.end()` para fatiar o código fonte iterativamente.
*   **Tipos Tratados:** `INT`, `BOOL`, `STRING` (tipos); `IF`, `ELSE`, `WHILE`, `PRINT`, `READ` (palavras-chave); `MAIS`, `MENOS`, `MULT`, `DIV`, `IGUAL_COMP`, `DIFERENTE`, `MAIOR`, `MENOR`, `MAIOR_IGUAL`, `MENOR_IGUAL` (operadores); numéricos inteiros, booleanos e strings delimitadas por aspas duplas.

### 3.2. Analisador Sintático (`src/parser_.py`)
*   **Responsabilidade:** Implementar um Parser Descendente Recursivo preditivo (LL(1)) para transformar `List[Token]` em uma AST.
*   **Classes de Nós (ASTNodes):** 
    *   *Nós de Expressão:* `Numero`, `Texto` (String), `Booleano`, `Identificador`, `OperacaoBinaria`.
    *   *Nós de Comando:* `DeclaracaoVariavel`, `Atribuicao`, `ComandoIf`, `ComandoWhile`, `ComandoPrint`, `ComandoRead`, `Bloco`.
*   **Métodos Principais:**
    *   `_consumir(tipo_esperado)`: Compara `token_atual.type`. Se casar, avança o ponteiro. Se falhar, levanta `ParserError`.
    *   A hierarquia de precedência de operadores é feita matematicamente através da cadeia de chamadas de métodos: `expressao()` -> `igualdade()` -> `comparacao()` -> `termo()` -> `fator()` -> `primario()`.

### 3.3. Analisador Semântico (`src/semantic.py`)
*   **Responsabilidade:** Adicionar significado e validações lógicas à AST.
*   **Classe `SymbolTable`:**
    *   Mantém o estado do escopo na propriedade `self.scopes` (uma Pilha de Dicionários `[{}]`).
    *   `enter_scope()`: Dá `.append({})`.
    *   `leave_scope()`: Dá `.pop()`. Garante que variáveis locais morram ao sair de blocos.
    *   `lookup(name)`: Busca de cima para baixo (`reversed(self.scopes)`).
    *   **Classe `SemanticAnalyzer` (Implementa o padrão *Visitor*):**
    *   Possui métodos `visit_NomeDoNo(node)`.
    *   *Type Checking:* Retorna os tipos lógicos (`'INT'`, `'BOOL'` ou `'STRING'`) a cada visita. Avalia regras como: `(INT) MAIS (INT) -> INT` e validações de igualdade entre tipos compatíveis.
    *   Levanta `SemanticError` em três casos principais: 
    ...
        1. Variável não declarada; 
        2. Redeclaração no mesmo escopo; 
        3. Incompatibilidade de tipos (ex: `int x = true;` ou `while (10)`).
### 3.4. Otimizador de Código (`src/optimizer.py`)
*   **Responsabilidade:** Passagem opcional que reduz a carga de execução operando simplificações (*Constant Folding*) em tempo de compilação.
*   **Funcionamento (Visitor):** 
    *   No método `visit_OperacaoBinaria`, ele resolve os ramos esquerdo e direito. 
    *   Se ambos retornarem nós literais (`Numero` ou `Booleano`), o compilador calcula o resultado em Python e **destrói** a árvore da `OperacaoBinaria`, retornando um único nó literal equivalente para o nó pai.

### 3.5. Gerador de Código Intermediário (`src/ir_generator.py`)
*   **Responsabilidade:** Linearizar a AST para TAC (Código de Três Endereços).
*   **Estruturas de Dados:**
    *   `self.instructions`: `List[Tuple]`.
    *   Gera temporários via `self.new_temp()` (ex: `t1, t2`) e labels via `self.new_label()` (ex: `L1, L2`).
*   **Padrões de Tradução:**
    *   *Expressão:* `10 + 5` -> `('MAIS', '10', '5', 't1')`
    *   *If-Else:* Avalia a condição, gera `('JUMP_IF_FALSE', cond_var, None, 'L_FALSE')`, visita corpo `THEN`, gera `JUMP L_END`, cria instrução `LABEL L_FALSE`, visita corpo `ELSE`, cria instrução `LABEL L_END`.

### 3.6. Gerador de Código Final (`src/code_generator.py`)
*   **Responsabilidade:** Traduzir TAC generalista para as instruções de pilha específicas da nossa Máquina Virtual.
*   **Algoritmo de Duas Passagens (2-Pass Resolution):**
    *   **Passagem 1:** Traduz as instruções (ex: `MAIS` -> `LOAD arg1`, `LOAD arg2`, `ADD`, `STORE result`). Ignora endereços de `JUMP`, mas anota o índice real da instrução na memória toda vez que encontra um `LABEL`.
    *   **Passagem 2:** Varre o Bytecode novamente, substituindo labels textuais (ex: `'L2'`) pelo índice inteiro absoluto da memória.

### 3.7. Máquina Virtual (`src/vm.py`)
*   **Responsabilidade:** Executar o Bytecode gerado utilizando a arquitetura Stack Machine (Pilha).
*   **Estruturas de Memória:**
    *   `self.stack`: Lista LIFO `[]` que acumula valores soltos e operandos.
    *   `self.memory`: Dicionário `{}` ("Heap/Registradores") armazenando valores de variáveis (ex: `memory['x'] = 10`).
    *   `self.pc`: Program Counter. Ponteiro para a linha atual do Bytecode.
*   **Conjunto de Instruções (ISA):**
    *   `PUSH val`: `stack.append(val)`
    *   `LOAD var`: `stack.append(memory[var])`
    *   `STORE var`: `memory[var] = stack.pop()`
    *   `ADD/SUB/MUL/DIV`: `b = pop()`, `a = pop()`, `push(a OP b)`
    *   `JUMP addr`: `pc = addr - 1`
    *   `JUMP_IF_FALSE addr`: se `not pop()`, `pc = addr - 1`
    *   `READ var`: `memory[var] = input()`
    *   `PRINT`: `print(pop())`

---

## 4. Integração e Fluxo do Módulo Principal (End-to-End)

A integração do projeto flui encadeando a saída de uma classe como entrada da próxima. O fluxo de inicialização seria exatamente este em um `main.py` de produção:

```python
# 1. Lexer recebe String, solta Tokens
tokens = Lexer(codigo_fonte).tokenize()

# 2. Parser recebe Tokens, solta AST
ast = Parser(tokens).parse()

# 3. Analisador Semântico valida a AST in-place
SemanticAnalyzer().visit(ast)

# 4. Otimizador simplifica a AST in-place
Optimizer().visit(ast)

# 5. IR Generator gera o TAC
tac = IRGenerator().visit(ast)

# 6. Code Generator transforma TAC em Bytecode
bytecode = CodeGenerator(tac).generate()

# 7. VM executa o Bytecode
VirtualMachine(bytecode).run()
```
*O padrão de projeto **Visitor** usado nas fases centrais (Semântica, Otimização, IR) é o grande segredo dessa integração elegante, pois permite injetar comportamentos na Árvore de Sintaxe sem precisar modificar as classes de dados da árvore original.*

---

## 5. Análise de Performance, Tempo e Espaço (Big-O)

| Módulo | Estrutura Dominante | Tempo (Time) | Espaço (Space) | Análise de Gargalos |
| :--- | :--- | :--- | :--- | :--- |
| **Lexer** | Motor Regex nativo | $O(N)$ | $O(T)$ | Linear sobre os caracteres ($N$). O espaço é proporcional ao número de Tokens ($T$). Altamente eficiente. |
| **Parser** | Descida Recursiva | $O(T)$ | $O(N_{ast})$ | Sem backtracking (é LL(1)). Visita cada token uma vez. O tamanho da Árvore de Sintaxe ($N_{ast}$) domina a memória ram. |
| **Semantic** | Pilha de Hash Maps | $O(N_{ast})$ | $O(S + V)$ | Busca na tabela é teórica $O(Escopos)$, mas praticamente $O(1)$ usando hashes. $V$ é o total de Variáveis Locais ativas na ramificação mais profunda. |
| **Optimizer**| Depth-First Search | $O(N_{ast})$ | $O(N_{ast})$ | Modifica a AST in-place. Otimização linear muito rápida. |
| **IR Gen.** | Linearização AST | $O(N_{ast})$ | $O(I_{tac})$ | Percorre a AST uma vez, gerando $I_{tac}$ instruções na memória. |
| **Code Gen.**| Array de Tuplas (2-Pass)| $O(I_{tac})$ | $O(I_{byte})$ | A primeira e segunda passagem são estritamente lineares. Uso de dict de labels torna a Passagem 2 $O(1)$ por resolução de endereço. |
| **VM Execution**| Loop Fetch-Decode | $O(E)$ | $O(V_{exec} + P)$ | Depende do Algoritmo compilado ($E$ iterações). Uso de Pilha ($P$) e Memória local ($V_{exec}$). Eficiente em $O(1)$ por ciclo de clock virtual, o overhead vem do loop da
