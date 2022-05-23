from code_writer import CodeWriter
from parser import Parser


class BackendCompiler:
    def __init__(self, input_path: str) -> None:
        self.path_name = input_path.removesuffix(".vm")
        with open(input_path) as input_file:
            commands = list(map(lambda instruction: instruction.removesuffix("\n").split("//")[0].strip(), input_file.readlines()))
        commands = list(filter(lambda command: command, commands))
        self.parser = Parser(commands=commands)
        self.code_writer = CodeWriter(commands=commands)

    def compile(self):
        self.code_writer.set_file_name(file_name=self.path_name + ".asm")
        while True:
            command_type = self.parser.judge_command_type()
            arg1 = self.parser.get_arg1(command_type)
            arg2 = self.parser.get_arg2(command_type)
            if command_type == "C_ARITHMETIC":
                operator = arg1
                self.code_writer.write_arithmetic(operator)
            else:
                parsed_command = [command_type, arg1, arg2]
                self.code_writer.write_push_pop(parsed_command)
            if not self.parser.has_more_commands():
                break
            self.parser.advance()
        self.code_writer.close()


if __name__ == "__main__":
    file_names = [
        "StackArithmetic/SimpleAdd/SimpleAdd.vm",
        "StackArithmetic/StackTest/StackTest.vm",
        "MemoryAccess/BasicTest/BasicTest.vm",
        "MemoryAccess/PointerTest/PointerTest.vm",
        "MemoryAccess/StaticTest/StaticTest.vm"
    ]
    for file_name in file_names:
        compiler = BackendCompiler(file_name)
        compiler.compile()
