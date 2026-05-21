section .data
    memory: times 30000 db 0

section .text
    global _start

_start:
    mov r15, memory      ; r15 = указатель на текущую ячейку памяти

    add byte [r15], 7

loop_0_start:
    cmp byte [r15], 0
    je loop_0_end

    inc r15

    add byte [r15], 10

    dec r15

    dec byte [r15]

    jmp loop_0_start
loop_0_end:

    inc r15

    add byte [r15], 2

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    dec r15

    add byte [r15], 3

loop_1_start:
    cmp byte [r15], 0
    je loop_1_end

    inc r15

    add byte [r15], 10

    dec r15

    dec byte [r15]

    jmp loop_1_start
loop_1_end:

    inc r15

    dec byte [r15]

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    add byte [r15], 7

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    add byte [r15], 3

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    dec r15

    add byte [r15], 8

loop_2_start:
    cmp byte [r15], 0
    je loop_2_end

    inc r15

    sub byte [r15], 10

    dec r15

    dec byte [r15]

    jmp loop_2_start
loop_2_end:

    inc r15

    inc byte [r15]

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    dec r15

    add byte [r15], 8

loop_3_start:
    cmp byte [r15], 0
    je loop_3_end

    inc r15

    add byte [r15], 10

    dec r15

    dec byte [r15]

    jmp loop_3_start
loop_3_end:

    inc r15

    add byte [r15], 7

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    sub byte [r15], 8

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    add byte [r15], 3

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    sub byte [r15], 6

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    sub byte [r15], 8

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    dec r15

    add byte [r15], 7

loop_4_start:
    cmp byte [r15], 0
    je loop_4_end

    inc r15

    sub byte [r15], 10

    dec r15

    dec byte [r15]

    jmp loop_4_start
loop_4_end:

    inc r15

    add byte [r15], 3

    mov rax, 1       ; sys_write
    mov rdi, 1       ; stdout
    mov rsi, r15     ; адрес текущей ячейки
    mov rdx, 1       ; длина 1 байт
    syscall

    mov rax, 60      ; sys_exit
    mov rdi, 0       ; код возврата 0
    syscall