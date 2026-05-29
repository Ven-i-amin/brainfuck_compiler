# test_x86_docker.py
import subprocess
import sys
import os

def test_x86_with_docker():
    """Тестирует x86 компилятор через Docker"""
    
    print("=" * 60)
    print("Тест x86 компилятора (через Docker)")
    print("=" * 60)
    
    # Проверка Docker
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Docker не установлен!")
        return False
    
    # Скрипт для выполнения внутри контейнера
    docker_script = """
    set -e
    python3 main.py compile-asm hello.bf -o hello.asm
    nasm -f elf64 hello.asm -o hello.o
    ld hello.o -o hello
    OUTPUT=$(./hello)
    if [ "$OUTPUT" = "Hello World!" ]; then
        echo "x86 компилятор работает!"
        exit 0
    else
        echo "Неправильный вывод: $OUTPUT"
        exit 1
    fi
    """
    
    # Запуск в Docker
    result = subprocess.run(
        ["docker", "run", "--rm", "-v", f"{os.getcwd()}:/app", "-w", "/app", "brainfuck-compiler", "bash", "-c", docker_script],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    return result.returncode == 0


if __name__ == "__main__":
    success = test_x86_docker()
    sys.exit(0 if success else 1)