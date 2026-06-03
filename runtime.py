# 群星之舞 (Star Dance) - 运行时对象

from typing import Optional
from environment import Environment, ReturnException


# ═══════════════════════════════════════════════════════════════
# 错误注册表 — 所有内部错误/异常/警告在此声明
# ═══════════════════════════════════════════════════════════════
#
# 规则:
#   ER + 4位数字 = 内置错误 (≤5000 严重错误, >5000 异常)
#   ER + 5位数字 = 用户自定义错误 (≥10000)
#   WR + 4位数字 = 内置警告
#   WR + 5位数字 = 用户自定义警告
#
# 格式: code -> (name, message_template, suggestion_template)

ERROR_REGISTRY = {
    # ─── 语法错误 ER0001-ER0010 ───────────────────────────────
    'ER0001': ('SyntaxError', '语法错误', '请检查语句是否符合语法规则'),
    'ER0002': ('UnexpectedToken', '意外的符号', '请检查是否有多余或缺失的符号'),
    'ER0003': ('UnmatchedBrace', '括号不匹配', '请检查花括号/圆括号/方括号是否成对出现'),

    # ─── 类型错误 ER0101-ER0110 ───────────────────────────────
    'ER0101': ('TypeError', '类型错误', '请检查操作数的类型是否正确'),
    'ER0102': ('TypeMismatch', '类型不匹配', '请确保赋值或传参时类型一致'),
    'ER0103': ('DivisionByZero', '除零错误', '除数不能为零'),

    # ─── 名称错误 ER0201-ER0210 ───────────────────────────────
    'ER0201': ('NameError', '名称未定义', '请检查变量名或命途名是否拼写正确'),
    'ER0202': ('AttributeError', '属性不存在', '请检查对象是否包含该属性或方法'),
    'ER0203': ('DuplicateName', '名称重复定义', '请检查是否存在同名变量或命途'),

    # ─── 运行时错误 ER0301-ER0310 ─────────────────────────────
    'ER0301': ('IndexError', '索引越界', '请检查索引值是否在有效范围内'),
    'ER0302': ('NullReference', '空引用', '请检查对象是否已初始化'),
    'ER0303': ('InvalidOperation', '无效操作', '请检查操作是否符合预期'),
    'ER0304': ('NotCallable', '不可调用', '该对象不是一个可调用的方法或函数'),

    # ─── 常量/赋值错误 ER0401-ER0410 ──────────────────────────
    'ER0401': ('ConstAssignError', '常量不可修改', '常量只能在 start 块中定义且不可重新赋值'),
    'ER0402': ('InvalidAssignment', '无效赋值', '请检查赋值目标是否合法'),

    # ─── 继承/命途错误 ER0501-ER0510 ──────────────────────────
    'ER0501': ('InheritError', '继承错误——完成命途不可被继承', 'finish 命途不能被任何类继承'),
    'ER0502': ('FixedError', '固定命途——只能在 main 块中实例化', 'fix 命途只能在 main{} 中 new 实例'),
    'ER0503': ('SUPPERError', 'SUPPER 使用错误', 'SUPPER 只能在实例方法中调用'),
    'ER0504': ('SUPPERFixedError', '固定命途不可用 new SUPPER()', 'fix 命途的子类不能通过 new SUPPER() 实例化父类'),
    'ER0505': ('NewObjectError', 'Object 不可实例化', '基类 Object 不能被直接 new 实例化'),

    # ─── 异常（非严重）ER5001-ER5010 ──────────────────────────
    'ER5001': ('UserException', '用户抛出的异常', '请使用 try-catch 捕获此异常'),
    'ER5002': ('CustomError', '自定义错误', '请根据具体错误信息处理'),
}

# ─── 警告注册表 ──────────────────────────────────────────────────
WARN_REGISTRY = {
    'WR0001': ('Deprecated', '已弃用的语法', '请使用推荐的新语法替代'),
    'WR0002': ('TypeCoercion', '隐式类型转换', '类型转换可能导致精度损失'),
    'WR0003': ('UnusedVariable', '未使用的变量', '建议删除未使用的变量'),
}


def get_error_info(code: str) -> dict:
    """获取错误信息"""
    info = ERROR_REGISTRY.get(code)
    if info:
        return {'code': code, 'name': info[0], 'message': info[1], 'suggestion': info[2]}
    # 用户自定义错误 (ER10000+)
    if code.startswith('ER'):
        return {'code': code, 'name': 'UserDefinedError', 'message': '用户自定义错误', 'suggestion': ''}
    return {'code': code, 'name': 'UnknownError', 'message': '未知错误', 'suggestion': ''}


def get_warn_info(code: str) -> dict:
    """获取警告信息"""
    info = WARN_REGISTRY.get(code)
    if info:
        return {'code': code, 'name': info[0], 'message': info[1], 'suggestion': info[2]}
    return {'code': code, 'name': 'UserDefinedWarning', 'message': '用户自定义警告', 'suggestion': ''}


