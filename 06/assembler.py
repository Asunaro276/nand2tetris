from io import TextIOWrapper
from typing import List
from api_module import code, parser, symbol_table


def make_symbol_table(instructions: List[str]):
    program_count = 0
    line_count = 0
    instruction = instructions[program_count]
    while True:
        instruction_type = parser.judge_instruction_type(instruction)
        if instruction_type == "L":
            symbol = parser.extract_symbol(instruction)
            symbol_table.add_entry(symbol, program_count)
            line_count += 1
            instruction = parser.advance_instruction(instructions, line_count)
            continue

        line_count += 1
        program_count += 1
        if not parser.has_more_lines(instructions, line_count):
            break
        instruction = parser.advance_instruction(instructions, line_count)


def parser_instructions(instructions: List[str], output_file: TextIOWrapper):
    program_count = 0
    next_address = 16
    symbol = "null"
    instruction = instructions[program_count]
    while True:
        instruction_type = parser.judge_instruction_type(instruction)
        if instruction_type == "C":
            dest, comp, jump = parser.parser_c_instruction(instruction)
            dest_converted = code.convert_dest(dest)
            comp_converted = code.convert_comp(comp)
            jump_converted = code.convert_jump(jump)
            instruction_assembled = "111" + comp_converted + dest_converted + jump_converted
        elif instruction_type == "A":
            symbol = parser.extract_symbol(instruction)
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol_table.contains_symbol(symbol):
                    address = symbol_table.get_address(symbol)
                else:
                    symbol_table.add_entry(symbol, next_address)
                    address = next_address
                    next_address += 1
            instruction_assembled = format(address, "016b")
        output_file.write(instruction_assembled + "\n")

        program_count += 1
        if not parser.has_more_lines(instructions, program_count):
            break
        instruction = parser.advance_instruction(instructions, program_count)


def assemble(assembly_file_path: str):
    with open(assembly_file_path, "r") as input_file:
        instructions = list(map(lambda instruction: instruction.removesuffix("\n").split("//")[0].strip(), input_file.readlines()))
    instructions = list(filter(lambda instruction: instruction, instructions))
    make_symbol_table(instructions)
    instructions = list(filter(lambda instruction: not (instruction.startswith("(") and instruction.endswith(")")), instructions))
    with open(assembly_file_path.removesuffix(".asm") + ".hack", "w") as output_file:
        parser_instructions(instructions, output_file)
    return instructions


def test_assembler(assembly_file_path: str):
    assembly_instructions = assemble(assembly_file_path)
    with open(assembly_file_path.removesuffix(".asm") + ".hack", "r") as hack_file:
        hack_instructions = hack_file.readlines()
    with open(assembly_file_path.removesuffix(".asm") + "-test" + ".hack", "r") as test_file:
        test_instructions = test_file.readlines()
    is_match_instructions = [hack_instruction == test_instruction for hack_instruction, test_instruction in zip(hack_instructions, test_instructions)]
    for i, is_match in enumerate(is_match_instructions):
        if not is_match:
            print(f"False in {i}: {assembly_instructions[i]}")
    print(all(is_match_instructions))


if __name__ == "__main__":
    test_assembler("./add/Add.asm")
    test_assembler("./max/MaxL.asm")
    test_assembler("./max/Max.asm")
    test_assembler("./rect/Rect.asm")
    test_assembler("./rect/RectL.asm")
    test_assembler("./pong/Pong.asm")
    test_assembler("./pong/PongL.asm")
