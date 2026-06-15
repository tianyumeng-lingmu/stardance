# 群星之舞 (Star Dance)

「群星之舞」是一套中文命名的轻量级脚本语言，支持面向对象编程、类型化变量声明、完整运算符体系、异常处理、数据库操作等特性。语法风格融合了 C 与 Python，适合入门学习与快速脚本开发。

> **文件后缀**: `.star`

---

## ✨ 特性一览

| 特性 | 说明 |
|------|------|
| ✅ **类型系统** | `int` / `float` / `str` / `bool` / `list` / `object` |
| ✅ **运算符** | 算术 `+ - * / %`、自增自减 `++x x++`、比较 `> < == >= <= != === !> !<` |
| ✅ **位运算** | `<< >> >>> & \|` |
| ✅ **逻辑运算** | `&& \|\| !`（惰性短路求值） |
| ✅ **流程控制** | `if-else` / `case-when` / `while` / `for` / `foreach` |
| ✅ **跳转语句** | `break` / `continue` / `cutdown`（跳出所有嵌套循环） |
| ✅ **生成器** | `pause` / `next()` — 惰性求值、状态自动保存恢复 |
| ✅ **面向对象** | `life`（命途/类）、`thing`（方法）、继承、`SUPER`、多态 |
| ✅ **魔术方法** | `INIT`（构造）、`STR`（字符串）、`LEN`（长度） |
| ✅ **异常处理** | `throw` / `try-catch-finally`，自定义错误子类 |
| ✅ **集合类型** | 列表（数组 + 字典风格键值对） |
| ✅ **数据库** | 内置 SQLite 支持：`db_create` / `db_execute` / `db_query` |
| ✅ **常量** | `start{}` 块中声明全局常量 |
| ✅ **内置函数** | `type()` / `ID()` / `bool()` / `insert()` 表达式返回值 |
| ✅ **元语** | `fix`（冻结/不可变）、`finish`（禁止继承）、`join`（继承） |

---

## 🚀 快速开始

### 使用预编译的可执行文件

```bash
# 运行 .star 脚本
stardance hello.star

# 启动交互式 REPL
stardance
```

### 从源码运行

```bash
pip install -r requirements.txt
python main.py hello.star
```

### 从源码打包

```bash
pip install pyinstaller
cd star_dance
pyinstaller --clean --onefile --console --name stardance ^
  --add-data ".;." ^
  --hidden-import lexer --hidden-import parser ^
  --hidden-import interpreter --hidden-import runtime ^
  --hidden-import tokens --hidden-import ast_nodes ^
  --hidden-import environment --hidden-import database ^
  --hidden-import sqlite3 stardance.py
```

---

## 📝 快速示例

```
main {
    // Hello World
    see("你好，群星之舞！\n");

    // 变量声明
    int a = 42;
    float pi = 3.14;
    str name = "小明";
    bool ok = true;

    // 循环
    for (int i = 0; i < 3; i++) {
        see("计数: ", i, "\n");
    }

    // 面向对象
    life Person {
        thing INIT(str name) {
            this.name = name;
        }
        thing greet() {
            see("你好，我是 ", this.name, "\n");
        }
    }

    object p = new Person("小红");
    p.greet();
}
```

---

## 📦 项目结构

```
star_dance/
├── main.py            # 主入口
├── stardance.py       # CLI + REPL 入口（用于打包）
├── tokens.py          # 词法标记定义
├── lexer.py           # 词法分析器
├── parser.py          # 语法分析器
├── ast_nodes.py       # 抽象语法树节点
├── interpreter.py     # 解释执行器
├── environment.py     # 变量环境
├── database.py        # 数据库操作模块
├── runtime.py         # 运行时支持
├── *.star             # 示例与测试文件
└── dist/
    └── stardance.exe  # 可执行文件
```

---

## 📚 学习

完整语法教学请参阅 [`STUDY.md`](STUDY.md)。

---

## 📄 许可证

MIT License
