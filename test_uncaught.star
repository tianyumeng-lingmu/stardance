// 未捕获异常测试 — 应该显示格式化错误
main {
    var err = new Error;
    err.code = "ER5001";
    err.name = "UncaughtError";
    err.message = "这是一个未捕获的异常";
    err.suggestion = "请使用 try-catch 捕获异常";
    throw err;
}