# ═══════════════════════════════════════════════════════════════


class LifeClass:
    """命途（类）定义"""
    def __init__(self, name: str, parent: Optional['LifeClass'] = None,
                 is_fixed: bool = False, is_finished: bool = False):
        self.name = name
        self.parent = parent
        self.is_fixed = is_fixed
        self.is_finished = is_finished
        self.methods = {}       # dict[str, ThingDecl]
        self.static_methods = {}  # dict[str, ThingDecl]
        self.fields = []        # list[str] - 属性名列表

    def add_method(self, method) -> None:
        """添加方法"""
        if method.is_static:
            self.static_methods[method.name] = method
        else:
            self.methods[method.name] = method

    def add_field(self, name: str) -> None:
        """添加属性声明"""
        if name not in self.fields:
            self.fields.append(name)

    def find_method(self, name: str):
        """查找方法（含继承链）"""
        if name in self.methods:
            return self.methods[name]
        if name in self.static_methods:
            return self.static_methods[name]
        if self.parent is not None:
            return self.parent.find_method(name)
        return None

    def find_method_source(self, name: str):
        """查找方法并返回 (method, source_class) — 用于 SUPPER"""
        if name in self.methods:
            return self.methods[name], self
        if name in self.static_methods:
            return self.static_methods[name], self
        if self.parent is not None:
            return self.parent.find_method_source(name)
        return None, None

    def find_static_method(self, name: str):
        """查找静态方法"""
        if name in self.static_methods:
            return self.static_methods[name]
        if self.parent is not None:
            return self.parent.find_static_method(name)
        return None

    def instantiate(self) -> 'LifeInstance':
        """创建实例"""
        return LifeInstance(self)

    def __repr__(self):
        parent_str = f" -> {self.parent.name}" if self.parent else ""
        return f"LifeClass({self.name}{parent_str}, methods={list(self.methods.keys())})"

    def find_method_from(self, name: str, start_class=None):
        """从指定类开始查找方法（用于 SUPPER 跳过当前类）"""
        cls = start_class or self
        if name in cls.methods:
            return cls.methods[name]
        if cls.parent is not None:
            return cls.find_method_from(name, cls.parent)
        return None


class LifeInstance:
    """命途实例（对象）"""
    def __init__(self, klass: LifeClass):
        self.klass = klass
        self.fields = {}        # dict[str, object]

    def get(self, name: str):
        """获取属性或方法"""
        if name == 'klass':
            return self.klass
        if name in self.fields:
            return self.fields[name]
        method, source_class = self.klass.find_method_source(name)
        if method is not None:
            return BoundMethod(self, method, source_class)
        if self.klass.parent is not None:
            # 检查父类的字段
            pass
        raise NameError(f"[运行时错误] 实例没有属性或方法: '{name}'")

    def set(self, name: str, value) -> None:
        """设置属性"""
        self.fields[name] = value

    def __str__(self):
        return f"<{self.klass.name} instance>"

    def __repr__(self):
        return f"<{self.klass.name} instance at {id(self):#x}>"


class BoundMethod:
    """绑定到实例的方法"""
    def __init__(self, instance: LifeInstance, method, source_class=None):
        self.instance = instance
        self.method = method
        self.source_class = source_class or instance.klass

    def __repr__(self):
        return f"<BoundMethod {self.instance.klass.name}.{self.method.name}>"


class StarFunction:
    """普通函数（非命途方法）"""
    def __init__(self, decl, closure: Environment):
        self.decl = decl          # ThingDecl
        self.closure = closure    # 闭包环境

    def call(self, interpreter, args: list) -> Optional:
        from interpreter import Interpreter
        env = self.closure.create_child(f"function:{self.decl.name}")

        # 绑定参数
        for i, param_name in enumerate(self.decl.params):
            value = args[i] if i < len(args) else None
            env.define(param_name, value)

        # 绑定 this（如果有）
        env.define('this', self.closure.get('this') if self.closure.has('this') else None)

        try:
            interpreter.execute_block(self.decl.body, env)
        except ReturnException as ret:
            return ret.value

        return None


class SuperWrapper:
    """SUPPER 关键字包装器 - 从父类开始解析方法"""
    def __init__(self, instance: LifeInstance, start_class: LifeClass = None):
        self.instance = instance
        self.parent_class = start_class or instance.klass.parent

    def get(self, name: str):
        if self.parent_class is None:
            raise NameError(f"[运行时错误] 基类 Object 没有方法: '{name}'")
        method, source = self.parent_class.find_method_source(name)
        if method is not None:
            return BoundMethod(self.instance, method, source)
        raise NameError(f"[运行时错误] 父类 '{self.parent_class.name}' 没有方法: '{name}'")

    def __repr__(self):
        return f"<SUPPER of {self.instance.klass.name}>"
