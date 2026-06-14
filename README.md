# Compilador Didático em Python

Este projeto consiste no desenvolvimento de um compilador completo para uma linguagem de programação imperativa simples, utilizando exclusivamente Python e suas bibliotecas padrão. O projeto foi construído seguindo rigorosos princípios de engenharia de software e teoria de linguagens formais.

## 🚀 Estrutura do Projeto

```
/
|-- lexer.py            # Fase 1: Analisador Léxico (Scanner)
|-- parser_.py          # Fase 2: Analisador Sintático (Parser) e AST
|-- semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
|-- optimizer.py        # Bônus: Otimizador de AST (Constant Folding)
|-- ir_generator.py     # Fase 4: Gerador de Código Intermediário (TAC)
|-- code_generator.py   # Fase 5: Gerador de Bytecode
|-- vm.py               # Fase 5: Máquina Virtual (Stack Machine)
|-- test_runner.py      # Executor central de testes
|-- DOCS.md             # Documentação técnica detalhada
|-- tests/              # Suíte de testes (61 casos automatizados)
|-- .gitignore          # Configurações de repositório
|-- README.md           # Guia de apresentação e visão geral
```

## 🛠️ Como Executar os Testes

Para validar a integridade de todas as fases do compilador, execute:

```sh
python3 test_runner.py
```

---

## 📖 Guia de Apresentação (Para os Integrantes)

Este guia foi preparado para ajudar a equipe a explicar o funcionamento do compilador de forma didática durante a apresentação do projeto.

### 1. O que é este Compilador?
É um sistema que traduz uma linguagem de alto nível (com `if`, `while`, `int`) para uma linguagem de baixíssimo nível (Bytecode) que roda em nossa própria Máquina Virtual. Ele não é apenas um interpretador; ele passa por todas as fases clássicas de compilação.

### 2. O Fluxo de Dados (A "Pergunta de Ouro")
**Pergunta:** "O que acontece quando eu clico em 'Compilar'?"
**Resposta:** 
1. O **Lexer** quebra o texto em tokens.
2. O **Parser** organiza os tokens em uma árvore (AST).
3. O **Semântico** checa se você não está somando `int` com `bool` ou usando variáveis inexistentes.
4. O **Otimizador** faz as contas constantes (ex: `2+2` vira `4`) para economizar tempo depois.
5. O **IR Generator** transforma a árvore em uma lista plana de instruções (TAC).
6. O **Code Generator** transforma essa lista em números e códigos que a VM entende (Bytecode).
7. A **VM** executa esse código usando uma pilha.

### 3. Perguntas Técnicas Prováveis (FAQ)

*   **P: Por que usar o Padrão Visitor?**
    *   **R:** Para manter o código limpo. Os nós da nossa Árvore (AST) só guardam dados. Toda a "inteligência" (Semântica, IR, Otimização) fica em classes separadas. Isso facilita adicionar novas funcionalidades sem mexer na estrutura da árvore.
*   **P: O que é TAC (Código de Três Endereços)?**
    *   **R:** É uma linguagem intermediária simplificada. Cada linha tem no máximo 3 endereços (dois operandos e um destino). Ex: `t1 = a + b`. Isso facilita muito a vida do gerador de código final.
*   **P: Como a VM funciona sem registradores?**
    *   **R:** Ela é uma **Máquina de Pilha** (Stack Machine). Em vez de dizer "coloque no registrador EAX", nós dizemos "coloque na pilha". Operações como `ADD` retiram os dois últimos valores da pilha e colocam o resultado de volta. É o mesmo modelo usado pelo Java (JVM) e Python.
*   **P: Como vocês lidaram com saltos (Jumps) no `if` e `while`?**
    *   **R:** Usamos uma técnica de **duas passagens**. Primeiro geramos o código e marcamos onde estão os "Labels". Na segunda passagem, voltamos substituindo o nome do Label pelo número exato da linha para onde a VM deve pular.

---

## 📝 Documentação Detalhada (Módulos)

Para uma análise profunda de cada classe, método e complexidade Big-O de cada etapa, consulte o arquivo **[DOCS.md](./DOCS.md)**.

### Resumo das Fases Concluídas:
-   **✅ Análise Léxica:** Reconhecimento completo de tokens e tratamento de erros de linha/coluna.
-   **✅ Análise Sintática:** Construção de AST com precedência de operadores e estruturas complexas.
-   **✅ Análise Semântica:** Tabela de símbolos com suporte a múltiplos escopos e *Type Checking*.
-   **✅ Otimização:** Implementação de *Constant Folding*.
-   **✅ IR & Code Gen:** Geração de TAC e Bytecode resolvida.
-   **✅ Máquina Virtual:** Execução funcional com suporte a `read` e `print`.

---

## 🏁 Conclusão
O projeto atingiu 100% dos requisitos obrigatórios e bônus, com **61 testes automatizados** garantindo que algoritmos como **Fibonacci**, **Fatorial** e **Bubble Sort** funcionem perfeitamente do código fonte à execução.
