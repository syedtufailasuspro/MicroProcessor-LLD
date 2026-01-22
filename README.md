# MicroProcessor-LLD

We want to design a basic Microprocessor System. We can assume that our microprocessor consists of a fixed number of registers, say 4 : A, B, C and D. These registers are capable of storing an integer value in them.
The microprocessor should be capable of handling following sets of instructions: -

1. `SET B 7` : Sets the value in register B to 7.
2. `ADR C A` : Adds the content of register A to the content of C and writes it back to C i.e. C = C + A
3. `ADD D 15` : Adds the constant value 15 to the contents of D and writes it back to D i.e. D = D + 15
4. `MOV C D` : Updates the content of C to the content of D, without changing content of D.
5. `INR B` : Same as B++, increments value by 1
6. `DCR A` : Same as A-- 
7. `RST` : Resets the values stored inside all registers to 0.

Note : It is very important for the code to be super extensible, so that we can support new instructions like AND, OR, XOR etc in future.

## How to Run

Requirements: Python 3.x

Run the application using:
```bash
python main.py FILEPATH=sample_input/input1.txt
```

To run tests:
```bash
python tests.py
```