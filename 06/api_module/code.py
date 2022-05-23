DEST_DICT = {
    "null": 0b000,
    "M": 0b001,
    "D": 0b010,
    "A": 0b100,
}

COMP_DICT = {
    "0": 0b0101010,
    "1": 0b0111111,
    "-1": 0b0111010,
    "D": 0b0001100,
    "A": 0b0110000,
    "!D": 0b0001111,
    "!A": 0b0110011,
    "-D": 0b0001111,
    "-A": 0b0110011,
    "D+1": 0b0011111,
    "A+1": 0b0110111,
    "D-1": 0b0001110,
    "A-1": 0b0110010,
    "D+A": 0b0000010,
    "D-A": 0b0010011,
    "A-D": 0b0000111,
    "D&A": 0b0000000,
    "D|A": 0b0010101,
    "M": 0b1110000,
    "!M": 0b1110001,
    "-M": 0b1110011,
    "M+1": 0b1110111,
    "M-1": 0b1110010,
    "D+M": 0b1000010,
    "D-M": 0b1010011,
    "M-D": 0b1000111,
    "D&M": 0b1000000,
    "D|M": 0b1010101,
}

JUMP_DICT = {
    "null": 0b000,
    "JGT": 0b001,
    "JEQ": 0b010,
    "JGE": 0b011,
    "JLT": 0b100,
    "JNE": 0b101,
    "JLE": 0b110,
    "JMP": 0b111,
}


def convert_dest(dest: str) -> str:
    if dest == "null":
        dest_converted = DEST_DICT[dest]
        return format(dest_converted, "03b")
    dest_converted = 0
    for char in dest:
        dest_converted += DEST_DICT[char]
    return format(int(dest_converted), "03b")


def convert_comp(comp: str) -> str:
    comp_converted = COMP_DICT[comp]
    return format(comp_converted, "07b")


def convert_jump(jump: str) -> str:
    jump_converted = JUMP_DICT[jump]
    return format(jump_converted, "03b")


if __name__ == "__main__":
    print(convert_dest("MD"))
    print(convert_comp("0"))
    print(convert_jump("JNE"))
