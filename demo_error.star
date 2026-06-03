// ═══════════════════════════════════════════════════════════════
// 群星之舞 v0.5 — 错误系统测试
// ═══════════════════════════════════════════════════════════════

start {
    var test_count = 0;
}

main {
    see("=== 群星之舞 v0.5 错误系统测试 ===\n");

    // ─── 测试1：Error 类是内置类 ──────────────────────────────
    see("--- 测试1：Error 类存在 ---\n");
    var e1 = new Error;
    see("e1.klass = ", e1.klass.name, " (should be Error)\n");

    // ─── 测试2：Error STR 魔术方法 ────────────────────────────
    see("--- 测试2：Error STR 显示 ---\n");
    // 内部使用 _new_error 设置字段
    // 这里手动设置字段来测试
    var e2 = new Error;
    e2.code = "ER0001";
    e2.name = "SyntaxError";
    see("e2 = ", e2, "\n");  // 应该显示 [ER0001]-SyntaxError

    // ─── 测试3：Error 继承自 Object ───────────────────────────
    see("--- 测试3：Error 继承链 ---\n");
    see("e1.klass.name = ", e1.klass.name, " (should be Error)\n");
    see("e1.klass.parent.name = ", e1.klass.parent.name, " (should be Object)\n");

    // ─── 测试4：自定义错误子类 ────────────────────────────────
    see("--- 测试4：自定义错误子类 ---\n");
    life MyError join Error {
        thing INIT(code, name, msg) {
            this.code = code;
            this.name = name;
            this.message = msg;
        }
    }
    var myErr = new MyError("ER10001", "MyCustomError", "这是一个自定义错误");
    see("myErr = ", myErr, " (should be [ER10001]-MyCustomError)\n");

    // ─── 测试5：throw + try-catch ─────────────────────────────
    see("--- 测试5：throw + try-catch ---\n");
    try {
        var err = new Error;
        err.code = "ER5001";
        err.name = "TestError";
        err.message = "测试抛出异常";
        throw err;
        see("这行不应该被执行\n");
    } catch(e) {
        see("捕获到异常: ", e, "\n");
    }

    // ─── 测试6：try-catch-finally ─────────────────────────────
    see("--- 测试6：try-catch-finally ---\n");
    try {
        see("  try 块执行\n");
        var err2 = new Error;
        err2.code = "ER5002";
        err2.name = "FinallyTest";
        throw err2;
    } catch(e) {
        see("  catch 块执行: ", e, "\n");
    } finally {
        see("  finally 块总是执行\n");
    }

    // ─── 测试7：finally 在没有异常时也执行 ────────────────────
    see("--- 测试7：无异常时的 try-finally ---\n");
    try {
        see("  try 块正常执行\n");
    } catch(e) {
        see("  不应该执行到这里\n");
    } finally {
        see("  finally 块仍然执行\n");
    }

    // ─── 测试8：Error 所有字段 ────────────────────────────────
    see("--- 测试8：Error 字段 ---\n");
    var e3 = new Error;
    e3.code = "ER0101";
    e3.name = "TypeError";
    e3.message = "类型错误: 期望 int 得到 str";
    e3.line = 42;
    e3.column = 15;
    e3.suggestion = "请检查参数类型";
    see("  code: ", e3.code, "\n");
    see("  name: ", e3.name, "\n");
    see("  message: ", e3.message, "\n");
    see("  line: ", e3.line, "\n");
    see("  column: ", e3.column, "\n");
    see("  suggestion: ", e3.suggestion, "\n");

    // ─── 测试9：throw 子类 ────────────────────────────────────
    see("--- 测试9：throw 自定义子类 ---\n");
    life NetworkError join Error {
        thing INIT(code, msg, url) {
            this.code = code;
            this.name = "NetworkError";
            this.message = msg;
            this.url = url;
        }
    }
    try {
        throw new NetworkError("ER10002", "连接超时", "https://api.example.com");
    } catch(e) {
        see("  捕获: ", e, "\n");
        see("  url: ", e.url, "\n");
    }

    // ─── 测试10：多层 try-catch ───────────────────────────────
    see("--- 测试10：嵌套 try-catch ---\n");
    try {
        try {
            var e4 = new Error;
            e4.code = "ER5003";
            e4.name = "InnerError";
            throw e4;
        } catch(inner) {
            see("  内层捕获: ", inner, "\n");
            // 重新抛出
            throw inner;
        }
    } catch(outer) {
        see("  外层捕获: ", outer, "\n");
    }

    see("\n=== 所有错误系统测试完成 ===");
}
