from microprocessor.micro_processor import MicroProcessor
from microprocessor.instructions.registry import InstructionRegistry

def test():
    mp = MicroProcessor()
    mp.add_register("A")
    mp.add_register("B")
    
    # SET A 10
    i1 = InstructionRegistry.get_set_instruction("A", 10, mp)
    mp.execute_instruction(i1)
    assert mp.get_register("A").value == 10
    print("SET OK")
    
    # INR A
    i2 = InstructionRegistry.get_inr_instruction("A", mp)
    mp.execute_instruction(i2)
    assert mp.get_register("A").value == 11
    print("INR OK")
    
    # MOV A B (B is 0) -> B = A -> B=11
    i3 = InstructionRegistry.get_mov_instruction("A", "B", mp)
    mp.execute_instruction(i3)
    assert mp.get_register("B").value == 11
    print("MOV OK")
    
    # ADD B 5 -> B = B + 5 = 16
    i4 = InstructionRegistry.get_add_instruction("B", 5, mp)
    mp.execute_instruction(i4)
    assert mp.get_register("B").value == 16
    print("ADD OK")
    
    print("All tests passed")

if __name__ == "__main__":
    test()
