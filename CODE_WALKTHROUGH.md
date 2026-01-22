# Microprocessor LLD Code Walkthrough

This document provides a detailed, line-by-line explanation of the Microprocessor design. This is designed to help you understand **Low-Level Design (LLD)** concepts, **SOLID principles**, and **Design Patterns** used in this project.

---

## 1. `microprocessor/register.py`
**Concept**: Encapsulation.

This class represents a single storage unit (Register) in the microprocessor.

```python
class Register:
    def __init__(self):
        self._value = 0
```
-   **`class Register:`**: Defines the blueprint for a register (like A, B, C, D).
-   **`def __init__(self):`**: The constructor. It runs when you say `Register()`.
-   **`self._value = 0`**: We initialize the register with 0.
    -   *Crucial Detail*: The underscore `_` prefix in `_value` is a Python convention indicating this is a **protected/private** variable. We don't want external code modifying it directly (e.g., `reg._value = 100`).

```python
    @property
    def value(self) -> int:
        return self._value
```
-   **`@property`**: This decorator allows us to access the method `value()` like an attribute (i.e., `reg.value` instead of `reg.value()`).
-   **`return self._value`**: This provides read access to the private variable.

```python
    @value.setter
    def value(self, value: int):
        self._value = value
```
-   **`@value.setter`**: This allows us to set the value using `reg.value = 5`.
-   **Why use this?** (Encapsulation): If we later decide that registers can only hold 8-bit numbers (0-255), we can add an `if` check here without changing any other code in the system.

---

## 2. `microprocessor/instructions/base.py`
**Concept**: Interface / Strategy Pattern.

This defines the contract for what an "Instruction" is.

```python
from abc import ABC, abstractmethod

class Instruction(ABC):
```
-   **`ABC`** (Abstract Base Class): This prevents you from creating a generic `Instruction()` object. You *must* create specific types like `AddInstruction`.
-   **Liskov Substitution Principle (LSP)**: Any code that expects an `Instruction` can basically expect *any* child class (Add, Mov, etc.) to work safely.

```python
    @abstractmethod
    def execute(self) -> None:
        pass
```
-   **`@abstractmethod`**: This forces any subclass (like `AddInstruction`) to implement the `execute` method. If they forget, the program crashes at startup.
-   **Command Pattern**: This is the core of the Command Pattern. Every instruction wraps a request as an object (`execute`).

---

## 3. `microprocessor/micro_processor.py`
**Concept**: The Receiver / System State.

This class manages the specific state (Registers) and executes commands.

```python
from typing import Dict, Optional
from microprocessor.register import Register
from microprocessor.instructions.base import Instruction

class MicroProcessor:
    def __init__(self):
        self.registers: Dict[str, Register] = {}
```
-   **`self.registers = {}`**: A dictionary to map names ("A", "B") to actual `Register` objects. This makes the system extensible (we can add register "E" easily).

```python
    def get_register(self, name: str) -> Optional[Register]:
        return self.registers.get(name)
```
-   Returns the `Register` object for a given name. If it doesn't exist, returns `None`.

```python
    def execute_instruction(self, instruction: Instruction) -> None:
        instruction.execute()
```
-   **Polymorphism**: This method doesn't care *what* instruction it is (Add, Mov, Rst). It just knows it has an `execute()` method. This is the **Open/Closed Principle**—we don't need to change this code to add a new instruction type.

```python
    def reset_registers(self) -> None:
        for register in self.registers.values():
            register.value = 0
```
-   Iterates through all registers and resets them. Used by `RstInstruction`.

```python
    def add_register(self, name: str) -> None:
        self.registers[name] = Register()
```
-   Dynamically creates a new register.

---

## 4. `microprocessor/instructions/commands.py`
**Concept**: Concrete Commands / Single Responsibility Principle (SRP).

Each class here does **one** thing.

### Example: `AddInstruction`

```python
class AddInstruction(Instruction):
    def __init__(self, register_name: str, value: int, micro_processor: MicroProcessor):
        self.register = micro_processor.get_register(register_name)
        self.value = value
```
-   **`__init__`**: Captures *everything* needed to execute the command **later**. It doesn't run the math yet; it just prepares.
-   It stores the specific `Register` object and the value to add.

```python
    def execute(self) -> None:
        if self.register:
            self.register.value += self.value
```
-   **`execute`**: Performs the actual business logic. It modifies the state of the register.

### Example: `MovInstruction`

```python
class MovInstruction(Instruction):
    def __init__(self, src_name: str, dest_name: str, micro_processor: MicroProcessor):
        self.src = micro_processor.get_register(src_name)
        self.dest = micro_processor.get_register(dest_name)
```
-   **Dependency Injection**: We pass the `micro_processor` into the instruction so it can look up the registers it needs.

```python
    def execute(self) -> None:
        if self.src and self.dest:
            self.dest.value = self.src.value
```
-   Copies value from source to destination.

---

## 5. `microprocessor/instructions/registry.py`
**Concept**: Factory / Static Factory Method.

This acts as a middleman to create instruction objects.

```python
class InstructionRegistry:
    @staticmethod
    def get_add_instruction(register: str, value: int, micro_processor: MicroProcessor) -> Instruction:
        return AddInstruction(register, value, micro_processor)
```
-   **Decoupling**: The main code should not need to know `AddInstruction` exists deeply. It just asks the Registry for it.
-   **Factory Pattern**: If `AddInstruction` constructor changes (e.g., takes a new logging parameter), we only change this file, not `main.py`.

---

## 6. `main.py`
**Concept**: The Client / Driver Code.

This parses text input and coordinates the system.

```python
def run(command_line_args: List[str]):
    # ... setup logic ...
    micro_processor = MicroProcessor()
    micro_processor.add_register("A") # ... etc
```
-   Initializes the "Machine".

```python
                if command == "ADD":
                    register = tokens[1]
                    value = int(tokens[2])
                    instruction = InstructionRegistry.get_add_instruction(register, value, micro_processor)
```
-   **Parsing**: It reads the string "ADD" and decides which factory method to call.
-   **Creation**: It creates the instruction object but does *not* execute it yet.

```python
                if instruction:
                    # Execute
                    micro_processor.execute_instruction(instruction)
```
-   **Execution**: Finally, it tells the microprocessor to run the instruction object it just built.

---

## Summary of SOLID Principles Used

1.  **S - Single Responsibility Principle**:
    -   `Register` only manages data.
    -   `AddInstruction` only knows how to add.
    -   `main.py` only handles file I/O.
2.  **O - Open/Closed Principle**:
    -   To add a `SUB` (Subtract) instruction, you create `SubInstruction` and update the Registry. You **do not** touch `MicroProcessor.py` or `Instruction.java`.
3.  **L - Liskov Substitution Principle**:
    -   `MicroProcessor` can execute *any* class that inherits from `Instruction` without breaking.
4.  **I - Interface Segregation**:
    -   Our `Instruction` interface is simple (`execute` only). We don't force instructions to implement unrelated methods.
5.  **D - Dependency Inversion**:
    -   High-level modules (the logic runner) depend on abstractions (`Instruction` interface), not concrete details.
