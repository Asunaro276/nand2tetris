from typing import List


def judge_instruction_type(instruction: str) -> str:
    if instruction[0] == "@":
        return "A"
    elif instruction[0] + instruction[-1] == "()":
        return "L"
    else:
        return "C"


def has_more_lines(instructions: List[str], program_count: int) -> bool:
    return len(instructions) > program_count


def advance_instruction(instructions: List[str], program_count: int) -> str:
    return instructions[program_count]


def extract_symbol(instruction: str) -> str:
    return instruction.strip("@()")


def parser_c_instruction(instruction: str) -> str:
    instruction_symbols = instruction.split("=")
    if len(instruction_symbols) == 1:
        comp, jump = instruction_symbols[0].split(";")
        dest = "null"
    else:
        dest = instruction_symbols[0]
        comp_jump = instruction_symbols[1].split(";")
        comp = comp_jump[0]
        jump = comp_jump[1] if len(comp_jump) == 2 else "null"
    return dest, comp, jump


if __name__ == "__main__":
    print(parser_c_instruction("D=M"))
