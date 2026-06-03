start{
    see("=== 群星之舞 v0.2 数据类型与列表 ===\n");
}

main{
    // ─── 数据类型声明 ───
    int x = 42;
    float y = 3.14;
    str name = "群星之舞";
    see("int: ");
    see(x);
    see("\n");
    see("float: ");
    see(y);
    see("\n");
    see("str: ");
    see(name);
    see("\n\n");

    // ─── 列表（普通数组） ───
    see("=== 普通列表 ===\n");
    list numbers = [1, 2, 3, 4, 5];
    see(numbers);
    see("\n");
    see("len: ");
    see(len(numbers));
    see("\n\n");

    // ─── 列表（字典风格） ───
    see("=== 字典风格列表 ===\n");
    list a = [
        a: 1,
        b: 3
    ];
    see("a.a = ");
    see(a.a);
    see("\n");
    see("a.b = ");
    see(a.b);
    see("\n");
    see("len: ");
    see(len(a));
    see("\n");
    see("a: ");
    see(a);
    see("\n\n");

    // ─── 设属性值 ───
    a.c = 99;
    see("a.c assign: ");
    see(a.c);
    see("\n\n");

    // ─── fix() 冻结列表 ───
    see("=== fix() 冻结列表 ===\n");
    list mutable = [10, 20, 30];
    object fixed = fix(mutable);
    see("type_of(fixed): ");
    see(type_of(fixed));
    see("\n");
    see("fixed: ");
    see(fixed);
    see("\n");
    see("len(fixed): ");
    see(len(fixed));
    see("\n\n");

    // ─── fix() 冻结字典 ───
    list dict2 = [x: 100, y: 200];
    object fixed_dict = fix(dict2);
    see("fix(dict): ");
    see(fixed_dict);
    see("\n");
    see("type_of: ");
    see(type_of(fixed_dict));
    see("\n\n");

    // ─── 混合使用（字典 + 方法） ───
    list person = [
        name: "小明",
        age: 18,
    ];
    see("person.name = ");
    see(person.name);
    see("\n");
    see("person.age = ");
    see(person.age);
    see("\n\n");

    // ─── insert 输入测试（模拟） ───
    see("=== insert 输入测试 ===\n");
    see("（input 交互需要手动输入，在 REPL 中测试）\n");
    see("示例代码: insert(\"请输入名字: \", input_name, \"\");\n");

    see("\n=== 演示结束 ===\n");
}
