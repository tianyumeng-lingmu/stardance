// ═══════════════════════════════════════════════════
// 星舞计算器 — 群星之舞 (Star Dance) 示例程序
// 使用新的 insert() 表达式形式
// ═══════════════════════════════════════════════════

main {
    see("╔══════════════════════════╗\n");
    see("║    ✦ 星舞计算器 ✦       ║\n");
    see("║   Star Dance Calculator  ║\n");
    see("╚══════════════════════════╝\n\n");

    see("支持的运算:\n");
    see("  +  加法          -  减法\n");
    see("  *  乘法          /  除法\n");
    see("  %% 取模(余数)    ^  幂运算\n\n");
    see("输入 .exit 退出计算器\n");
    see("━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n");

    bool running = true;

    while (running) {
        // ─── 获取第一个数 ───
        see("输入第一个数: ");
        str a_input = insert("");
        // 检查退出
        if (a_input == ".exit") {
            running = false;
            continue;
        }
        int a = int(a_input);

        // ─── 获取运算符 ───
        see("输入运算符 (+, -, *, /, %%, ^): ");
        str op = insert("");

        if (op == ".exit") {
            running = false;
            continue;
        }

        // ─── 获取第二个数 ───
        see("输入第二个数: ");
        str b_input = insert("");

        if (b_input == ".exit") {
            running = false;
            continue;
        }
        int b = int(b_input);

        // ─── 计算结果 ───
        float result = 0;
        bool valid = true;

        if (op == "+") {
            result = a + b;
        } else if (op == "-") {
            result = a - b;
        } else if (op == "*") {
            result = a * b;
        } else if (op == "/") {
            if (b == 0) {
                see("错误：除数不能为零！\n\n");
                valid = false;
            } else {
                result = a / b;
            }
        } else if (op == "%%" || op == "%") {
            if (b == 0) {
                see("错误：取模不能为零！\n\n");
                valid = false;
            } else {
                result = a % b;
            }
        } else if (op == "^") {
            // 幂运算：手动累乘
            if (b == 0) {
                result = 1;
            } else {
                result = 1;
                int i = 0;
                if (b > 0) {
                    while (i < b) {
                        result = result * a;
                        i = i + 1;
                    }
                } else {
                    // 负指数：计算正指数后取倒数
                    float abs_b = 0 - b;
                    while (i < abs_b) {
                        result = result * a;
                        i = i + 1;
                    }
                    if (result != 0) {
                        result = 1 / result;
                    } else {
                        see("错误：0 不能有负指数！\n\n");
                        valid = false;
                    }
                }
            }
        } else {
            see("错误：不支持的运算符 '", op, "'\n\n");
            valid = false;
        }

        // ─── 显示结果 ───
        if (valid) {
            see("\n━━━━━━━━━━━━━━━━━━━━\n");
            see("  ", a, " ", op, " ", b, " = ", result, "\n");
            see("━━━━━━━━━━━━━━━━━━━━\n\n");
        }

        // ─── 询问是否继续 ───
        see("继续计算？(y/n): ");
        str cont = insert("");
        if (cont == "n" || cont == "N" || cont == ".exit") {
            running = false;
        }
        see("\n");
    }

    see("\n感谢使用星舞计算器，再见！\n");
}
