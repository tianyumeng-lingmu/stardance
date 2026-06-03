start{
    see("=== 群星之舞 继承与魔术方法测试 ===\n\n");
}

main{
    // ─── 测试 1：生命隐式继承 Object ───
    see("--- 测试 1：life 隐式继承 Object ---\n");
    life Animal {}

    object a = new Animal();
    see("a = ");
    see(a);
    see("\n");  // 应显示: a = <Animal instance>
    see("\n");

    // ─── 测试 2：INIT 魔术方法自动调用 ───
    see("--- 测试 2：INIT 魔术方法自动调用 ---\n");
    life Person {
        str name;

        thing INIT(str n){
            this.name = n;
        }

        thing greet(){
            see("你好，我是 ");
            see(this.name);
            see("\n");
        }
    }

    object p = new Person("小明");
    p.greet();  // 应显示: 你好，我是 小明
    see("\n");

    // ─── 测试 3：STR 魔术方法覆盖 ───
    see("--- 测试 3：STR 魔术方法覆盖 ---\n");
    life Cat extends Animal {
        thing STR(){
            return "🐱 小猫喵喵";
        }
    }

    object cat = new Cat();
    see("cat = ");
    see(cat);   // 应显示: cat = 🐱 小猫喵喵
    see("\n\n");

    // ─── 测试 4：继承与多态 ───
    see("--- 测试 4：继承与多态 ---\n");
    life Shape {
        thing area(){
            return 0;
        }
    }

    life Circle extends Shape {
        float r;

        thing INIT(float radius){
            this.r = radius;
        }

        thing area(){
            return 3.14159 * this.r * this.r;
        }
    }

    object shape = new Circle(5.0);
    see("圆面积 = ");
    see(shape.area());  // 应显示: 78.53975
    see("\n\n");

    // ─── 测试 5：SUPPER 关键字调用父方法 ───
    see("--- 测试 5：SUPPER 关键字调用父方法 ---\n");
    life Parent {
        thing greet(){
            see("Parent::greet()\n");
        }
    }

    life Child extends Parent {
        thing greet(){
            SUPPER.greet();    // 调用父类方法
            see("Child::greet()\n");
        }
    }

    object child = new Child();
    child.greet();  // 应显示: Parent::greet()  Child::greet()
    see("\n");

    // ─── 测试 6：多层继承链 ───
    see("--- 测试 6：多层继承链 ---\n");
    life GrandParent {
        thing say(){
            see("GrandParent\n");
        }
    }

    life Mid extends GrandParent {
        thing say(){
            SUPPER.say();
            see("Mid\n");
        }
    }

    life Young extends Mid {
        thing say(){
            SUPPER.say();
            see("Young\n");
        }
    }

    object young = new Young();
    young.say();  // 应显示: GrandParent Mid Young
    see("\n");

    // ─── 测试 7：LEN 魔术方法 ───
    see("--- 测试 7：LEN 魔术方法 ---\n");
    life MyList {
        int size;

        thing INIT(int s){
            this.size = s;
        }

        thing LEN(){
            return this.size;
        }
    }

    object ml = new MyList(5);
    see("len(ml) = ");
    see(len(ml));  // 应显示: 5
    see("\n\n");

    // ─── 测试 8：用户自定义 Object 方法合并 ───
    see("--- 测试 8：为 Object 添加通用方法 ---\n");
    life Object {
        thing myType(){
            return type_of(this);
        }
    }

    see("type via Object: ");
    see(young.myType());  // 应显示: Young
    see("\n\n");

    see("=== 所有测试通过！===\n");
}
