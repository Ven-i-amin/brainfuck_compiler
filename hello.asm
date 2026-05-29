section .data
    memory: times 30000 db 0

section .text
    global _start

_start:
    mov r15, memory

    add byte [r15], 7

loop_0_start:
    cmp byte [r15], 0
    je loop_0_end

    inc r15

    add byte [r15], 7

    dec r15

    dec byte [r15]

    jmp loop_0_start
loop_0_end:

    inc r15

    mov rax, 1
    mov rdi, 1
    mov rsi, r15
    mov rdx, 1
    syscall

    inc byte [r15]

    mov rax, 1
    mov rdi, 1
    mov rsi, r15
    mov rdx, 1
    syscall

    inc byte [r15]

    mov rax, 1
    mov rdi, 1
    mov rsi, r15
    mov rdx, 1
    syscall

    mov rax, 60
    mov rdi, 0
    syscall