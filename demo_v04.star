// 群星之舞 v0.4 测试
// 功能: 常量 / join继承 / fix固定命途 / finish完成命途 / new SUPPER()

start{
    // === 测试1: 常量声明 ===
    float PI = 3.1415926;
    str GREETING = "hello from constant";
    int YEAR = 2026;
}

main{
    see("=== 群星之舞 v0.4 测试 ===");
    see("");

    // === 测试1: 常量 ===
    see("--- 测试1：start块常量声明 ---");
    see("PI = ", PI, " (should be 3.1415926)");
    see("GREETING = ", GREETING);
    see("YEAR = ", YEAR);
    see("");

    // === 测试2: join 继承 ===
    see("--- 测试2：join 关键字继承 ---");
    life Animal{
        thing speak(){
            see("Animal speaks");
        }
    }
    life Dog join Animal{
        thing speak(){
            see("Dog barks");
        }
    }
    object d = new Dog;
    d.speak();
    see("");

    // === 测试3: SUPPER 调用父方法（join继承） ===
    see("--- 测试3：join + SUPPER 调用父方法 ---");
    life Cat join Animal{
        thing speak(){
            see("Cat says: ", this.klass.name);
        }
        thing parentSpeak(){
            SUPPER.speak();
        }
    }
    object c = new Cat;
    c.parentSpeak();
    c.speak();
    see("");

    // === 测试4: new SUPPER() 创建父类实例 ===
    see("--- 测试4：new SUPPER() 创建父类实例 ---");
    life Parent{
        thing STR(){
            return "[Parent 实例]";
        }
    }
    life Child join Parent{
        thing makeParent(){
            object p = new SUPPER();
            see("在子类中创建了父类实例: ", p);
            return 1;
        }
    }
    object child = new Child;
    child.makeParent();
    see("");

    // === 测试5: fix 固定命途 ===
    see("--- 测试5：fix 固定命途 ---");
    fix life FixedBase{
        thing STR(){
            return "[FixedBase]";
        }
        thing greet(){
            see("Hello from FixedBase");
        }
    }
    // 可以在 main 中直接声明 fix 命途对象
    object fb = new FixedBase;
    see("fb = ", fb);
    fb.greet();
    see("");

    // === 测试6: fix 命途可被继承，但子类不能 new SUPPER() ===
    see("--- 测试6：fix 命途可继承，但 new SUPPER() 受限 ---");
    life SubClass join FixedBase{
        thing STR(){
            return "[SubClass inherits FixedBase]";
        }
        thing tryNewSuper(){
            see("[预期报错] 尝试 new SUPPER()...");
            object p = new SUPPER();
            see("不会执行到这里");
            return 0;
        }
    }
    object sub = new SubClass;
    see("sub = ", sub);
    sub.greet();
    see("");

    // === 测试7: SUPPER 在多层继承 + join 中正确定位 ===
    see("--- 测试7：多层 join 继承链 ---");
    life GrandParent{
        thing name(){
            return "GrandParent";
        }
    }
    life Mid join GrandParent{
        thing name(){
            return "Mid";
        }
        thing superName(){
            return SUPPER.name();
        }
    }
    life Young join Mid{
        thing name(){
            return "Young";
        }
        thing superName(){
            return SUPPER.name();
        }
        thing superSuperName(){
            return SUPPER.superName();
        }
    }
    object young = new Young;
    see("young.name() = ", young.name());
    see("young.superName() = ", young.superName());
    see("young.superSuperName() = ", young.superSuperName());
    see("");

    // === 测试8: finish 完成命途 ===
    see("--- 测试8：finish 完成命途 ---");
    finish life FinalMath{
        thing STR(){
            return "[FinalMath] 完成命途，不可被继承";
        }
    }
    object fm = new FinalMath;
    see("FinalMath: ", fm);

    // finish 命途不可被继承（取消注释可测试报错）
    // life BadChild join FinalMath{}
    see("");

    // === 测试9: 常量不可修改 ===
    see("--- 测试9：常量不可修改 ---");
    see("PI = ", PI, " (常量不可被赋值修改)");
    // PI = 3.0;  // 取消注释可测试常量不可修改
    see("");

    see("=== v0.4 所有测试完成 ===");
}
