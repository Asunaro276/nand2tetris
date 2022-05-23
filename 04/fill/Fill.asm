// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @KBD
    D=A
    @i
    M=D-1
    @KBD
    D=M
    @FILL_BLACK_PREPROCESS
    D;JNE
    @FILL_WHITE_PREPROCESS
    D;JEQ
(FILL_WHITE_PREPROCESS)
    @SCREEN
    D=A
    @j
    M=D
    @SCREEN
    M=0
(FILL_WHITE)
    @j
    M=M+1
    A=M
    M=0
    @i
    D=M
    A=D
    D=M
    @END
    D;JGT
    @FILL_WHITE
    0;JMP
(FILL_BLACK_PREPROCESS)
    @SCREEN
    D=A
    @j
    M=D
    @SCREEN
    M=1
(FILL_BLACK)
    @j
    M=M+1
    A=M
    M=0
    @i
    D=M
    A=D
    D=M
    @END
    M;JEQ
    @FILL_BLACK
    0;JMP
(END)
    @END
    0;JMP