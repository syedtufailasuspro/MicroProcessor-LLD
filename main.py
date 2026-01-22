import sys
import os
from typing import List
from microprocessor.micro_processor import MicroProcessor
from microprocessor.instructions.registry import InstructionRegistry

def run(command_line_args: List[str]):
    micro_processor = MicroProcessor()
    micro_processor.add_register("A")
    micro_processor.add_register("B")
    micro_processor.add_register("C")
    micro_processor.add_register("D")

    if not command_line_args:
        print("No input file provided")
        return

    arg = command_line_args[0]
    if "=" in arg:
        input_file = arg.split("=")[1]
    else:
        input_file = arg
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                tokens = line.split(" ")
                command = tokens[0]
                
                instruction = None
                
                if command == "ADD":
                    register = tokens[1]
                    value = int(tokens[2])
                    instruction = InstructionRegistry.get_add_instruction(register, value, micro_processor)
                elif command == "ADR":
                    register1 = tokens[1]
                    register2 = tokens[2]
                    instruction = InstructionRegistry.get_adr_instruction(register1, register2, micro_processor)
                elif command == "DCR":
                    register = tokens[1]
                    instruction = InstructionRegistry.get_dcr_instruction(register, micro_processor)
                elif command == "INR":
                    register = tokens[1]
                    instruction = InstructionRegistry.get_inr_instruction(register, micro_processor)
                elif command == "MOV":
                    src = tokens[1]
                    dest = tokens[2]
                    instruction = InstructionRegistry.get_mov_instruction(src, dest, micro_processor)
                elif command == "RST":
                    instruction = InstructionRegistry.get_rst_instruction(micro_processor)
                elif command == "SET":
                    register = tokens[1]
                    value = int(tokens[2])
                    instruction = InstructionRegistry.get_set_instruction(register, value, micro_processor)
                else:
                    raise RuntimeError("Invalid Instruction!")
                
                if instruction:
                    # Execute
                    micro_processor.execute_instruction(instruction)
                    # For debugging/verification, we might want to print something, 
                    # but Java code didn't print anything during execution loop.
                    
    except Exception as e:
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        # Default behavior in Java code was to throw RuntimeException if args != 1
        # But here we act nicer or similar.
        print("Usage: python main.py FILEPATH=<path>")
        sys.exit(1)
    
    run(sys.argv[1:])

if __name__ == "__main__":
    main()
