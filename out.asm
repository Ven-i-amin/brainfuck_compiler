section .data
    memory: times 30000 db 0

section .text
    global _start

_start:
    mov r15, memory

    add byte [r15], 40

    inc r15

    add byte [r15], 26

loop_0_start:
    cmp byte [r15], 0
    je loop_0_end

    dec r15

    inc byte [r15]

    inc r15

    dec byte [r15]

    jmp loop_0_start
loop_0_end:

    dec r15

    mov rax, 1
    mov rdi, 1
    mov rsi, r15
    mov rdx, 1
    syscall

    mov rax, 60
    mov rdi, 0
    syscall