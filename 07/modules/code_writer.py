from typing import List


OPERATORS = {
    "add": "+",
    "sub": "-",
    "and": "&",
    "or": "|",
    "neg": "-",
    "not": "!",
    "eq": "EQ",
    "lt": "LT",
    "gt": "GT",
}

SEGMENTS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}


class CodeWriter:
    def __init__(self, commands) -> None:
        self.commands = commands
        self.program_count = 0
        self.current_command = commands[0]
        self.output_file = None
        self.file_name = None

    def set_file_name(self, file_name: str) -> None:
        self.output_file = open(file_name, "w")
        self.file_name = file_name.removesuffix(".asm").split("/")[-1]

    def write_arithmetic(self, operator: str) -> None:
        assembly_commands = []
        assembly_command1 = ["@SP", "A=M-1"]
        assembly_command2 = ["D=M", "A=A-1"]
        if operator in ["add", "sub", "and", "or"]:
            assembly_commands.extend(assembly_command1)
            assembly_commands.extend(assembly_command2)
            assembly_commands.append(f"M=M{OPERATORS[operator]}D")
            assembly_commands.extend([
                "@SP",
                "M=M-1",
                "A=M",
                "M=0",
            ])
        elif operator in ["neg", "not"]:
            assembly_commands.extend(assembly_command1)
            assembly_commands.append(f"M={OPERATORS[operator]}M")
        else:
            assembly_commands.extend(assembly_command1)
            assembly_commands.extend(assembly_command2)
            judge_command = [
                "D=M-D",
                f"@TRUE{self.program_count}",
                f"D;J{OPERATORS[operator]}",
                f"@FALSE{self.program_count}",
                "0;JMP",
                f"(FALSE{self.program_count})",
                "@SP",
                "A=M-1",
                "M=0",
                "A=A-1",
                "M=0",
                f"@CONTINUE{self.program_count}",
                "0;JMP",
                f"(TRUE{self.program_count})",
                "@SP",
                "A=M-1",
                "M=0",
                "A=A-1",
                "M=-1",
                f"(CONTINUE{self.program_count})",
                "@SP",
                "M=M-1",
            ]
            assembly_commands.extend(judge_command)
        self.program_count += 1
        assembly_commands = list(map(lambda command: command + "\n", assembly_commands))
        self.output_file.writelines(assembly_commands)

    def write_push_pop(self, command: List[str]) -> None:
        operator, segment, index = command
        assembly_commands = []
        if segment in ["local", "argument", "this", "that"]:
            assembly_commands.extend([
                f"@{SEGMENTS[segment]}",
                "D=M",
                f"@{index}",
                "D=D+A",
            ])
        elif segment == "pointer":
            assembly_commands.extend([
                "@3",
                "D=A",
                f"@{index}",
                "D=D+A",
            ])
        elif segment == "temp":
            assembly_commands.extend([
                "@5",
                "D=A",
                f"@{index}",
                "D=D+A",
            ])
        elif segment == "constant":
            assembly_commands.extend([
                f"@{index}",
                "D=A",
            ])
        elif segment == "static":
            assembly_commands.extend([
                f"@{self.file_name}.{index}",
                "D=A",
            ])

        if operator == "C_PUSH":
            if segment in ["constant"]:
                assembly_commands.extend([
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ])
            else:
                assembly_commands.extend([
                    "A=D",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ])
        elif operator == "C_POP":
            assembly_commands.extend([
                "@R5",
                "M=D",
                "@SP",
                "A=M-1",
                "D=M",
                "M=0",
                "@R5",
                "A=M",
                "M=D",
                "@SP",
                "M=M-1",
            ])
        self.program_count += 1
        assembly_commands = list(map(lambda command: command + "\n", assembly_commands))
        self.output_file.writelines(assembly_commands)

    def close(self):
        self.output_file.writelines([
            "(END)\n",
            "@END\n",
            "0;JMP",
        ])
        self.output_file.close()
