start{
    // 这里可以配置数据库和全局常量
    see("=== 群星之舞 演示程序 ===\n");
}

main{
    // ─── 定义命途（类） ───
    life Person{
        thing init(name, age){
            this.name = name;
            this.age = age;
        }

        thing greet(){
            see("你好，我是 ");
            see(this.name);
            see("，今年 ");
            see(this.age);
            see(" 岁。\n");
        }

        thing birthday(){
            this.age = this.age + 1;
            see(this.name);
            see(" 过生日啦！现在 ");
            see(this.age);
            see(" 岁了。\n");
        }
    }

    // ─── 继承演示 ───
    life Student extends Person{
        thing init(name, age, school){
            this.name = name;
            this.age = age;
            this.school = school;
        }

        thing study(){
            see(this.name);
            see(" 在 ");
            see(this.school);
            see(" 学习。\n");
        }
    }

    // ─── 使用对象 ───
    object p = new Person;
    p.init("小明", 18);
    p.greet();
    p.birthday();
    p.birthday();

    see("\n");

    // ─── 继承 ───
    object s = new Student;
    s.init("小红", 16, "星空中学");
    s.greet();
    s.study();

    see("\n");

    // ─── 数据库操作 ───
    see("=== 数据库操作 ===\n");
    db_create("users", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, score REAL");
    see("✅ 创建表 users 成功\n");

    db_execute("INSERT INTO users (name, age, score) VALUES ('小明', 18, 95.5)");
    db_execute("INSERT INTO users (name, age, score) VALUES ('小红', 16, 88.0)");
    db_execute("INSERT INTO users (name, age, score) VALUES ('小刚', 17, 92.3)");
    see("✅ 插入 3 条数据成功\n");

    object result = db_query("SELECT * FROM users");
    see("📊 查询结果：\n");
    see(result);
    see("\n");

    // ─── 条件判断 ───
    see("\n=== 条件判断 ===\n");
    object score = 95;
    if (score >= 90){
        see("优秀！\n");
    } else {
        if (score >= 60){
            see("及格\n");
        } else {
            see("不及格\n");
        }
    }

    // ─── 循环 ───
    see("\n=== 循环 ===\n");
    object i = 1;
    while (i <= 5){
        see("计数: ");
        see(i);
        see("\n");
        i = i + 1;
    }

    see("\n=== 演示结束 ===\n");
}
