from microprocessor.instructions.base import Instruction
from microprocessor.micro_processor import MicroProcessor

class AddInstruction(Instruction):
    def __init__(self, register_name: str, value: int, micro_processor: MicroProcessor):
        self.register = micro_processor.get_register(register_name)
        self.value = value

    def execute(self) -> None:
        if self.register:
            self.register.value += self.value

class AdrInstruction(Instruction):
    def __init__(self, register1_name: str, register2_name: str, micro_processor: MicroProcessor):
        self.register1 = micro_processor.get_register(register1_name)
        self.register2 = micro_processor.get_register(register2_name)

    def execute(self) -> None:
        if self.register1 and self.register2:
            self.register1.value += self.register2.value

class DcrInstruction(Instruction):
    def __init__(self, register_name: str, micro_processor: MicroProcessor):
        self.register = micro_processor.get_register(register_name)

    def execute(self) -> None:
        if self.register:
            self.register.value -= 1

class InrInstruction(Instruction):
    def __init__(self, register_name: str, micro_processor: MicroProcessor):
        self.register = micro_processor.get_register(register_name)

    def execute(self) -> None:
        if self.register:
            self.register.value += 1

class MovInstruction(Instruction):
    def __init__(self, src_name: str, dest_name: str, micro_processor: MicroProcessor):
        self.src = micro_processor.get_register(src_name)
        self.dest = micro_processor.get_register(dest_name)

    def execute(self) -> None:
        if self.src and self.dest:
            self.dest.value = self.src.value

class RstInstruction(Instruction):
    def __init__(self, micro_processor: MicroProcessor):
        self.micro_processor = micro_processor

    def execute(self) -> None:
        self.micro_processor.reset_registers()

class SetInstruction(Instruction):
    def __init__(self, register_name: str, value: int, micro_processor: MicroProcessor):
        self.register = micro_processor.get_register(register_name)
        self.value = value

    def execute(self) -> None:
        if self.register:
            self.register.value = self.value
