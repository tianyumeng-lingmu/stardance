# 群星之舞 (Star Dance) - 抽象语法树节点

from typing import Optional


class ASTNode:
    """所有 AST 节点的基类"""
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


# ─── 语句 (Statement) ───────────────────────────────────────────────

class Program(ASTNode):
    """程序根节点：包含 start块, main块, 和模块级函数声明"""
    def __init__(self, start_block, main_block, func_decls=None):
        super().__init__(0, 0)
        self.start_block = start_block   # StartBlock | None
        self.main_block = main_block     # MainBlock | None
        self.func_decls = func_decls or []  # list[ThingDecl] - 模块级函数

    def __repr__(self):
        return f"Program(start={self.start_block}, main={self.main_block})"


class Block(ASTNode):
    """代码块：一系列语句"""
    def __init__(self, statements: list, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self):
        return f"Block({len(self.statements)} stmts)"


class StartBlock(Block):
    """start {} 块"""
    def __repr__(self):
        return f"StartBlock({len(self.statements)} stmts)"


class MainBlock(Block):
    """main {} 块"""
    def __repr__(self):
        return f"MainBlock({len(self.statements)} stmts)"


class LifeDecl(ASTNode):
    """命途声明: [fix|finish] life name [extends|join parent] { body }"""
    def __init__(self, name: str, body: list, parent: Optional[str] = None,
                 is_fixed: bool = False, is_finished: bool = False,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.body = body          # list[ASTNode]
        self.parent = parent      # 父命途名 | None
        self.is_fixed = is_fixed
        self.is_finished = is_finished

    def __repr__(self):
        parts = []
        if self.is_fixed: parts.append("fix")
        if self.is_finished: parts.append("finish")
        parts.append(self.name)
        if self.parent:
            parts.append(f"->{self.parent}")
        return f"LifeDecl({' '.join(parts)}, {len(self.body)} members)"


class ThingDecl(ASTNode):
    """方法声明: thing name(params) { body }"""
    def __init__(self, name: str, params: list[str], body: list[ASTNode],
                 is_static: bool = False, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.params = params      # list[str]
        self.body = body          # list[ASTNode]
        self.is_static = is_static

    def __repr__(self):
        return f"ThingDecl({self.name}({','.join(self.params)}), {len(self.body)} stmts)"


class VarDecl(ASTNode):
    """变量声明: (object|var|int|float|str|list) name [= expr];"""
    def __init__(self, name: str, initializer: Optional[ASTNode] = None,
                 var_type: Optional[str] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.initializer = initializer
        self.var_type = var_type

    def __repr__(self):
        return f"VarDecl({self.name} = {self.initializer}, type={self.var_type})"


class ConstDecl(ASTNode):
    """常量声明: type name = value; (只能在start块中使用)"""
    def __init__(self, name: str, initializer: ASTNode, var_type: Optional[str] = None,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.initializer = initializer
        self.var_type = var_type

    def __repr__(self):
        return f"ConstDecl({self.name} = {self.initializer}, type={self.var_type})"


class Assign(ASTNode):
    """赋值语句: target = expr;"""
    def __init__(self, target: ASTNode, value: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.target = target
        self.value = value

    def __repr__(self):
        return f"Assign({self.target} = {self.value})"


class IfStmt(ASTNode):
    """条件语句"""
    def __init__(self, condition: ASTNode, then_block: list[ASTNode],
                 else_block: Optional[list[ASTNode]] = None,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"IfStmt(cond={self.condition})"


class WhileStmt(ASTNode):
    """循环语句"""
    def __init__(self, condition: ASTNode, body: list[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStmt(cond={self.condition})"


class ForStmt(ASTNode):
    """For循环: for init; cond; update { body }"""
    def __init__(self, init: Optional[ASTNode], condition: Optional[ASTNode],
                 update: Optional[ASTNode], body: list[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForStmt(...)"


class ReturnStmt(ASTNode):
    """返回语句"""
    def __init__(self, value: Optional[ASTNode] = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"ReturnStmt({self.value})"


class ExprStmt(ASTNode):
    """表达式语句: expression;"""
    def __init__(self, expr: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expr = expr

    def __repr__(self):
        return f"ExprStmt({self.expr})"


class SeeStmt(ASTNode):
    """打印语句: see(expr1, expr2, ...);"""
    def __init__(self, args: list, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.args = args   # list[ASTNode]

    def __repr__(self):
        return f"SeeStmt({self.args})"


class ThrowStmt(ASTNode):
    """抛出异常: throw expr;"""
    def __init__(self, expr: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expr = expr

    def __repr__(self):
        return f"ThrowStmt({self.expr})"


class TryStmt(ASTNode):
    """异常捕获: try { body } catch(var) { body } finally { body }
    catch_var 为 None 时表示没有 catch 块
    finally_body 为 None 时表示没有 finally 块"""
    def __init__(self, try_body: list, catch_var: str = None,
                 catch_body: list = None, finally_body: list = None,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.try_body = try_body
        self.catch_var = catch_var
        self.catch_body = catch_body or []
        self.finally_body = finally_body or []

    def __repr__(self):
        parts = [f"Try({len(self.try_body)} stmts)"]
        if self.catch_var:
            parts.append(f"catch({self.catch_var})")
        if self.finally_body:
            parts.append("finally")
        return f"TryStmt({' '.join(parts)})"


# ─── 表达式 (Expression) ───────────────────────────────────────────

class BinaryOp(ASTNode):
    """二元运算: left op right"""
    def __init__(self, left: ASTNode, op: str, right: ASTNode,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"


class UnaryOp(ASTNode):
    """一元运算: op operand"""
    def __init__(self, op: str, operand: ASTNode, is_prefix: bool = True,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.op = op
        self.operand = operand
        self.is_prefix = is_prefix

    def __repr__(self):
        if self.is_prefix:
            return f"UnaryOp({self.op}{self.operand})"
        return f"UnaryOp({self.operand}{self.op})"


class Literal(ASTNode):
    """字面量"""
    def __init__(self, value: object, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"Literal({self.value!r})"


class Identifier(ASTNode):
    """标识符引用"""
    def __init__(self, name: str, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class NewExpr(ASTNode):
    """创建实例: new ClassName"""
    def __init__(self, class_name: str, args: list = None, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.class_name = class_name
        self.args = args or []

    def __repr__(self):
        return f"NewExpr({self.class_name}, args={self.args})"


class CallExpr(ASTNode):
    """函数/方法调用: callee(args)"""
    def __init__(self, callee: ASTNode, args: list[ASTNode],
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"CallExpr({self.callee}, args={self.args})"


class GetAttr(ASTNode):
    """属性访问: object.attr"""
    def __init__(self, obj: ASTNode, attr: str, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.obj = obj
        self.attr = attr

    def __repr__(self):
        return f"GetAttr({self.obj}.{self.attr})"


class IndexExpr(ASTNode):
    """下标访问: expr[idx]"""
    def __init__(self, obj: ASTNode, index: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.obj = obj
        self.index = index

    def __repr__(self):
        return f"IndexExpr({self.obj}[{self.index}])"


class ListLiteral(ASTNode):
    """列表字面量: [expr, ...] 或 [key: expr, ...]
    entries: list of (key_str, value_node) tuples — key 为 None 表示索引项"""
    def __init__(self, entries: list, has_keys: bool = False,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.entries = entries    # list of (key_or_None, value_node)
        self.has_keys = has_keys

    def __repr__(self):
        return f"ListLiteral({len(self.entries)} items, dict={self.has_keys})"


class ForeachStmt(ASTNode):
    """遍历循环: foreach var in expr { body }"""
    def __init__(self, var_name: str, iterable: ASTNode, body: list,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.var_name = var_name
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"ForeachStmt({self.var_name} in {self.iterable})"


class CaseStmt(ASTNode):
    """分支语句: case(expr) { when val { ... } else { ... } }"""
    def __init__(self, expr: ASTNode, when_clauses: list, else_body: list = None,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expr = expr
        self.when_clauses = when_clauses    # list of WhenClause
        self.else_body = else_body or []

    def __repr__(self):
        return f"CaseStmt(expr={self.expr}, {len(self.when_clauses)} whens)"


class WhenClause(ASTNode):
    """when 分支子句: when value { body }"""
    def __init__(self, value: ASTNode, body: list,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.value = value
        self.body = body

    def __repr__(self):
        return f"WhenClause({self.value})"


class BreakStmt(ASTNode):
    """跳出当前循环"""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__(line, column)

    def __repr__(self):
        return "BreakStmt()"


class PassStmt(ASTNode):
    """空语句"""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__(line, column)

    def __repr__(self):
        return "PassStmt()"


class ContinueStmt(ASTNode):
    """继续下一次循环"""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__(line, column)

    def __repr__(self):
        return "ContinueStmt()"


class CutDownStmt(ASTNode):
    """中断所有嵌套循环"""
    def __init__(self, line: int = 0, column: int = 0):
        super().__init__(line, column)

    def __repr__(self):
        return "CutDownStmt()"


class AnonymouFunc(ASTNode):
    """匿名函数: anonymou(params) { body }"""
    def __init__(self, params: list[str], body: list,
                 line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.params = params
        self.body = body

    def __repr__(self):
        return f"AnonymouFunc(({','.join(self.params)}), {len(self.body)} stmts)"


class NamedArgument(ASTNode):
    """命名参数: name = value (在函数调用中使用)"""
    def __init__(self, name: str, value: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.name = name
        self.value = value

    def __repr__(self):
        return f"NamedArgument({self.name} = {self.value})"


class UseStmt(ASTNode):
    """导入包语句: use package_name;"""
    def __init__(self, package_name: str, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.package_name = package_name

    def __repr__(self):
        return f"UseStmt({self.package_name})"


class PauseStmt(ASTNode):
    """暂停语句（生成器）: pause expr;"""
    def __init__(self, expr: ASTNode, line: int = 0, column: int = 0):
        super().__init__(line, column)
        self.expr = expr

    def __repr__(self):
        return f"PauseStmt({self.expr})"
