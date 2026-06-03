#!/usr/bin/env python3
# 群星之舞 (Star Dance) CLI 入口 - 用于 PyInstaller 打包

import sys
import os

# 当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 当打包为 exe 时，__file__ 是 exe 路径，依赖文件在 _MEIPASS 目录
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = SCRIPT_DIR

# 确保能找到模块
sys.path.insert(0, BASE_DIR)

# 模块依赖由 PyInstaller 在 run_source() 中的局部导入自动检测


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


def _format_star_error(error_instance, source_lines: list = None) -> str:
    """格式化 StarException 显示"""
    # 尝试获取 Error 实例的各个字段
    code = "ER????"
    name = "UnknownError"
    msg = str(error_instance)
    line_no = 0
    col = 0
    suggestion = ""

    if hasattr(error_instance, 'get'):
        try:
            code = error_instance.get('code') or code
            name = error_instance.get('name') or name
            msg = error_instance.get('message') or msg
            line_no = error_instance.get('line') or 0
            col = error_instance.get('column') or 0
            suggestion = error_instance.get('suggestion') or ""
        except Exception:
            pass

    result = f"[{code}]-{name}：\n"
    if line_no:
        result += f"  line {line_no}：{msg}\n"
        # 显示源码行
        if source_lines and line_no > 0 and line_no <= len(source_lines):
            src_line = source_lines[line_no - 1].rstrip('\n')
            result += f"  {src_line}\n"
            if col:
                result += f"  {' ' * max(0, col - 1)}^\n"
    else:
        result += f"  {msg}\n"
    if suggestion:
        result += f"  建议：{suggestion}\n"
    return result


def run_source(source: str, source_name: str = "<stdin>"):
    """运行源码"""
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter, StarException

    source_lines = source.split('\n') if source else []

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
        except StarException as e:
            print(_format_star_error(e.error_instance, source_lines), file=sys.stderr)
            sys.exit(1)
        finally:
            interpreter.close()

    except SyntaxError as e:
        print(f"[ER0001]-SyntaxError：\n  {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        msg = str(e)
        if msg.startswith('['):
            print(msg, file=sys.stderr)
        else:
            print(f"[运行时错误] {msg}", file=sys.stderr)
        sys.exit(1)


def run_repl():
    """启动交互式 REPL"""
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter

    print("=" * 50)
    print("  群星之舞 (Star Dance) v0.6 - REPL")
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
                    if not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                        continue
                    print(f"  [错误] 语法不完整")
                    buffer = []
    finally:
        interpreter.close()


def main():
    # 设置 stdout 为 UTF-8 编码，支持 emoji 等 Unicode 字符
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print("用法: stardance <file.star>")
        print("       stardance               (启动 REPL)")
        print()
        run_repl()
    else:
        run_file(sys.argv[1])


if __name__ == '__main__':
    main()
