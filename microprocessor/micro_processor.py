from typing import Dict, Optional
from microprocessor.register import Register
from microprocessor.instructions.base import Instruction

class MicroProcessor:
    def __init__(self):
        self.registers: Dict[str, Register] = {}

    def get_register(self, name: str) -> Optional[Register]:
        return self.registers.get(name)

    def execute_instruction(self, instruction: Instruction) -> None:
        instruction.execute()

    def reset_registers(self) -> None:
        for register in self.registers.values():
            register.value = 0

    def add_register(self, name: str) -> None:
        self.registers[name] = Register()

    def remove_register(self, name: str) -> None:
        if name in self.registers:
            del self.registers[name]
