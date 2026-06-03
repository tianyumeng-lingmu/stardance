# 群星之舞 编程语言学习指南

> 版本：v0.6 | 文件后缀：`.star`

---

## 目录

1. [你好，世界](#1-你好世界)
2. [注释](#2-注释)
3. [程序结构](#3-程序结构)
4. [变量与数据类型](#4-变量与数据类型)
5. [运算符](#5-运算符)
6. [流程控制](#6-流程控制)
7. [循环](#7-循环)
8. [跳转语句](#8-跳转语句)
9. [列表与字典](#9-列表与字典)
10. [面向对象](#10-面向对象)
11. [异常处理](#11-异常处理)
12. [内置函数](#12-内置函数)
13. [数据库操作](#13-数据库操作)
14. [常量与修饰符](#14-常量与修饰符)
15. [附录：运算符优先级](#15-附录运算符优先级)

---

## 1. 你好，世界

```
main {
    see("你好，世界！\n");
}
```

`see()` 是内置的打印函数，支持多参数：

```
see("答案 = ", 42, "\n");
// 输出: 答案 = 42
```

---

## 2. 注释

```
// 这是单行注释

/*
   这是多行注释
   可以写多行内容
*/
```

---

## 3. 程序结构

一个 `.star` 文件由 **两个可选块** 组成：

### 3.1 `start{}` 块 — 配置与常量声明

程序启动时执行，用于声明常量和初始化配置：

```
start {
    float PI = 3.1415926;
    str APP_NAME = "群星之舞";
    int MAX_COUNT = 100;
}
```

### 3.2 `main{}` 块 — 主程序逻辑

程序的入口逻辑：

```
main {
    see("程序启动\n");
}
```

可以同时使用两个块：

```
start {
    str GREETING = "欢迎！";
}

main {
    see(GREETING, "\n");   // 输出: 欢迎！
}
```

> 注意：`start` 中声明的常量在整个程序中可用，但不可修改。

---

## 4. 变量与数据类型

### 4.1 类型化变量声明

```
int a = 42;           // 整数
float b = 3.14;       // 浮点数
str c = "hello";      // 字符串
bool d = true;        // 布尔值（true / false）
list e = [1, 2, 3];   // 列表
```

### 4.2 `object` 通用声明

```
object x = 42;           // 任意类型
object z = new Person;   // 对象实例
```

> 注意：`var` 关键字不再支持，固定类型声明（`int`/`float`/`str`/`bool`/`list`/`object`）是唯一的方式。

### 4.3 类型字面量

| 类型 | 示例 |
|------|------|
| `int` | `42`, `-10`, `0` |
| `float` | `3.14`, `-0.5`, `100.0` |
| `str` | `"你好"`, `"hello"` |
| `bool` | `true`, `false` |
| `list` | `[1, 2, 3]`, `[a: 1, b: 2]` |
| `null` | `null` |

---

## 5. 运算符

### 5.1 算术运算符

```
int sum = 5 + 6;       // 加法 → 11
int diff = 10 - 3;     // 减法 → 7
int prod = 4 * 5;      // 乘法 → 20
float quot = 15 / 4;   // 除法 → 3.75
int rem = 17 % 5;      // 取模 → 2
```

### 5.2 自增 / 自减

```
int x = 5;

// 后缀（先取值，后自增）
see(x++);   // 输出 5, x 变为 6
see(x);     // 输出 6

// 前缀（先自增，后取值）
see(++x);   // 输出 7, x 变为 7
see(x);     // 输出 7
```

### 5.3 比较运算符

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `==` | 相等 | `5 == 5` → `true` |
| `!=` | 不等 | `5 != 3` → `true` |
| `===` | 严格相等（值和类型都需相等） | `5 === 5` → `true`, `5 === "5"` → `false` |
| `>` | 大于 | `5 > 3` → `true` |
| `<` | 小于 | `3 < 5` → `true` |
| `>=` | 大于等于 | `5 >= 5` → `true` |
| `<=` | 小于等于 | `3 <= 5` → `true` |
| `!>` | 不大于（等价于 `<=`） | `5 !> 10` → `true` |
| `!<` | 不小于（等价于 `>=`） | `10 !< 5` → `true` |

### 5.4 逻辑运算符（惰性求值）

```
bool r1 = true && false;    // AND → false（惰性：左边为 false 则不计算右边）
bool r2 = true || false;    // OR  → true（惰性：左边为 true 则不计算右边）
bool r3 = !true;            // NOT → false
```

**惰性求值示例**：
```
int counter = 0;
bool r = true || (counter++ > 0);   // counter++ 不会执行，counter 仍为 0
```

### 5.5 位运算符

```
int a = 1 << 3;           // 左移 → 8
int b = 16 >> 2;          // 右移 → 4
int c = -8 >>> 2;         // 无符号右移 → 1073741822
int d = 5 & 3;            // 按位与 → 1
int e = 5 | 3;            // 按位或 → 7
```

---

## 6. 流程控制

### 6.1 `if-else`

```
int score = 85;

if (score >= 90) {
    see("优秀\n");
} else if (score >= 60) {
    see("及格\n");
} else {
    see("不及格\n");
}
```

> 条件表达式必须返回 `bool` 类型。

### 6.2 `case-when`

```
int day = 3;

case (day) {
    when 1 {
        see("星期一\n");
    }
    when 2 {
        see("星期二\n");
    }
    when 3 {
        see("星期三\n");
    }
    else {
        see("未知日期\n");
    }
}
```

`else` 分支为可选，当所有 `when` 都不匹配时执行。

---

## 7. 循环

### 7.1 `while` 循环

```
int i = 1;
while (i <= 3) {
    see("i = ", i, "\n");
    i = i + 1;
}
```

### 7.2 `for` 循环（C 风格）

```
for (int i = 0; i < 5; i++) {
    see("i = ", i, "\n");
}

// 也可以不加初始化
int j = 0;
for (; j < 3; j++) {
    see("j = ", j, "\n");
}
```

### 7.3 `foreach` 循环（Python 风格）

遍历列表：
```
list colors = ["红", "绿", "蓝"];
foreach color in colors {
    see("颜色: ", color, "\n");
}
```

遍历字符串：
```
foreach ch in "ABC" {
    see("char: ", ch, "\n");
}
```

遍历字典：
```
list scores = ["小明": 95, "小红": 88];
foreach name in scores {
    see("学生: ", name, "\n");
}
// 字典遍历返回键名
```

---

## 8. 跳转语句

### 8.1 `break` — 退出当前循环

```
for (int i = 1; i <= 10; i++) {
    if (i == 6) {
        break;      // i=6 时跳出循环
    }
    see("i = ", i, "\n");
}
// 输出: 1 2 3 4 5
```

### 8.2 `continue` — 跳过本次循环

```
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue;   // i=3 时跳过本轮
    }
    see("i = ", i, "\n");
}
// 输出: 1 2 4 5
```

### 8.3 `cutdown` — 跳出所有嵌套循环

无论嵌套多少层循环，`cutdown` 直接结束所有循环：

```
for (int p = 1; p <= 5; p++) {
    for (int q = 1; q <= 5; q++) {
        if (p == 3 && q == 2) {
            cutdown;    // 退出所有循环！
        }
        see("q = ", q, "\n");
    }
    see("p = ", p, "\n");
}
// p=3, q=2 时全部退出，不会执行后续任何循环
```

---

## 9. 列表与字典

### 9.1 普通列表（数组）

```
list numbers = [1, 2, 3, 4, 5];
see(len(numbers));         // 输出: 5
see(numbers[0]);           // 输出: 1
numbers[0] = 99;           // 修改元素
```

### 9.2 字典风格列表

```
list person = [
    name: "小明",
    age: 18,
];
see(person.name);          // 输出: 小明
see(person.age);           // 输出: 18
person.age = 19;           // 修改属性
```

### 9.3 字符串键的字典

```
list scores = [
    "小明": 95,
    "小红": 88,
];
```

### 9.4 常用操作

```
list items = [10, 20, 30];
len(items);                 // 获取长度
```

---

## 10. 面向对象

### 10.1 定义命途（类）

```
life Person {
    // 属性
    str name;
    int age;

    // INIT 魔术方法（构造时自动调用）
    thing INIT(str name, int age) {
        this.name = name;
        this.age = age;
    }

    // 普通方法
    thing greet() {
        see("你好，我是 ", this.name, "\n");
    }

    // STR 魔术方法（自定义 see() 显示）
    thing STR() {
        return "Person(" + this.name + ")";
    }

    // LEN 魔术方法（自定义 len() 返回值）
    thing LEN() {
        return 1;
    }
}
```

### 10.2 创建与使用对象

```
object p = new Person("小明", 18);
p.greet();                    // 输出: 你好，我是 小明
see(p);                       // 调用 STR → 输出: Person(小明)
see(len(p));                  // 调用 LEN → 输出: 1
```

### 10.3 继承

使用 `extends` 或 `join` 关键字实现继承：

```
// 父类
life Animal {
    thing speak() {
        see("Animal speaks\n");
    }
}

// 子类继承
life Dog extends Animal {
    thing speak() {
        see("Dog barks\n");
    }
}

// join 等价于 extends
life Cat join Animal {
    thing speak() {
        see("Cat meows\n");
    }
}
```

### 10.4 `SUPPER` — 调用父类方法

```
life Parent {
    thing greet() {
        see("Parent::greet()\n");
    }
}

life Child extends Parent {
    thing greet() {
        SUPPER.greet();         // 调用父类方法
        see("Child::greet()\n");
    }
}
```

### 10.5 `new SUPPER()` — 在子类中创建父类实例

```
life Child extends Parent {
    thing makeParent() {
        object p = new SUPPER();
        return 1;
    }
}
```

### 10.6 多层继承链

```
life GrandParent {
    thing say() { see("GrandParent\n"); }
}
life Mid extends GrandParent {
    thing say() { SUPPER.say(); see("Mid\n"); }
}
life Young extends Mid {
    thing say() { SUPPER.say(); see("Young\n"); }
}
```

### 10.7 为 Object 添加通用方法

`Object` 是所有 life 的基类，可以为其添加方法：

```
life Object {
    thing myType() {
        return type_of(this);
    }
}
```

---

## 11. 异常处理

### 11.1 错误对象

内置 `Error` 类，支持继承：

```
var err = new Error;
err.code = "ER0001";
err.name = "MyError";
err.message = "出错了";
err.line = 42;
err.column = 10;
err.suggestion = "请检查输入";
```

### 11.2 抛出异常

```
throw err;
```

### 11.3 捕获异常

```
try {
    var err = new Error;
    err.code = "ER5001";
    err.name = "TestError";
    err.message = "测试异常";
    throw err;
} catch(e) {
    see("捕获到: ", e, "\n");
}
```

### 11.4 try-catch-finally

```
try {
    // 可能出错的代码
    throw someError;
} catch(e) {
    // 异常处理
    see("异常: ", e, "\n");
} finally {
    // 无论是否有异常都会执行
    see("清理操作\n");
}
```

### 11.5 自定义错误子类

```
life NetworkError join Error {
    thing INIT(code, msg, url) {
        this.code = code;
        this.name = "NetworkError";
        this.message = msg;
        this.url = url;
    }
}

try {
    throw new NetworkError("ER10001", "连接超时", "https://api.example.com");
} catch(e) {
    see("错误: ", e, "\n");
    see("URL: ", e.url, "\n");
}
```

---

## 12. 内置函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `see(...)` | 打印输出 | `see("hello", 42, "\n")` |
| `len(x)` | 获取长度 | `len([1,2,3])` → `3` |
| `type_of(x)` | 获取类型名称 | `type_of(42)` → `"int"` |
| `fix(x)` | 冻结列表为不可变 | `fix([1,2,3])` |
| `insert(prompt)` | 获取用户输入（返回字符串） | `str s = insert("输入: ")` |
| `int(x)` | 转换为整数 | `int("42")` → `42` |
| `float(x)` | 转换为浮点数 | `float("3.14")` → `3.14` |
| `str(x)` | 转换为字符串 | `str(42)` → `"42"` |
| `bool(x)` | 转换为布尔值 | `bool(1)` → `true`, `bool(0)` → `false` |
| `type(x)` | 获取类型描述 | `type(42)` → `<class:int>` |
| `ID(x)` | 获取对象唯一标识 | 返回 `<ID:0x...>` 格式 |

### 12.1 `insert()` — 用户输入

`insert()` 现在是一个**表达式**（返回值），而不是语句：

```
main {
    see("请输入名字: ");
    str name = insert("");       // 返回用户输入的字符串
    see("你好, ", name, "\n");

    // 配合 int()/float() 做数字输入
    see("请输入年龄: ");
    int age = int(insert(""));
    see("年龄: ", age, "\n");
}
```

### 12.2 `type()` — 获取类型描述

返回 `<class:类型名>` 格式的字符串：

```
str t1 = type(42);          // "<class:int>"
str t2 = type("hello");     // "<class:str>"
str t3 = type(true);        // "<class:bool>"

life MyClass {}
object obj = new MyClass();
str t4 = type(obj);         // "<class:MyClass>"
```

### 12.3 `ID()` — 获取对象唯一标识

返回每个对象的唯一内存地址标识：

```
str id1 = ID(42);       // "<ID:0x...>"
str id2 = ID(obj);      // "<ID:0x...>"
```

### 12.4 类型转换错误处理

`int()` / `float()` 在遇到非法转换时会抛出异常，可用 `try-catch` 捕获：

```
try {
    int bad = int("abc");
} catch (e) {
    see("转换失败: ", e.message, "\n");
}
```

---

## 13. 数据库操作

内置 SQLite 数据库支持：

```
// 创建表
db_create("users", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER");

// 插入数据
db_execute("INSERT INTO users (name, age) VALUES ('小明', 18)");

// 查询数据
object result = db_query("SELECT * FROM users");
see(result);
```

> 数据库文件自动保存为 `<脚本名>.db`。

---

## 14. 常量与修饰符

### 14.1 `start` 块常量

```
start {
    float PI = 3.1415926;
    str APP_NAME = "群星之舞";
}
```

常量在 `start{}` 中声明，全局可用，不可修改。

### 14.2 `fix` — 固定命途（冻结）

`fix` 命途不可被修改，但可被继承（子类不能 `new SUPPER()`）：

```
fix life FixedBase {
    thing STR() { return "[FixedBase]"; }
}

// fix 命途可被继承
life SubClass join FixedBase {
    // 但不能调用 new SUPPER()
}
```

### 14.3 `finish` — 完成命途（禁止继承）

`finish` 命途不可被任何类继承：

```
finish life FinalMath {
    thing STR() { return "不可被继承"; }
}

object fm = new FinalMath;
// life BadChild join FinalMath {}  // 错误！finish 命途禁止继承
```

### 14.4 `fix()` 函数 — 冻结列表/字典

```
list mutable = [10, 20, 30];
object fixed = fix(mutable);    // 冻结为不可变
```

---

## 15. 附录：运算符优先级

从低到高：

| 优先级 | 类别 | 运算符 | 结合性 |
|--------|------|--------|--------|
| 1（最低） | 赋值 | `=` | 右结合 |
| 2 | 逻辑 OR | `\|\|` | 左结合 |
| 3 | 逻辑 AND | `&&` | 左结合 |
| 4 | 按位 OR | `\|` | 左结合 |
| 5 | 按位 AND | `&` | 左结合 |
| 6 | 相等判断 | `==` `!=` `===` | 左结合 |
| 7 | 比较 | `<` `>` `<=` `>=` `!>` `!<` | 左结合 |
| 8 | 移位 | `<<` `>>` `>>>` | 左结合 |
| 9 | 加减 | `+` `-` | 左结合 |
| 10 | 乘除取模 | `*` `/` `%` | 左结合 |
| 11 | 一元 | `!` `-` `++x` `--x` | 右结合 |
| 12（最高） | 后缀 | `x++` `x--` | 左结合 |

---

> 群星之舞 — 让你的代码如群星般闪耀 ✨
