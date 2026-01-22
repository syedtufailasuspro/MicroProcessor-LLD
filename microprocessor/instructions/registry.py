from microprocessor.micro_processor import MicroProcessor
from microprocessor.instructions.base import Instruction
from microprocessor.instructions.commands import (
    AddInstruction, AdrInstruction, DcrInstruction, 
    InrInstruction, MovInstruction, RstInstruction, SetInstruction
)

class InstructionRegistry:
    @staticmethod
    def get_add_instruction(register: str, value: int, micro_processor: MicroProcessor) -> Instruction:
        return AddInstruction(register, value, micro_processor)

    @staticmethod
    def get_adr_instruction(register1: str, register2: str, micro_processor: MicroProcessor) -> Instruction:
        return AdrInstruction(register1, register2, micro_processor)

    @staticmethod
    def get_dcr_instruction(register: str, micro_processor: MicroProcessor) -> Instruction:
        return DcrInstruction(register, micro_processor)

    @staticmethod
    def get_inr_instruction(register: str, micro_processor: MicroProcessor) -> Instruction:
        return InrInstruction(register, micro_processor)

    @staticmethod
    def get_mov_instruction(src: str, dest: str, micro_processor: MicroProcessor) -> Instruction:
        return MovInstruction(src, dest, micro_processor)

    @staticmethod
    def get_rst_instruction(micro_processor: MicroProcessor) -> Instruction:
        return RstInstruction(micro_processor)

    @staticmethod
    def get_set_instruction(register: str, value: int, micro_processor: MicroProcessor) -> Instruction:
        return SetInstruction(register, value, micro_processor)
