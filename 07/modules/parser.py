from typing import List


COMMAND_TYPES = {
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "pop": "C_POP",
    "push": "C_PUSH",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL",
}


class Parser:
    def __init__(self, commands: List[str]) -> None:
        self.commands = commands
        self.program_count = 0
        self.current_command = commands[0].split()

    def has_more_commands(self) -> bool:
        return len(self.commands) - 1 > self.program_count

    def advance(self) -> None:
        self.program_count += 1
        self.current_command = self.commands[self.program_count].split()

    def judge_command_type(self) -> str:
        return COMMAND_TYPES[self.current_command[0]]

    def get_arg1(self, command_type: str) -> str:
        if command_type == "C_ARITHMETIC":
            return self.current_command[0]
        elif command_type == "C_RETURN":
            return None
        else:
            return self.current_command[1]

    def get_arg2(self, command_type: str) -> int:
        if command_type in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return self.current_command[2]
        else:
            return None
