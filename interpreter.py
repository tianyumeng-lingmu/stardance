# 群星之舞 (Star Dance) - 解释器

from tokens import TokenType
from ast_nodes import *
from environment import Environment, ReturnException
from database import StarDatabase
from runtime import (
    LifeClass, LifeInstance, BoundMethod, StarFunction, SuperWrapper,
    ERROR_REGISTRY, get_error_info
)


class StarException(Exception):
    """语言级异常，携带 Error 实例"""
    def __init__(self, error_instance: 'LifeInstance'):
        self.error_instance = error_instance
        super().__init__(str(error_instance))


class BreakException(Exception):
    """循环 break"""
    pass


class ContinueException(Exception):
    """循环 continue"""
    pass


class CutDownException(Exception):
    """中断所有嵌套循环"""
    pass


class InterpreterError(Exception):
    pass


class Interpreter:
    """群星之舞 AST 解释器"""

    def __init__(self):
        self.global_env = Environment(name="<global>")
        self.database = None        # StarDatabase 实例，程序启动时创建
        self.env_history = []       # 环境历史记录（用于调试）
        self.in_main_block = False  # 是否在 main 块中执行
        self._loop_depth = 0        # 嵌套循环深度，用于 cutdown 控制

    def interpret(self, program: Program, db_path: str = None):
        """执行整个程序"""
        # 初始化数据库
        self.database = StarDatabase(db_path)
        self.global_env.define('__db__', self.database)

        # 注册内置函数到全局环境
        self._register_builtins()
        # 注册 Object 基类
        self._register_default_object()
        # 注册 Error 内置错误类
        self._register_default_error()

        # 解析并注册所有 life 声明
        if program.start_block:
            self._collect_class_definitions(program.start_block)
        if program.main_block:
            self._collect_class_definitions(program.main_block)

        # 执行 start 块
        if program.start_block:
            self.execute_block(program.start_block.statements, self.global_env, is_top_level=True)

        # 执行 main 块
        self.in_main_block = True
        if program.main_block:
            self.execute_block(program.main_block.statements, self.global_env, is_top_level=True)
        self.in_main_block = False

    def _collect_class_definitions(self, block):
        """收集块中所有的 life 声明并注册"""
        for stmt in getattr(block, 'statements', block) if isinstance(block, (list, Block)) else block:
            if isinstance(stmt, LifeDecl):
                self._register_life(stmt, self.global_env)

    def _register_life(self, decl: LifeDecl, env: Environment):
        """注册命途定义"""
        # 如果用户重定义 Object，合并方法而非替换
        if decl.name == 'Object' and env.has_class('Object'):
            existing = env.get_class('Object')
            for member in decl.body:
                if isinstance(member, ThingDecl):
                    existing.add_method(member)
                elif isinstance(member, VarDecl):
                    existing.add_field(member.name)
            return

        # 先处理父命途
        parent_class = None
        if decl.parent:
            try:
                parent_class = env.get_class(decl.parent)
            except (NameError, InterpreterError):
                raise InterpreterError(
                    f"[运行时错误] 命途 '{decl.parent}' 未定义"
                )
            # 检查 finish 约束：finish 命途不可被继承
            if parent_class.is_finished:
                self._throw_error('ER0501',
                                  f"试图继承 finish 命途 '{decl.parent}'",
                                  decl.line, decl.column)

        life_class = LifeClass(decl.name, parent_class,
                               is_fixed=decl.is_fixed,
                               is_finished=decl.is_finished)

        # 注册成员
        for member in decl.body:
            if isinstance(member, ThingDecl):
                life_class.add_method(member)
            elif isinstance(member, VarDecl):
                life_class.add_field(member.name)

        env.define_class(decl.name, life_class)
        # 同时将命途定义作为变量注册，方便通过 name 访问
        env.define(decl.name, life_class)

    def _register_builtins(self):
        """注册内置函数"""

        # see() - 打印输出
        interp = self

        def builtin_see(*args):
            output = []
            for arg in args:
                if arg is None:
                    output.append("null")
                elif isinstance(arg, bool):
                    output.append("true" if arg else "false")
                elif isinstance(arg, LifeInstance):
                    # 尝试调用 STR 魔术方法
                    str_method, str_source = arg.klass.find_method_source('STR')
                    if str_method is not None:
                        bm = BoundMethod(arg, str_method, str_source)
                        result = interp._call_bound_method(bm, [], interp.global_env)
                        output.append(str(result) if result is not None else "")
                    else:
                        output.append(str(arg))
                else:
                    output.append(str(arg))
            print(''.join(output))

        self.global_env.define('see', builtin_see)

        # db_execute() - 执行 SQL
        def builtin_db_execute(sql: str, *params):
            return self.database.execute(sql, params)

        self.global_env.define('db_execute', builtin_db_execute)

        # db_query() - 执行 SQL 查询
        def builtin_db_query(sql: str, *params):
            return self.database.query(sql, params)

        self.global_env.define('db_query', builtin_db_query)

        # db_create() - 创建表
        def builtin_db_create(table_name: str, columns: str):
            return self.database.create_table(table_name, columns)

        self.global_env.define('db_create', builtin_db_create)

        # db_drop() - 删除表
        def builtin_db_drop(table_name: str):
            return self.database.drop_table(table_name)

        self.global_env.define('db_drop', builtin_db_drop)

        # str() - 转为字符串
        def builtin_str(value):
            if value is None:
                return "null"
            return str(value)

        self.global_env.define('str', builtin_str)

        # int() - 转为整数
        def builtin_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                interp._throw_error('ER0101',
                                    f"无法将 '{value}' (类型: {type(value).__name__}) 转换为整数",
                                    0, 0, "请确保传入的字符串是合法的数字格式")

        self.global_env.define('int', builtin_int)

        # float() - 转为浮点数
        def builtin_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                interp._throw_error('ER0102',
                                    f"无法将 '{value}' (类型: {type(value).__name__}) 转换为浮点数",
                                    0, 0, "请确保传入的字符串是合法的浮点格式")

        self.global_env.define('float', builtin_float)

        # bool() - 转为布尔值
        def builtin_bool(value):
            if isinstance(value, bool):
                return value
            if value is None:
                return False
            if isinstance(value, (int, float)):
                return value != 0
            if isinstance(value, str):
                return value != ""
            if isinstance(value, (list, tuple, dict)):
                return len(value) > 0
            if isinstance(value, LifeInstance):
                return True
            return bool(value)

        self.global_env.define('bool', builtin_bool)

        # insert() - 获取用户输入（返回字符串）
        def builtin_insert(prompt=""):
            try:
                return input(str(prompt))
            except EOFError:
                return ""

        self.global_env.define('insert', builtin_insert)

        # type() - 获取类型名 (<class:int> 格式)
        def builtin_type(value):
            if isinstance(value, LifeInstance):
                return f"<class:{value.klass.name}>"
            if isinstance(value, bool):
                return "<class:bool>"
            if isinstance(value, int):
                return "<class:int>"
            if isinstance(value, float):
                return "<class:float>"
            if isinstance(value, str):
                return "<class:str>"
            if isinstance(value, bool):
                return "<class:bool>"
            if isinstance(value, list):
                return "<class:list>"
            if isinstance(value, tuple):
                return "<class:tuple>"
            if isinstance(value, dict):
                return "<class:dict>"
            if value is None:
                return "<class:null>"
            return f"<class:{type(value).__name__}>"

        self.global_env.define('type', builtin_type)

        # ID() - 获取唯一标识
        def builtin_ID(value):
            return f"<ID:{id(value):#x}>"

        self.global_env.define('ID', builtin_ID)

        # len() - 获取长度
        def builtin_len(value):
            if isinstance(value, LifeInstance):
                len_method, len_source = value.klass.find_method_source('LEN')
                if len_method is not None:
                    bm = BoundMethod(value, len_method, len_source)
                    result = interp._call_bound_method(bm, [], interp.global_env)
                    return result if result is not None else 0
                return 0
            if isinstance(value, str):
                return len(value)
            if isinstance(value, (list, tuple)):
                return len(value)
            if isinstance(value, dict):
                return len(value)
            return 0

        self.global_env.define('len', builtin_len)

        # type_of() - 获取类型
        def builtin_type_of(value):
            if isinstance(value, LifeInstance):
                return value.klass.name
            if isinstance(value, str):
                return "string"
            if isinstance(value, int):
                return "int"
            if isinstance(value, float):
                return "float"
            if isinstance(value, bool):
                return "bool"
            if isinstance(value, tuple):
                return "list_fixed"
            if isinstance(value, (list, dict)):
                return "list"
            if value is None:
                return "null"
            return type(value).__name__

        self.global_env.define('type_of', builtin_type_of)

        # fix() - 将列表冻结为不可变
        def builtin_fix(value):
            if isinstance(value, list):
                return tuple(value)
            if isinstance(value, dict):
                # 冻结字典：转为 key-value 元组列表
                return tuple(sorted(value.items()))
            return value

        self.global_env.define('fix', builtin_fix)

    def _register_default_object(self):
        """预注册 Object 基类及其默认魔术方法"""
        object_class = LifeClass('Object', parent=None)

        # STR — see()/str() 调用时转为字符串
        # 默认不创建 STR，see() 内建会自动用 <ClassName instance> 显示
        # 用户可在子类中定义 thing STR(){return "...";} 覆盖

        # INIT — 构造函数（默认无操作）
        from ast_nodes import ThingDecl
        init_body = []
        object_class.add_method(ThingDecl('INIT', [], init_body))

        # LEN — len() 调用（默认由 builtin_len 返回 0）
        # 用户可在子类中定义 thing LEN(){return 42;} 覆盖

        self.global_env.define_class('Object', object_class)
        self.global_env.define('Object', object_class)

    def _register_default_error(self):
        """预注册 Error 内置错误类"""
        error_class = LifeClass('Error', parent=self.global_env.get_class('Object'))

        # 字段
        error_class.fields = ['code', 'name', 'message', 'line', 'column', 'suggestion']

        # 默认 STR 魔术方法
        from ast_nodes import ThingDecl, ReturnStmt, BinaryOp, Identifier, Literal
        str_body = [
            ReturnStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            Literal("["),
                            '+', GetAttr(Identifier('this'), 'code')
                        ),
                        '+', Literal("]-")
                    ),
                    '+', GetAttr(Identifier('this'), 'name')
                )
            )
        ]
        error_class.add_method(ThingDecl('STR', [], str_body))

        self.global_env.define_class('Error', error_class)
        self.global_env.define('Error', error_class)

    # ─── 错误辅助方法 ──────────────────────────────────────────

    def _new_error(self, code: str, message_detail: str = "",
                   line: int = 0, column: int = 0,
                   suggestion: str = "", source_line: str = "") -> 'LifeInstance':
        """创建一个 Error 实例（不抛出）
        code: 错误编码如 'ER0001'
        message_detail: 额外的错误细节描述
        """
        info = get_error_info(code)
        err = self.global_env.get_class('Error').instantiate()
        err.set('code', code)
        err.set('name', info['name'])
        err.set('message', info['message'] + (f": {message_detail}" if message_detail else ""))
        err.set('line', line)
        err.set('column', column)
        err.set('suggestion', suggestion or info['suggestion'])
        err.set('__source_line', source_line)
        return err

    def _throw_error(self, code: str, message_detail: str = "",
                     line: int = 0, column: int = 0,
                     suggestion: str = "", source_line: str = ""):
        """抛出错误 — 创建 Error 实例并触发 StarException"""
        error_instance = self._new_error(code, message_detail, line, column,
                                         suggestion, source_line)
        raise StarException(error_instance)

    def _format_error_display(self, err: 'LifeInstance') -> str:
        """格式化错误显示的完整信息（含行号、代码行、位置标记、建议）"""
        code = err.get('code') if hasattr(err, 'get') else 'ER0000'
        name = err.get('name') if hasattr(err, 'get') else 'UnknownError'
        message = err.get('message') if hasattr(err, 'get') else str(err)
        line = err.get('line') if hasattr(err, 'get') else 0
        column = err.get('column') if hasattr(err, 'get') else 0
        source_line = err.get('__source_line') if hasattr(err, 'get') else ""
        suggestion = err.get('suggestion') if hasattr(err, 'get') else ""

        result = f"[{code}]-{name}：\n"
        if line:
            result += f"line {line}：{message}\n"
            if source_line:
                result += f"  {source_line}\n"
                if column:
                    result += f"  {' ' * max(0, column - 1)}^\n"
        else:
            result += f"{message}\n"
        if suggestion:
            result += f"建议：{suggestion}\n"
        return result

    def _call_bound_method(self, bound: BoundMethod, args: list, env: Environment):
        """调用绑定方法（用于魔术方法自动调用）"""
        method_env = env.create_child(f"magic:{bound.method.name}")
        method_env.define('this', bound.instance)
        # 存储方法定义所在类，供 SUPPER 正确解析多层继承
        method_env.define('__class__', bound.source_class)

        for i, param_name in enumerate(bound.method.params):
            value = args[i] if i < len(args) else None
            method_env.define(param_name, value)

        try:
            self.execute_block(bound.method.body, method_env)
        except ReturnException as ret:
            return ret.value
        return None

    def execute_block(self, stmts: list, env: Environment, is_top_level: bool = False):
        """执行一个语句块"""
        block_env = env if is_top_level else env.create_child()
        self.env_history.append(block_env)

        for stmt in stmts:
            try:
                self.execute(stmt, block_env)
            except CutDownException:
                if self._loop_depth > 0:
                    raise
                # 不在循环内时，吞掉异常（已退出所有嵌套循环），继续执行下一条语句

        self.env_history.pop()

    def execute(self, node: ASTNode, env: Environment):
        """分发执行 AST 节点"""
        if isinstance(node, Block):
            self.execute_block(node.statements, env)

        elif isinstance(node, LifeDecl):
            # 在块内定义命途
            self._register_life(node, env)

        elif isinstance(node, VarDecl):
            value = None
            if node.initializer:
                value = self.evaluate(node.initializer, env)
            env.define(node.name, value)

        elif isinstance(node, ConstDecl):
            value = self.evaluate(node.initializer, env)
            env.define_constant(node.name, value)

        elif isinstance(node, Assign):
            value = self.evaluate(node.value, env)
            if isinstance(node.target, Identifier):
                env.assign(node.target.name, value)
            elif isinstance(node.target, GetAttr):
                obj = self.evaluate(node.target.obj, env)
                if isinstance(obj, LifeInstance):
                    obj.set(node.target.attr, value)
                elif isinstance(obj, dict):
                    obj[node.target.attr] = value
                else:
                    raise InterpreterError(f"无法为 {type(obj).__name__} 设置属性")

        elif isinstance(node, IfStmt):
            condition = self.evaluate(node.condition, env)
            if self._is_truthy(condition):
                self.execute_block(node.then_block, env)
            elif node.else_block:
                self.execute_block(node.else_block, env)

        elif isinstance(node, WhileStmt):
            self._loop_depth += 1
            try:
                while self._is_truthy(self.evaluate(node.condition, env)):
                    try:
                        self.execute_block(node.body, env)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                    except CutDownException:
                        raise
                    except ReturnException:
                        raise
            finally:
                self._loop_depth -= 1

        elif isinstance(node, ForStmt):
            self._loop_depth += 1
            try:
                for_env = env.create_child("for")
                if node.init:
                    self.execute(node.init, for_env)
                while True:
                    if node.condition and not self._is_truthy(self.evaluate(node.condition, for_env)):
                        break
                    try:
                        self.execute_block(node.body, for_env)
                    except BreakException:
                        break
                    except ContinueException:
                        if node.update:
                            self.evaluate(node.update, for_env)
                        continue
                    except CutDownException:
                        raise
                    except ReturnException:
                        raise
                    if node.update:
                        self.evaluate(node.update, for_env)
            finally:
                self._loop_depth -= 1

        elif isinstance(node, ForeachStmt):
            self._loop_depth += 1
            try:
                iterable = self.evaluate(node.iterable, env)
                if isinstance(iterable, str):
                    items = list(iterable)
                elif isinstance(iterable, (list, tuple)):
                    items = iterable
                elif isinstance(iterable, dict):
                    items = list(iterable.keys())
                elif isinstance(iterable, range):
                    items = iterable
                else:
                    raise InterpreterError(f"foreach: 无法遍历 {type(iterable).__name__}")
                foreach_env = env.create_child("foreach")
                for item in items:
                    foreach_env.define(node.var_name, item)
                    try:
                        self.execute_block(node.body, foreach_env)
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                    except CutDownException:
                        raise
                    except ReturnException:
                        raise
            finally:
                self._loop_depth -= 1

        elif isinstance(node, CaseStmt):
            match_value = self.evaluate(node.expr, env)
            matched = False
            for when in node.when_clauses:
                when_value = self.evaluate(when.value, env)
                if match_value == when_value:
                    self.execute_block(when.body, env)
                    matched = True
                    break
            if not matched and node.else_body:
                self.execute_block(node.else_body, env)

        elif isinstance(node, ReturnStmt):
            value = None
            if node.value:
                value = self.evaluate(node.value, env)
            raise ReturnException(value)

        elif isinstance(node, BreakStmt):
            raise BreakException()

        elif isinstance(node, ContinueStmt):
            raise ContinueException()

        elif isinstance(node, CutDownStmt):
            raise CutDownException()

        elif isinstance(node, SeeStmt):
            values = [self.evaluate(a, env) for a in node.args]
            see_func = self.global_env.get('see')
            see_func(*values)

        elif isinstance(node, ThrowStmt):
            error_instance = self.evaluate(node.expr, env)
            if isinstance(error_instance, LifeInstance):
                error_instance.set('line', node.line)
                error_instance.set('column', node.column)
                klass = error_instance.klass
                while klass:
                    if klass.name == 'Error':
                        raise StarException(error_instance)
                    klass = klass.parent
            err = self._new_error('ER5001', str(error_instance),
                                  node.line, node.column)
            raise StarException(err)

        elif isinstance(node, TryStmt):
            try:
                self.execute_block(node.try_body, env)
            except StarException as e:
                if node.catch_var and node.catch_body:
                    catch_env = env.create_child("catch")
                    catch_env.define(node.catch_var, e.error_instance)
                    try:
                        self.execute_block(node.catch_body, catch_env)
                    except ReturnException:
                        raise
            except NameError as e:
                # 将 NameError 转换为 StarException 以供 try-catch 捕获
                if node.catch_var and node.catch_body:
                    err_msg = str(e).replace("[运行时错误] ", "")
                    err = self._new_error('ER0201', err_msg,
                                          node.line, node.column,
                                          "请检查变量名是否拼写正确")
                    catch_env = env.create_child("catch")
                    catch_env.define(node.catch_var, err)
                    try:
                        self.execute_block(node.catch_body, catch_env)
                    except ReturnException:
                        raise
            except InterpreterError as e:
                if node.catch_var and node.catch_body:
                    err = self._new_error('ER0001', str(e),
                                          node.line, node.column)
                    catch_env = env.create_child("catch")
                    catch_env.define(node.catch_var, err)
                    try:
                        self.execute_block(node.catch_body, catch_env)
                    except ReturnException:
                        raise
            finally:
                if node.finally_body:
                    try:
                        self.execute_block(node.finally_body, env)
                    except ReturnException:
                        raise

        elif isinstance(node, ExprStmt):
            self.evaluate(node.expr, env)

        else:
            raise InterpreterError(f"未知的 AST 节点类型: {type(node).__name__}")

    def evaluate(self, node: ASTNode, env: Environment):
        """计算表达式的值"""
        # 字面量
        if isinstance(node, Literal):
            return node.value

        # 标识符
        if isinstance(node, Identifier):
            if node.name == 'this':
                return env.get('this')
            if node.name == 'SUPPER':
                this = env.get('this')
                if not isinstance(this, LifeInstance):
                    raise InterpreterError("[运行时错误] SUPPER 只能在方法中使用")
                current_class = env.get('__class__') if env.has('__class__') else this.klass
                start_class = current_class.parent if current_class else this.klass.parent
                return SuperWrapper(this, start_class)
            return env.get(node.name)

        # 二元运算
        if isinstance(node, BinaryOp):
            return self._evaluate_binary(node, env)

        # 一元运算
        if isinstance(node, UnaryOp):
            return self._evaluate_unary(node, env)

        # new 表达式
        if isinstance(node, NewExpr):
            if node.class_name == 'SUPPER':
                this = env.get('this')
                if not isinstance(this, LifeInstance):
                    self._throw_error('ER0503', "new SUPPER() 只能在实例方法中使用",
                                      node.line, node.column)
                current_class = env.get('__class__') if env.has('__class__') else this.klass
                parent_class = current_class.parent if current_class else this.klass.parent
                if parent_class is None:
                    self._throw_error('ER0505', "基类 Object 不能被 new SUPPER()",
                                      node.line, node.column)
                if parent_class.is_fixed:
                    self._throw_error('ER0504',
                                      f"固定命途 '{parent_class.name}' 不可 new SUPPER()",
                                      node.line, node.column)
                instance = parent_class.instantiate()
                init_method, init_source = parent_class.find_method_source('INIT')
                if init_method is not None:
                    bound = BoundMethod(instance, init_method, init_source)
                    init_args = [self.evaluate(a, env) for a in node.args]
                    self._call_bound_method(bound, init_args, env)
                return instance

            life_class = env.get_class(node.class_name)
            if life_class.is_fixed and not self.in_main_block:
                self._throw_error('ER0502',
                                  f"固定命途 '{node.class_name}' 只能在 main 块中 new",
                                  node.line, node.column)
            instance = life_class.instantiate()
            init_method, init_source = life_class.find_method_source('INIT')
            if init_method is not None:
                bound = BoundMethod(instance, init_method, init_source)
                init_args = [self.evaluate(a, env) for a in node.args]
                self._call_bound_method(bound, init_args, env)
            return instance

        # 列表字面量
        if isinstance(node, ListLiteral):
            if node.has_keys:
                result = {}
                for key, value_node in node.entries:
                    result[key] = self.evaluate(value_node, env)
                return result
            else:
                return [self.evaluate(value_node, env) for _, value_node in node.entries]

        # 方法/函数调用
        if isinstance(node, CallExpr):
            return self._evaluate_call(node, env)

        # 属性访问
        if isinstance(node, GetAttr):
            obj = self.evaluate(node.obj, env)
            if isinstance(obj, LifeInstance):
                result = obj.get(node.attr)
                return result
            if isinstance(obj, SuperWrapper):
                return obj.get(node.attr)
            if isinstance(obj, LifeClass):
                if hasattr(obj, node.attr):
                    return getattr(obj, node.attr)
                raise InterpreterError(f"命途 '{obj.name}' 没有属性 '{node.attr}'")
            if isinstance(obj, dict):
                if node.attr in obj:
                    return obj[node.attr]
                raise InterpreterError(f"字典中没有键 '{node.attr}'")
            raise InterpreterError(f"无法访问 {type(obj).__name__} 的属性 '{node.attr}'")

        # 赋值（作为表达式）
        if isinstance(node, Assign):
            value = self.evaluate(node.value, env)
            if isinstance(node.target, Identifier):
                env.assign(node.target.name, value)
            elif isinstance(node.target, GetAttr):
                obj = self.evaluate(node.target.obj, env)
                if isinstance(obj, LifeInstance):
                    obj.set(node.target.attr, value)
                elif isinstance(obj, dict):
                    obj[node.target.attr] = value
            return value

        raise InterpreterError(f"无法计算的表达式: {type(node).__name__}")

    def _evaluate_binary(self, node: BinaryOp, env: Environment):
        left = self.evaluate(node.left, env)

        if node.op == '&&':
            # 惰性求值：左假则短路
            if not self._is_truthy(left):
                return False
            right = self.evaluate(node.right, env)
            return self._is_truthy(right)

        if node.op == '||':
            # 惰性求值：左真则短路
            if self._is_truthy(left):
                return True
            right = self.evaluate(node.right, env)
            return self._is_truthy(right)

        # 非惰性运算符：正常求值左右
        right = self.evaluate(node.right, env)

        if node.op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            if isinstance(left, int) and isinstance(right, int):
                return left / right
            return left / right
        elif node.op == '%':
            return left % right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '===':
            # 严格相等：值和类型都必须相同
            return type(left).__name__ == type(right).__name__ and left == right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
        elif node.op == '<=':
            return left <= right
        elif node.op == '>=':
            return left >= right
        elif node.op == '!>':
            # 不大于 = !(a > b) 等价于 a <= b
            return left <= right
        elif node.op == '!<':
            # 不小于 = !(a < b) 等价于 a >= b
            return left >= right
        # 位运算
        elif node.op == '&':
            return left & right
        elif node.op == '|':
            return left | right
        elif node.op == '<<':
            return left << right
        elif node.op == '>>':
            return left >> right
        elif node.op == '>>>':
            # 模拟32位无符号右移
            left = left & 0xFFFFFFFF
            return left >> right
        else:
            raise InterpreterError(f"未知的二元运算符: '{node.op}'")

    def _evaluate_unary(self, node: UnaryOp, env: Environment):
        if node.op == '++':
            if node.is_prefix:
                # ++i: 先自增再取值
                if isinstance(node.operand, Identifier):
                    old = env.get(node.operand.name)
                    new = old + 1
                    env.assign(node.operand.name, new)
                    return new
            else:
                # i++: 先取值再自增
                if isinstance(node.operand, Identifier):
                    old = env.get(node.operand.name)
                    env.assign(node.operand.name, old + 1)
                    return old

        elif node.op == '--':
            if node.is_prefix:
                # --i
                if isinstance(node.operand, Identifier):
                    old = env.get(node.operand.name)
                    new = old - 1
                    env.assign(node.operand.name, new)
                    return new
            else:
                # i--
                if isinstance(node.operand, Identifier):
                    old = env.get(node.operand.name)
                    env.assign(node.operand.name, old - 1)
                    return old

        elif node.op == '-':
            return -self.evaluate(node.operand, env)
        elif node.op == '!':
            return not self._is_truthy(self.evaluate(node.operand, env))

        raise InterpreterError(f"未知的一元运算符: '{node.op}'")

    def _evaluate_call(self, node: CallExpr, env: Environment):
        callee = self.evaluate(node.callee, env)
        args = [self.evaluate(arg, env) for arg in node.args]

        # 调用内置函数
        if callable(callee):
            return callee(*args)

        # 调用绑定方法
        if isinstance(callee, BoundMethod):
            return self._call_bound_method(callee, args, env)

        # 调用命途本身（作为构造函数）
        if isinstance(callee, LifeClass):
            return callee.instantiate()

        raise InterpreterError(f"无法调用的对象: {type(callee).__name__}")

    def _is_truthy(self, value) -> bool:
        """判断值的真值"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        return True

    def close(self):
        """关闭数据库连接"""
        if self.database:
            self.database.close()
