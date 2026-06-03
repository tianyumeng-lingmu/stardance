#!/usr/bin/env python3
# 群星之舞 (Star Dance) - 编程语言解释器入口

import sys
import os

# 确保能找到 star_dance 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_file(file_path: str):
    """运行 .star 文件"""
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}", file=sys.stderr)
        sys.exit(1)

    if not file_path.endswith('.star'):
        print(f"错误: 文件必须是 .star 后缀: {file_path}", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    run_source(source, file_path)


def run_source(source: str, source_name: str = "<stdin>"):
    """运行源码"""
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter

    try:
        # 1. 词法分析
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 2. 语法分析
        parser = Parser(tokens)
        ast = parser.parse()

        # 3. 解释执行
        db_path = os.path.splitext(source_name)[0] + '.db' if source_name != "<stdin>" else None
        interpreter = Interpreter()
        try:
            interpreter.interpret(ast, db_path)
        finally:
            interpreter.close()

    except Exception as e:
        print(f"{e}", file=sys.stderr)
        sys.exit(1)


def run_repl():
    """启动交互式 REPL"""
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter

    print("=" * 50)
    print("  群星之舞 (Star Dance) v0.3 - REPL")
    print("  输入 .exit 退出")
    print("=" * 50)

    interpreter = Interpreter()
    try:
        buffer = []
        while True:
            try:
                line = input(">>> " if not buffer else "... ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if line.strip() == '.exit':
                break

            buffer.append(line)

            # 尝试解析执行
            source = '\n'.join(buffer)
            if source.strip():
                try:
                    lexer = Lexer(source)
                    tokens = lexer.tokenize()
                    parser = Parser(tokens)
                    ast = parser.parse()
                    interpreter.interpret(ast)
                    buffer = []
                except Exception:
                    # 可能是不完整的输入，继续等待
                    if not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                        continue
                    print(f"  [错误] 语法不完整")
                    buffer = []
    finally:
        interpreter.close()


def main():
    if len(sys.argv) < 2:
        print("用法: python -m star_dance.main <file.star>")
        print("       python -m star_dance.main  (启动 REPL)")
        print()
        run_repl()
    else:
        run_file(sys.argv[1])


if __name__ == '__main__':
    main()
