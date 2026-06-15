<p align="center">
  <img src="./images/image-removebg-preview.png" alt="Compiler Logo" width="144">
</p>

# Compilador ASLAN

Este projeto consiste no desenvolvimento de um compilador completo para uma linguagem de programação imperativa simples

## 👥 Integrantes
- Alison Oliveira
- Maria Clara
- Davi Ribeiro

## 🚀 Estrutura do Projeto

```
/
|-- src/
|   |-- lexer.py            # Fase 1: Analisador Léxico (Scanner Padrão)
|   |-- lexer_narnia.py     # Fase 1: Analisador Léxico (Tema Nárnia)
|   |-- lexer_lotr.py       # Fase 1: Analisador Léxico (Tema Senhor dos Anéis)
|   |-- parser_.py          # Fase 2: Analisador Sintático (Parser) e AST
|   |-- semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
|   |-- optimizer.py        # Bônus: Otimizador de AST (Constant Folding)
|   |-- ir_generator.py     # Fase 4: Gerador de Código Intermediário (TAC)
|   |-- code_generator.py   # Fase 5: Gerador de Bytecode
|   |-- vm.py               # Fase 5: Máquina Virtual (Stack Machine)
|-- aslan.py             # Script principal de execução
|-- demo.py              # Script interativo de demonstração
|-- test_runner.py       # Executor central de testes
|-- DOCS.md              # Documentação técnica detalhada
|-- examples/            # Galeria de exemplos (.aslan)
|-- tests/               # Suíte de testes (74 casos automatizados)
|-- .gitignore           # Configurações de repositório
|-- README.md            # Guia de apresentação e visão geral
```

## 🎮 Demonstração Interativa e Temas

Para explorar os exemplos da linguagem e criar seus próprios códigos de forma interativa, execute:

```sh
python3 demo.py
```

O script permite listar exemplos clássicos (Fibonacci, Ordenação, etc.), visualizar o código-fonte e rodá-los imediatamente na VM. Você também pode alternar entre os **Temas de Sintaxe** pressionando a tecla `M` no menu.

Os temas também podem ser usados via linha de comando:

1. **Padrão**: Inglês tradicional (`int`, `bool`, `if`, `while`, `print`).
   ```sh
   python3 aslan.py meucodigo.aslan
   ```
2. **Nárnia**: Inspirado nas Crônicas de Nárnia (`rei_pedro`, `rainha_lucia`, `pela_juba_do_leao`, `proclamar`).
   ```sh
   python3 aslan.py arquivo.aslan --narnia
   ```
3. **Senhor dos Anéis**: Inspirado na luta de Gandalf e o Balrog (`poder_maia`, `chama_de_udun`, `nao_passara`, `cajado_brilha`).
   ```sh
   python3 aslan.py arquivo.aslan --lotr
   ```

## 🛠️ Como Executar os Testes

Para validar a integridade de todas as fases do compilador, execute:

```sh
python3 test_runner.py
```

## 📝 Documentação Detalhada (Módulos)

Para uma análise profunda de cada classe, método e complexidade Big-O de cada etapa, consulte o arquivo **[DOCS.md](./DOCS.md)**.

