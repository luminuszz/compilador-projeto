class VirtualMachine:
    """Máquina Virtual baseada em pilha para executar Bytecode."""

    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.stack = []
        self.memory = {}
        self.pc = 0
        self.running = False
        self.output = []

    def run(self):
        self.running = True
        while self.running and self.pc < len(self.bytecode):
            instruction = self.bytecode[self.pc]
            opcode = instruction[0]
            arg = instruction[1] if len(instruction) > 1 else None
            
            self.execute(opcode, arg)
            self.pc += 1

    def execute(self, opcode, arg):
        if opcode == 'PUSH':
            self.stack.append(arg)
        
        elif opcode == 'LOAD':
            val = self.memory.get(arg)
            if val is None:
                raise Exception(f"Erro na VM: Variável '{arg}' não inicializada.")
            self.stack.append(val)
            
        elif opcode == 'STORE':
            val = self.stack.pop()
            self.memory[arg] = val
            
        elif opcode == 'ADD':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) + int(b))
            
        elif opcode == 'SUB':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) - int(b))
            
        elif opcode == 'MUL':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) * int(b))
            
        elif opcode == 'DIV':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) // int(b))
            
        elif opcode == 'CMP_GT':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) > int(b))
            
        elif opcode == 'CMP_LT':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(int(a) < int(b))
            
        elif opcode == 'CMP_EQ':
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a == b)
            
        elif opcode == 'JUMP':
            self.pc = arg - 1
            
        elif opcode == 'JUMP_IF_FALSE':
            val = self.stack.pop()
            if not val:
                self.pc = arg - 1
                
        elif opcode == 'PRINT':
            val = self.stack.pop()
            self.output.append(str(val))
            print(val)
            
        elif opcode == 'READ':
            if hasattr(self, 'inputs') and self.inputs:
                val = self.inputs.pop(0)
            else:
                val = input(f"Entrada para '{arg}': ")
            self.memory[arg] = int(val)

        elif opcode == 'HALT':
            self.running = False
            
        else:
            raise Exception(f"Erro na VM: Instrução desconhecida '{opcode}'")
