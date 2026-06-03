// 群星之舞 v0.6 — 运算符、控制流、位运算测试

main {
    see("=== 群星之舞 v0.6 测试 ===\n\n");
    // ════════════════════════════════════════════
    // 测试1：int/float/bool 类型变量声明
    // ════════════════════════════════════════════
    see("--- 测试1：类型化变量声明 ---\n");
    int a = 42;
    float b = 3.14;
    str c = "hello";
    bool d = true;
    see("a = ", a, " (should be 42)\n");
    see("b = ", b, " (should be 3.14)\n");
    see("c = ", c, " (should be hello)\n");
    see("d = ", d, " (should be true)\n\n");

    // ════════════════════════════════════════════
    // 测试2：算术运算 int a = 5 + 6 语法
    // ════════════════════════════════════════════
    see("--- 测试2：算术运算 ---\n");
    int sum = 5 + 6;
    see("5 + 6 = ", sum, " (should be 11)\n");
    int sub = 10 - 3;
    see("10 - 3 = ", sub, " (should be 7)\n");
    int mul = 4 * 5;
    see("4 * 5 = ", mul, " (should be 20)\n");
    float div = 15 / 4;
    see("15 / 4 = ", div, " (should be 3.75)\n");
    int mod = 17 % 5;
    see("17 %% 5 = ", mod, " (should be 2)\n\n");

    // ════════════════════════════════════════════
    // 测试3：i++ / ++i / i-- / --i
    // ════════════════════════════════════════════
    see("--- 测试3：自增自减 ---\n");
    int x = 5;
    see("x++: ", x++, " (should be 5, then x=6)\n");
    see("x after: ", x, " (should be 6)\n");
    see("++x: ", ++x, " (should be 7)\n");
    see("x after: ", x, " (should be 7)\n");
    int y = 10;
    see("y--: ", y--, " (should be 10, then y=9)\n");
    see("after: ", y, " (should be 9)\n");
    see("--y: ", --y, " (should be 8)\n\n");

    // ════════════════════════════════════════════
    // 测试4：位运算 << >> >>> & |
    // ════════════════════════════════════════════
    see("--- 测试4：位运算 ---\n");
    int v1 = 1 << 3;
    see("1 << 3 = ", v1, " (should be 8)\n");
    int v2 = 16 >> 2;
    see("16 >> 2 = ", v2, " (should be 4)\n");
    int v3 = -8 >>> 2;
    see("-8 >>> 2 = ", v3, " (should be 1073741822)\n");
    int v4 = 5 & 3;
    see("5 & 3 = ", v4, " (should be 1)\n");
    int v5 = 5 | 3;
    see("5 | 3 = ", v5, " (should be 7)\n\n");

    // ════════════════════════════════════════════
    // 测试5：bool 类型 true/false 和 if-else
    // ════════════════════════════════════════════
    see("--- 测试5：if-else ---\n");
    int score = 85;
    if (score >= 90) {
        see("优秀\n");
    } else {
        if (score >= 80) {
            see("良好 (should be this)\n");
        } else {
            see("继续努力\n");
        }
    }

    // bool 条件
    bool is_ok = true;
    if (is_ok) {
        see("is_ok = true (should be this)\n");
    }
    if (!is_ok) {
        see("is_ok = false (should NOT print)\n");
    }

    // 复合条件
    int age = 20;
    if (age >= 18 && age <= 60) {
        see("成年人 (should be this)\n\n");
    }

    // ════════════════════════════════════════════
    // 测试6：惰性求值 && ||
    // ════════════════════════════════════════════
    see("--- 测试6：惰性求值 ---\n");
    bool lazy1 = false && see("不应打印\n") == "";
    see("lazy1 = ", lazy1, " (should be false, 右侧未执行)\n");
    bool lazy2 = true || see("不应打印\n") == "";
    see("lazy2 = ", lazy2, " (should be true, 右侧未执行)\n\n");

    // ════════════════════════════════════════════
    // 测试7：while 循环
    // ════════════════════════════════════════════
    see("--- 测试7：while 循环 ---\n");
    int i = 1;
    while (i <= 3) {
        see("i = ", i, "\n");
        i++;
    }
    see("\n");

    // ════════════════════════════════════════════
    // 测试8：for 循环 (类C)
    // ════════════════════════════════════════════
    see("--- 测试8：for 循环 ---\n");
    for (int j = 1; j <= 3; j++) {
        see("j = ", j, "\n");
    }
    see("\n");

    // ════════════════════════════════════════════
    // 测试9：foreach 循环
    // ════════════════════════════════════════════
    see("--- 测试9：foreach 循环 ---\n");
    list colors = ["红", "绿", "蓝"];
    foreach c in colors {
        see("颜色: ", c, "\n");
    }
    see("\n");

    // foreach 字符串
    str word = "AB";
    foreach ch in word {
        see("char: ", ch, "\n");
    }
    see("\n");

    // ════════════════════════════════════════════
    // 测试10：break / continue
    // ════════════════════════════════════════════
    see("--- 测试10：break / continue ---\n");
    for (int k = 1; k <= 10; k++) {
        if (k == 3) {
            see("  continue at 3\n");
            continue;
        }
        if (k == 6) {
            see("  break at 6\n");
            break;
        }
        see("  k = ", k, "\n");
    }
    see("\n");

    // ════════════════════════════════════════════
    // 测试11：cutdown — 跳出所有嵌套循环
    // ════════════════════════════════════════════
    see("--- 测试11：cutdown ---\n");
    for (int p = 1; p <= 5; p++) {
        see("外层 p = ", p, "\n");
        for (int q = 1; q <= 5; q++) {
            if (p == 3 && q == 2) {
                see("  cutdown at (p=", p, ", q=", q, ")\n");
                cutdown;
            }
            see("  q = ", q, "\n");
        }
    }
    see("cutdown 后到这里\n\n");

    // ════════════════════════════════════════════
    // 测试12：case-when
    // ════════════════════════════════════════════
    see("--- 测试12：case-when ---\n");
    int day = 3;
    case (day) {
        when 1 {
            see("星期一\n");
        }
        when 2 {
            see("星期二\n");
        }
        when 3 {
            see("星期三 (should be this)\n");
        }
        when 4 {
            see("星期四\n");
        }
        when 5 {
            see("星期五\n");
        }
        else {
            see("周末\n");
        }
    }

    // case-when else 分支
    int day2 = 99;
    case (day2) {
        when 1 {
            see("星期一\n");
        }
        else {
            see("未知日期 (should be this)\n\n");
        }
    }

    // ════════════════════════════════════════════
    // 测试13：惰性求值验证（副作用不应发生）
    // ════════════════════════════════════════════
    see("--- 测试13：惰性求值副作用验证 ---\n");
    int counter = 0;
    // 让右侧表达式包含自增操作
    // 如果 bool_t1 为 true，右侧不应执行
    bool bool_t1 = true;
    if (bool_t1 || (counter++) == 0) {
        see("惰性 OR: counter = ", counter, " (should be 0)\n");
    }
    bool bool_f1 = false;
    if (bool_f1 && (counter++) == 0) {
        see("不应执行\n");
    }
    see("惰性 AND: counter = ", counter, " (should be 0, counter++ 未执行)\n\n");

    // ════════════════════════════════════════════
    // 测试14：混合表达式
    // ════════════════════════════════════════════
    see("--- 测试14：混合表达式 ---\n");
    int expr1 = (2 + 3) * 4;
    see("(2+3)*4 = ", expr1, " (should be 20)\n");

    bool cmp1 = 10 > 5 && 3 < 7;
    see("10>5 && 3<7 = ", cmp1, " (should be true)\n");

    bool cmp2 = 10 > 5 || 10 < 3;
    see("10>5 || 10<3 = ", cmp2, " (should be true)\n");

    bool cmp3 = !(10 > 5);
    see("!(10>5) = ", cmp3, " (should be false)\n\n");

    // ════════════════════════════════════════════
    // 测试15：foreach 遍历字典（使用已有 [...] 字典语法）
    // ════════════════════════════════════════════
    see("--- 测试15：foreach 字典 ---\n");
    list scores = ["小明": 95, "小红": 88, "小刚": 73];
    foreach name in scores {
        see("学生: ", name, "\n");
    }
    see("\n");

    // ════════════════════════════════════════════
    // 测试16：补充比较运算符 ===，！>，！<
    // ════════════════════════════════════════════
    see("--- 测试16：补充比较运算符 ---\n");

    // === 严格相等
    bool s1 = (5 === 5);
    bool s2 = (5 === "5");
    bool s3 = (true === true);
    see("5 === 5 = ", s1, " (should be true)\n");
    see("5 === \"5\" = ", s2, " (should be false, type mismatch)\n");
    see("true === true = ", s3, " (should be true)\n");

    // ！> 不大于
    bool ng1 = (5 !> 10);    // 5 不大于 10 → true
    bool ng2 = (10 !> 5);    // 10 不大于 5 → false
    bool ng3 = (5 !> 5);     // 5 不大于 5 → true (相等)
    see("5 !> 10 = ", ng1, " (should be true)\n");
    see("10 !> 5 = ", ng2, " (should be false)\n");
    see("5 !> 5 = ", ng3, " (should be true)\n");

    // ！< 不小于
    bool nl1 = (10 !< 5);    // 10 不小于 5 → true
    bool nl2 = (5 !< 10);    // 5 不小于 10 → false
    bool nl3 = (5 !< 5);     // 5 不小于 5 → true (相等)
    see("10 !< 5 = ", nl1, " (should be true)\n");
    see("5 !< 10 = ", nl2, " (should be false)\n");
    see("5 !< 5 = ", nl3, " (should be true)\n");

    see("\n");

    // ════════════════════════════════════════════
    // 测试 17: type() 内置函数
    // ════════════════════════════════════════════
    see("--- 测试 17: type() 内置函数 ---\n");

    str t1 = type(42);
    str t2 = type(3.14);
    str t3 = type("hello");
    str t4 = type(true);
    str t5 = type([1, 2, 3]);
    str t6 = type(null);

    see("type(42) = ", t1, " (should be <class:int>)\n");
    see("type(3.14) = ", t2, " (should be <class:float>)\n");
    see("type(\"hello\") = ", t3, " (should be <class:str>)\n");
    see("type(true) = ", t4, " (should be <class:bool>)\n");
    see("type([1,2,3]) = ", t5, " (should be <class:list>)\n");
    see("type(null) = ", t6, " (should be <class:null>)\n");

    // 对象的 type()
    life MyClass {}
    object obj = new MyClass();
    str t7 = type(obj);
    see("type(MyClass obj) = ", t7, " (should be <class:MyClass>)\n");

    see("\n");

    // ════════════════════════════════════════════
    // 测试 18: ID() 内置函数
    // ════════════════════════════════════════════
    see("--- 测试 18: ID() 内置函数 ---\n");

    int xid = 42;
    str id1 = ID(xid);
    see("ID(42) = ", id1, " (should be <ID:...>)\n");

    str id2 = ID(obj);
    see("ID(obj) = ", id2, " (should be <ID:...>)\n");

    bool id_unique = (id1 != id2);
    see("不同对象的 ID 不同 = ", id_unique, " (should be true)\n");

    see("\n");

    // ════════════════════════════════════════════
    // 测试 19: bool() 内置函数
    // ════════════════════════════════════════════
    see("--- 测试 19: bool() 内置函数 ---\n");

    bool b1 = bool(1);
    bool b2 = bool(0);
    bool b3 = bool("hello");
    bool b4 = bool("");
    bool b5 = bool(true);
    bool b6 = bool(null);
    bool b7 = bool([1, 2]);
    bool b8 = bool([]);

    see("bool(1) = ", b1, " (should be true)\n");
    see("bool(0) = ", b2, " (should be false)\n");
    see("bool(\"hello\") = ", b3, " (should be true)\n");
    see("bool(\"\") = ", b4, " (should be false)\n");
    see("bool(true) = ", b5, " (should be true)\n");
    see("bool(null) = ", b6, " (should be false)\n");
    see("bool([1,2]) = ", b7, " (should be true)\n");
    see("bool([]) = ", b8, " (should be false)\n");

    see("\n");

    // ════════════════════════════════════════════
    // 测试 20: int()/float() 类型错误处理
    // ════════════════════════════════════════════
    see("--- 测试 20: int()/float() 类型错误 ---\n");

    // 正常转换
    int i_ok = int(42);
    see("int(42) = ", i_ok, " (should be 42)\n");

    int i_str = int("123");
    see("int(\"123\") = ", i_str, " (should be 123)\n");

    float f_ok = float(3.14);
    see("float(3.14) = ", f_ok, " (should be 3.14)\n");

    float f_str = float("4.56");
    see("float(\"4.56\") = ", f_str, " (should be 4.56)\n");

    // 验证非法的转换会抛出 InterpreterError
    // 这里用 try-catch 测试
    try {
        int bad = int("abc");
        see("int(\"abc\") 没有抛出异常 (错误!)\n");
    } catch (e) {
        see("int(\"abc\") 正确抛出错误: ", e.message, "\n");
    }

    try {
        float bad = float("xyz");
        see("float(\"xyz\") 没有抛出异常 (错误!)\n");
    } catch (e) {
        see("float(\"xyz\") 正确抛出错误: ", e.message, "\n");
    }

    see("\n");

    // ════════════════════════════════════════════
    // 测试 21: 未声明变量访问报错
    // ════════════════════════════════════════════
    see("--- 测试 21: 未声明变量访问报错 ---\n");

    try {
        see(undefined_var);
        see("访问未声明变量没有抛出异常 (错误!)\n");
    } catch (e) {
        see("访问未声明变量正确抛出错误: ", e.message, "\n");
    }

    see("\n");

    // ════════════════════════════════════════════
    // 测试 22: 各种类型错误场景
    // ════════════════════════════════════════════
    see("--- 测试 22: 类型错误场景 ---\n");

    // null 转 int
    try {
        int n_i = int(null);
        see("int(null) 没有抛出异常 (错误!)\n");
    } catch (e) {
        see("int(null) 正确抛出错误: ", e.message, "\n");
    }

    // bool 转 int (Python 中 True/False 可以转 int, 所以不报错)
    int bi = int(true);
    see("int(true) = ", bi, " (should be 1)\n");

    see("\n");

    // ════════════════════════════════════════════
    see("=== 所有 v0.6 测试完成 ===\n");
}
