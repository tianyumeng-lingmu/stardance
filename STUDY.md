# 群星之舞 编程语言学习指南

> 版本：v2.4 | 文件后缀：`.star`

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
10. [函数声明](#10-函数声明)
11. [生成器（Generator）](#11-生成器generator)
12. [面向对象（life 命途）](#12-面向对象life-命途)
    - [抽象命途](#127-抽象命途)
13. [异常处理](#13-异常处理)
14. [内置函数](#14-内置函数)
15. [包系统（Package）](#15-包系统package)
16. [FFI（外部函数接口）](#16-ffi外部函数接口)
17. [常量与修饰符](#17-常量与修饰符)
18. [附录：运算符优先级](#18-附录运算符优先级)

---

## 1. 你好，世界

```
main {
    thing main() {
        see("你好，世界！\n");
    }
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

### 3.1 `start{}` 块 — 配置与包导入

程序启动时执行，用于导入包和声明常量：

```
start {
    use system;
    use rand;
    float PI = 3.1415926;
    str APP_NAME = "群星之舞";
}
```

### 3.2 `main{}` 块 — 主程序（main 命途）

`main{}` 是程序的入口容器，内部必须包含 `thing main()` 作为实际主程序入口：

```
main {
    thing main() {
        see("程序启动\n");
    }
}
```

同时使用两个块：

```
start {
    use system;
}

main {
    thing main() {
        int pid = system.GetCurrentProcessId();
        see("PID = ", pid, "\n");
    }
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

> 固定类型声明（`int`/`float`/`str`/`bool`/`list`/`object`）是唯一的方式，`var` 关键字已不再使用。

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
int idiv = 17 /^ 5;    // 整除 → 3（截断小数）
```

> 除法（`/`）始终返回 `float` 类型。整除（`/^`）返回截断后的整数。

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
| `>` | 大于 | `5 > 3` → `true` |
| `<` | 小于 | `3 < 5` → `true` |
| `>=` | 大于等于 | `5 >= 5` → `true` |
| `<=` | 小于等于 | `3 <= 5` → `true` |
| `!>` | 不大于（等价于 `<=`） | `5 !> 10` → `true` |
| `!<` | 不小于（等价于 `>=`） | `10 !< 5` → `true` |

### 5.4 `has` 运算符

`has` 用于检查字符串是否包含子串：

```
str s = "Hello World";
if (s has "World") {
    see("包含 World\n");
}
```

### 5.5 逻辑运算符（惰性求值）

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

### 5.6 位运算符

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

### 9.4 字典下标访问

字典风格的列表支持字符串和整数下标两种访问方式：

```
object scores = [
    "小明": 95,
    "小红": 88,
];
see(scores["小明"]);       // 95  ← 字符串下标
see(scores["小红"]);       // 88

// 支持赋值
scores["小明"] = 100;

// 也支持整数下标（用于 str_split 等返回的结果）
object parts = str_split("a,b,c", ",");
see(parts[0]);               // "a"  ← 整数下标
see(parts["0"]);             // "a"  ← 字符串下标（等价）
```

> **注意：** 字符串索引 `s[0]` 用于获取字符串的第 0 个字符。

---

## 10. 函数声明

### 10.1 `thing` 关键字

所有函数使用 `thing` 关键字声明：

```
thing double(x) {
    return x * 2;
}

thing greet(name) {
    see("你好, ", name, "\n");
    return 0;
}
```

### 10.2 `return()` / `pause` 要求

**所有模块级 `thing` 函数必须有 `return()` 或 `pause` 语句**（二选一）：

```
// ✅ 正确 — 普通函数用 return
thing calc(x) {
    return x * 2;
}

// ✅ 正确 — 返回 null
thing doNothing() {
    return(null);
}

// ✅ 正确 — 生成器函数用 pause
thing counter(n) {
    var i = 0;
    while (i < n) {
        pause i;
        i = i + 1;
    }
    return(null);
}

// ❌ 编译错误 — 缺少 return() 或 pause
thing bad() {
    int x = 1;
    // 没有 return() 也没有 pause！
}
```

### 10.3 模块级函数

`main` 命途外部的 `thing` 是模块级函数，可在 `main` 内部引用：

```
thing add(a, b) {
    return a + b;
}

main {
    thing main() {
        int r = add(3, 4);
        see("3 + 4 = ", r, "\n");
    }
}
```

### 10.4 静态函数

使用 `static thing` 声明，通常用于 `life` 命途中的工厂方法：

```
static thing create(n) {
    return new MyClass(n);
}
```

---

## 11. 生成器（Generator）

使用 `pause` 关键字创建生成器函数。生成器可以暂停执行并返回一个值，下次调用时从暂停处继续。

### 11.1 基本用法

```
thing counter(n) {
    var i = 0;
    while (i < n) {
        pause i;        // 暂停，返回 i 的值
        i = i + 1;
    }
    return(null);       // 生成器耗尽
}

main {
    thing main() {
        var gen = counter(5);
        var v = next(gen);   // 0
        see(v);
        v = next(gen);       // 1
        see(v);
        v = next(gen);       // 2
        see(v);
        v = next(gen);       // null（已耗尽）
        see(v);
    }
}
```

### 11.2 工作原理

- 包含 `pause` 语句的函数自动成为**生成器函数**
- 调用生成器函数时**不执行函数体**，而是返回一个 `generator` 对象
- `next(gen)` 首次启动生成器，之后每次恢复至上一次 `pause` 的位置继续执行
- 生成器耗尽（执行到 `return` 或函数末尾）后，`next()` 返回 `null`

### 11.3 实现 range 生成器

```
thing myrange(from_val, to_val) {
    var i = from_val;
    while (i < to_val) {
        pause i;
        i = i + 1;
    }
    return(null);
}

main {
    thing main() {
        var gen = myrange(3, 8);
        var v = null;
        while ((v = next(gen)) != null) {
            see(v, " ");
        }
        // 输出: 3 4 5 6 7
    }
}
```

### 11.4 规则

- 生成器函数必须有 `pause` 语句（至少一个）
- 生成器函数也必须有 `return()`（用于标记耗尽，通常返回 `null`）
- `next()` 是唯一与生成器交互的方式
- 生成器的局部变量状态在 `pause` 时自动保存和恢复

---

## 12. 面向对象（life 命途）

### 12.1 定义命途（类）

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

> ⚠️ 在包含 `main{}` 的文件中，`life` 声明必须嵌套在 `main{}` 内部。没有 `main{}` 的文件（如包文件）中，`life` 可在顶级声明。

### 12.2 创建与使用对象

```
object p = new Person("小明", 18);
p.greet();                    // 输出: 你好，我是 小明
see(p);                       // 调用 STR → 输出: Person(小明)
```

### 12.3 继承

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

life Cat join Animal {
    thing speak() {
        see("Cat meows\n");
    }
}
```

### 12.4 `SUPER` — 调用父类方法

```
life Parent {
    thing greet() {
        see("Parent::greet()\n");
    }
}

life Child extends Parent {
    thing greet() {
        SUPER.greet();         // 调用父类方法
        see("Child::greet()\n");
    }
}
```

### 12.5 `fix` — 固定命途（冻结）

`fix` 命途不可被修改，但可被继承（子类不能 `new SUPER()`）：

```
fix life FixedBase {
    thing STR() { return "[FixedBase]"; }
}
```

### 12.6 `finish` — 完成命途（禁止继承）

`finish` 命途不可被任何类继承：

```
finish life FinalMath {
    thing STR() { return "不可被继承"; }
}

// life BadChild join FinalMath {}  // 错误！finish 命途禁止继承
```

### 12.7 抽象命途

当命途中的所有 `thing` 方法体均为 `pass` 时，该命途视为**抽象命途**。抽象命途不能被实例化：

```
life Animal {
    thing speak() { pass; }     // 抽象方法
    thing walk()  { pass; }     // 抽象方法
}

// object a = new Animal();     // 错误 18：无法实例化抽象命途
```

继承抽象命途的子类必须实现所有抽象方法，否则 `new` 也会报错误 18：

```
life Dog join Animal {
    thing speak() {
        see("bark\n");           // 实现 speak
    }
    thing walk() { pass; }      // 仍可为 pass，继续留给子类
}

life Puppy join Dog {
    thing walk() {
        see("walk\n");           // 实现 walk
    }
}

main {
    thing main() {
        object p = new Puppy("Buddy");  // OK：所有抽象方法已实现
        p.speak();              // bark
        p.walk();               // walk
    }
}
```

规则：
- 不需要 `abstract` 关键字，全 `pass` 方法体自动判定
- 抽象命途不能 `new`
- 抽象命途不能 `join` 抽象命途
- 子类未实现全部抽象方法也不能 `new`
- 非抽象命途可 `new`，未实现且无继承的方法调用时返回 `null`
- `pass` 在非抽象命途中 = 显性留白，保留父类版本
- 错误码：**18**

---

## 13. 异常处理

### 13.1 错误对象

内置 `Error` 类：

```
object err = new Error;
err.code = "ER0001";
err.name = "MyError";
err.message = "出错了";
err.line = 42;
err.column = 10;
err.suggestion = "请检查输入";
```

### 13.2 抛出异常

```
throw err;
```

### 13.3 捕获异常

```
try {
    object err = new Error;
    err.code = "ER5001";
    err.name = "TestError";
    err.message = "测试异常";
    throw err;
} catch(e) {
    see("捕获到: ", e, "\n");
}
```

### 13.4 try-catch-finally

```
try {
    throw someError;
} catch(e) {
    see("异常: ", e, "\n");
} finally {
    see("清理操作\n");
}
```

---

## 14. 内置函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `see(...)` | 打印输出 | `see("hello", 42, "\n")` |
| `len(x)` | 获取长度 | `len([1,2,3])` → `3` |
| `insert(prompt)` | 获取用户输入 | `str s = insert("输入: ")` |
| `int(x)` | 转换为整数 | `int("42")` → `42` |
| `float(x)` | 转换为浮点数 | `float("3.14")` → `3.14` |
| `str(x)` | 转换为字符串 | `str(42)` → `"42"` |
| `bool(x)` | 转换为布尔值 | `bool(1)` → `true` |
| `type(x)` | 获取类型描述 | `type(42)` → `<class:int>` |
| `fix(x)` | 冻结列表为不可变 | `fix([1,2,3])` |
| `next(gen)` | 获取生成器下一个值 | `next(gen)` → 值 或 `null` |
| `todo(msg?)` | 未实现警告（W18） | `todo("后续实现")` → 输出到 stderr |

### 14.1 JSON / 文件 I/O

| 函数 | 说明 | 示例 |
|------|------|------|
| `json_encode(obj)` | 将对象编码为 JSON 字符串 | `json_encode(['a':1])` → `{"a":1}` |
| `json_decode(str)` | 将 JSON 字符串解码为对象 | `json_decode('{"a":1}')` |
| `file_read(path)` | 读取文件内容 | `str content = file_read("data.json")` |
| `file_write(path, content)` | 写入文件 | `file_write("out.txt", "hello")` |
| `file_exists(path)` | 检查文件是否存在 | `file_exists("test.txt")` → `true` |

**示例：读取 JSON 配置文件**
```
str data = file_read("config.json");
object cfg = json_decode(data);
see(cfg["host"], cfg["port"]);
```

### 14.2 字符串函数

| 函数 | 说明 | 示例 |
|------|------|------|
| `str_at(s, idx)` | 取第 idx 个字符 | `str_at("Hello", 1)` → `"e"` |
| `str_sub(s, start, end)` | 取子串 | `str_sub("Hello", 1, 4)` → `"ell"` |
| `str_find(s, pattern)` | 查找子串位置 | `str_find("Hello", "ll")` → `2` |
| `str_contains(s, pattern)` | 是否包含子串 | `str_contains("Hello", "ll")` → `true` |
| `str_trim(s)` | 去除两端空白 | `str_trim("  hi  ")` → `"hi"` |
| `str_upper(s)` | 转大写 | `str_upper("hello")` → `"HELLO"` |
| `str_lower(s)` | 转小写 | `str_lower("HELLO")` → `"hello"` |
| `str_split(s, delimiter)` | 按分隔符分割 | `str_split("a,b,c", ",")` → `{"0":"a","1":"b","2":"c"}` |

**字符串索引（从 0 开始）：**
```
str s = "Hello";
see(s[0]);          // "H"
see(s[4]);          // "o"
```

---

## 15. 包系统（Package）

### 15.1 导入包

`use` 关键字在 `start{}` 中导入包：

```
start {
    use system;
    use rand;
}
```

### 15.2 命名空间调用

包函数必须使用 `包名.函数名()` 方式调用，不会污染全局命名空间：

```
start {
    use system;
    use rand;
}

main {
    thing main() {
        int pid = system.GetCurrentProcessId();  // system 包
        int n = rand.next();                     // rand 包
    }
}
```

### 15.3 system 包

基于 FFI 调用 Windows API，提供系统级功能：

| 函数 | 说明 |
|------|------|
| `system.GetTickCount64()` | 系统运行时间（毫秒） |
| `system.GetCurrentProcessId()` | 当前进程 ID |
| `system.GetCurrentThreadId()` | 当前线程 ID |
| `system.GetLastError()` | 最后错误码 |
| `system.IsDebuggerPresent()` | 调试器检测 |
| `system.GetProcessVersion(pid)` | 进程版本 |
| `system.SetConsoleTitle(title)` | 设置控制台标题 |
| `system.GetStdHandle(dev)` | 获取标准句柄 |
| `system.Sleep(ms)` | 休眠指定毫秒数 |
| `system.Beep(freq, ms)` | 蜂鸣 |
| `system.exit(code)` | 退出进程 |
| `system.srandom(seed)` | 设置随机数种子 |
| `system.random()` | 随机整数 0..32767 |
| `system.random_range(min, max)` | 范围随机整数 |
| `system.uptime()` | 系统运行秒数 |

```
start { use system; }

main {
    thing main() {
        int up = system.uptime();
        see("已运行 ", up, " 秒\n");
        system.Sleep(1000);
        system.exit(0);
    }
}
```

### 15.4 rand 包

随机数生成专用包：

| 函数 | 说明 |
|------|------|
| `rand.seed()` | 基于时间自动种子 |
| `rand.seed_with(val)` | 自定义种子（可重复） |
| `rand.next()` | 随机整数 0..32767 |
| `rand.range(min, max)` | 范围随机整数 [min, max] |
| `rand.unit()` | 0.0..1.0 随机浮点数 |

```
start { use rand; }

main {
    thing main() {
        rand.seed();
        int dice = rand.range(1, 6);
        float u = rand.unit();
        see("骰子: ", dice, " 随机: ", u, "\n");
    }
}
```

### 15.5 webstar 包

HTTP 服务器包：

```
start { use webstar; }

main {
    thing main() {
        int srv = webstar.web_start(8080);
        int conn = webstar.web_accept(srv);
        str line = webstar.web_read_line(conn);
        // 处理请求...
        str resp = webstar.web_response(200, "text/html", "<h1>OK</h1>");
        webstar.web_send(conn, resp);
        webstar.web_close(conn);
        webstar.web_close(srv);
    }
}
```

---

## 16. FFI（外部函数接口）

StarDance 支持直接调用 DLL 中的 C 函数：

### 16.1 基础用法

```
int k = ffi_load("kernel32.dll");                    // 加载 DLL
int pid = ffi_call(k, "GetCurrentProcessId", "i");   // 调用函数（返回 int）
ffi_call(k, "Beep", "v", 800, 200);                  // void 函数
ffi_free(k);                                          // 释放 DLL
```

### 16.2 返回类型

`ffi_call` 第三个参数指定返回类型：

| 代码 | 含义 |
|------|------|
| `"i"` | 返回 int（32/64 位整数） |
| `"f"` | 返回 float（double） |
| `"v"` | void，不返回值 |

### 16.3 参数列表

`ffi_call` 从第 4 个参数开始都是传给 DLL 函数的参数：

```
// kernel32!GetTickCount64() — 无参数，返回 int
int ms = ffi_call(k, "GetTickCount64", "i");

// kernel32!Beep(freq: DWORD, ms: DWORD) — 两个参数，void 返回
ffi_call(k, "Beep", "v", 800, 200);

// msvcrt!rand() — 无参数，返回 int
int m = ffi_load("msvcrt.dll");
int r = ffi_call(m, "rand", "i");
```

### 16.4 完整示例

```
start {
    use rand;
}

main {
    thing main() {
        int k = ffi_load("kernel32.dll");
        int ms = ffi_call(k, "GetTickCount64", "i");
        see("系统已运行 ", ms / 1000, " 秒\n");
        ffi_free(k);

        rand.seed_with(ms);
        see("随机数: ", rand.next(), "\n");
    }
}
```

---

## 17. 常量与修饰符

### 17.1 `start` 块常量

```
start {
    float PI = 3.1415926;
    str APP_NAME = "群星之舞";
}
```

常量在 `start{}` 中声明，全局可用，不可修改。

### 17.2 `fix()` 函数 — 冻结列表/字典

```
list mutable = [10, 20, 30];
object fixed = fix(mutable);    // 冻结为不可变
```

---

## 18. 附录：运算符优先级

从低到高：

| 优先级 | 类别 | 运算符 | 结合性 |
|--------|------|--------|--------|
| 1（最低） | 赋值 | `=` | 右结合 |
| 2 | 逻辑 OR | `\|\|` | 左结合 |
| 3 | 逻辑 AND | `&&` | 左结合 |
| 4 | 按位 OR | `\|` | 左结合 |
| 5 | 按位 AND | `&` | 左结合 |
| 6 | 相等判断 | `==` `!=` | 左结合 |
| 7 | 比较 | `<` `>` `<=` `>=` `!>` `!<` | 左结合 |
| 8 | 包含 | `has` | 左结合 |
| 9 | 移位 | `<<` `>>` `>>>` | 左结合 |
| 10 | 加减 | `+` `-` | 左结合 |
| 11 | 乘除取模 | `*` `/` `%` | 左结合 |
| 12 | 一元 | `!` `-` `++x` `--x` | 右结合 |
| 13（最高） | 后缀 | `x++` `x--` | 左结合 |

---

> 群星之舞 — 让你的代码如群星般闪耀 ✨
