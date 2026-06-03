# 群星之舞 (Star Dance) - 语法分析器
# 递归下降解析器

from tokens import TokenType
from ast_nodes import *


class ParseError(Exception):
    pass


class Parser:
    """将 Token 流解析为 AST"""

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def error(self, message: str) -> ParseError:
        tok = self.current()
        return ParseError(
            f"[语法错误] 第{tok.line}行第{tok.column}列: {message}"
        )

    def current(self):
        return self.tokens[self.pos]

    def peek(self, offset: int = 0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx].type
        return TokenType.EOF

    def check(self, *types: TokenType) -> bool:
        return self.current().type in types

    def consume(self, *types: TokenType) -> TokenType:
        tok = self.current()
        if tok.type not in types:
            expected = '/'.join(t.name for t in types)
            raise self.error(f"期望 {expected}，但遇到 '{tok.value or tok.type.name}'")
        self.pos += 1
        return tok.type

    def match(self, *types: TokenType) -> bool:
        if self.check(*types):
            self.pos += 1
            return True
        return False

    # ─── 解析入口 ──────────────────────────────────────────────────

    def parse(self) -> Program:
        start_block = None
        main_block = None

        while not self.check(TokenType.EOF):
            if self.check(TokenType.START):
                if start_block is not None:
                    raise self.error("重复的 start 块")
                start_block = self.parse_start_block()
            elif self.check(TokenType.MAIN):
                if main_block is not None:
                    raise self.error("重复的 main 块")
                main_block = self.parse_main_block()
            elif self.check(TokenType.LIFE):
                self.parse_life_decl()  # 顶层life暂时忽略（在start/main里注册）
            elif (self.check(TokenType.FIX) or self.check(TokenType.FINISH)) and self.peek(1) == TokenType.LIFE:
                self.parse_life_decl()
            else:
                raise self.error(f"意外的 token: {self.current().type.name} "
                               f"(start/main/life 只能在顶层使用)")

        if start_block is None:
            start_block = StartBlock([], 0, 0)
        if main_block is None:
            main_block = MainBlock([], 0, 0)

        return Program(start_block, main_block)

    # ─── 块解析 ────────────────────────────────────────────────────

    def parse_start_block(self) -> StartBlock:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.START)
        self.consume(TokenType.LBRACE)
        stmts = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.INT, TokenType.FLOAT, TokenType.STR, TokenType.BOOL, TokenType.LIST):
                stmts.append(self.parse_const_decl())
            else:
                stmts.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return StartBlock(stmts, line, col)

    def parse_main_block(self) -> MainBlock:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.MAIN)
        self.consume(TokenType.LBRACE)
        stmts = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.LIFE):
                stmts.append(self.parse_life_decl())
            elif (self.check(TokenType.FIX) or self.check(TokenType.FINISH)) and self.peek(1) == TokenType.LIFE:
                stmts.append(self.parse_life_decl())
            else:
                stmts.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return MainBlock(stmts, line, col)

    def parse_life_decl(self) -> LifeDecl:
        # 解析可选修饰符 fix / finish
        is_fixed = False
        is_finished = False
        if self.match(TokenType.FIX):
            is_fixed = True
        elif self.match(TokenType.FINISH):
            is_finished = True

        self.consume(TokenType.LIFE)
        name_tok = self.current()
        self.consume(TokenType.IDENTIFIER)
        name = name_tok.value
        parent = None
        if self.match(TokenType.EXTENDS, TokenType.JOIN):
            parent_tok = self.current()
            self.consume(TokenType.IDENTIFIER)
            parent = parent_tok.value
        elif name != 'Object':
            parent = 'Object'  # 所有 life 隐式继承 Object
        self.consume(TokenType.LBRACE)
        body = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.check(TokenType.STATIC):
                body.append(self.parse_thing_decl(is_static=True))
            elif self.check(TokenType.THING):
                body.append(self.parse_thing_decl())
            elif self.check(TokenType.OBJECT, TokenType.INT, TokenType.FLOAT, TokenType.STR, TokenType.BOOL, TokenType.LIST):
                body.append(self.parse_var_decl())
            else:
                raise self.error(f"命途中只能包含 thing/object/var，遇到 {self.current().type.name}")
        self.consume(TokenType.RBRACE)
        return LifeDecl(name, body, parent, is_fixed, is_finished,
                        name_tok.line, name_tok.column)

    def parse_thing_decl(self, is_static: bool = False) -> ThingDecl:
        if is_static:
            self.consume(TokenType.STATIC)
        self.consume(TokenType.THING)
        name_tok = self.current()
        self.consume(TokenType.IDENTIFIER)
        name = name_tok.value
        self.consume(TokenType.LPAREN)
        params = []
        if not self.check(TokenType.RPAREN):
            # 可选类型关键字
            if self.check(TokenType.INT, TokenType.FLOAT, TokenType.STR, TokenType.BOOL,
                          TokenType.LIST, TokenType.OBJECT):
                self.pos += 1  # 跳过类型关键字
            params.append(self.current().value)
            self.consume(TokenType.IDENTIFIER)
            while self.match(TokenType.COMMA):
                # 可选类型关键字
                if self.check(TokenType.INT, TokenType.FLOAT, TokenType.STR, TokenType.BOOL,
                              TokenType.LIST, TokenType.OBJECT):
                    self.pos += 1
                params.append(self.current().value)
                self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        body = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            body.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return ThingDecl(name, params, body, is_static, name_tok.line, name_tok.column)

    # ─── 语句解析 ──────────────────────────────────────────────────

    def parse_statement(self) -> ASTNode:
        if self.check(TokenType.LBRACE):
            return self.parse_block()
        elif self.check(TokenType.OBJECT, TokenType.INT, TokenType.FLOAT,
                       TokenType.STR, TokenType.BOOL, TokenType.LIST):
            return self.parse_var_decl()
        elif self.check(TokenType.IF):
            return self.parse_if_stmt()
        elif self.check(TokenType.WHILE):
            return self.parse_while_stmt()
        elif self.check(TokenType.FOR):
            return self.parse_for_stmt()
        elif self.check(TokenType.FOREACH):
            return self.parse_foreach_stmt()
        elif self.check(TokenType.CASE):
            return self.parse_case_stmt()
        elif self.check(TokenType.RETURN):
            return self.parse_return_stmt()
        elif self.check(TokenType.BREAK):
            return self.parse_break_stmt()
        elif self.check(TokenType.CONTINUE):
            return self.parse_continue_stmt()
        elif self.check(TokenType.CUTDOWN):
            return self.parse_cutdown_stmt()
        elif self.check(TokenType.SEE):
            return self.parse_see_stmt()
        elif self.check(TokenType.THROW):
            return self.parse_throw_stmt()
        elif self.check(TokenType.TRY):
            return self.parse_try_stmt()
        else:
            return self.parse_expr_stmt()

    def parse_block(self) -> Block:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.LBRACE)
        stmts = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            stmts.append(self.parse_statement())
        self.consume(TokenType.RBRACE)
        return Block(stmts, line, col)

    def parse_var_decl(self, consume_semi: bool = True) -> VarDecl:
        line = self.current().line
        col = self.current().column
        var_type = None
        if self.check(TokenType.INT):
            var_type = 'int'; self.pos += 1
        elif self.check(TokenType.FLOAT):
            var_type = 'float'; self.pos += 1
        elif self.check(TokenType.STR):
            var_type = 'str'; self.pos += 1
        elif self.check(TokenType.BOOL):
            var_type = 'bool'; self.pos += 1
        elif self.check(TokenType.LIST):
            var_type = 'list'; self.pos += 1
        else:
            self.match(TokenType.OBJECT)
        name_tok = self.current()
        self.consume(TokenType.IDENTIFIER)
        name = name_tok.value
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()
        if consume_semi:
            self.consume(TokenType.SEMICOLON)
        return VarDecl(name, initializer, var_type, line, col)

    def parse_const_decl(self) -> ConstDecl:
        """解析常量声明: type name = value; (start块专用)"""
        line = self.current().line
        col = self.current().column
        var_type = None
        if self.check(TokenType.INT):
            var_type = 'int'; self.pos += 1
        elif self.check(TokenType.FLOAT):
            var_type = 'float'; self.pos += 1
        elif self.check(TokenType.STR):
            var_type = 'str'; self.pos += 1
        elif self.check(TokenType.BOOL):
            var_type = 'bool'; self.pos += 1
        elif self.check(TokenType.LIST):
            var_type = 'list'; self.pos += 1
        name_tok = self.current()
        self.consume(TokenType.IDENTIFIER)
        name = name_tok.value
        self.consume(TokenType.ASSIGN)  # 常量必须有初始值
        initializer = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ConstDecl(name, initializer, var_type, line, col)

    # ─── 特定语句解析 ────────────────────────────────────────────

    def parse_if_stmt(self) -> IfStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        then_block = [self.parse_statement()]
        else_block = None
        if self.match(TokenType.ELSE):
            else_block = [self.parse_statement()]
        return IfStmt(condition, then_block, else_block, line, col)

    def parse_while_stmt(self) -> WhileStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        body = [self.parse_statement()]
        return WhileStmt(condition, body, line, col)

    def parse_for_stmt(self) -> ForStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        init = None
        if not self.check(TokenType.SEMICOLON):
            if self.check(TokenType.OBJECT, TokenType.INT, TokenType.FLOAT,
                          TokenType.STR, TokenType.BOOL):
                init = self.parse_var_decl(consume_semi=False)
            else:
                init = self.parse_expr_stmt_no_semi()
        self.consume(TokenType.SEMICOLON)
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        update = None
        if not self.check(TokenType.RPAREN):
            update = self.parse_expression()
        self.consume(TokenType.RPAREN)
        body = [self.parse_statement()]
        return ForStmt(init, condition, update, body, line, col)

    def parse_foreach_stmt(self) -> ForeachStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.FOREACH)
        var_tok = self.current()
        self.consume(TokenType.IDENTIFIER)
        var_name = var_tok.value
        self.consume(TokenType.IN)
        iterable = self.parse_expression()
        body = [self.parse_statement()]
        return ForeachStmt(var_name, iterable, body, line, col)

    def parse_case_stmt(self) -> CaseStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.CASE)
        self.consume(TokenType.LPAREN)
        expr = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LBRACE)
        when_clauses = []
        else_body = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            if self.match(TokenType.WHEN):
                val = self.parse_expression()
                body = [self.parse_statement()]
                when_clauses.append(WhenClause(val, body, line, col))
            elif self.match(TokenType.ELSE):
                else_body = []
                while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
                    else_body.append(self.parse_statement())
                break
            else:
                raise self.error(f"case 中只能包含 when 或 else 分支")
        self.consume(TokenType.RBRACE)
        return CaseStmt(expr, when_clauses, else_body, line, col)

    def parse_return_stmt(self) -> ReturnStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.RETURN)
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ReturnStmt(value, line, col)

    def parse_break_stmt(self) -> BreakStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.BREAK)
        self.consume(TokenType.SEMICOLON)
        return BreakStmt(line, col)

    def parse_continue_stmt(self) -> ContinueStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.CONTINUE)
        self.consume(TokenType.SEMICOLON)
        return ContinueStmt(line, col)

    def parse_cutdown_stmt(self) -> CutDownStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.CUTDOWN)
        self.consume(TokenType.SEMICOLON)
        return CutDownStmt(line, col)

    def parse_see_stmt(self) -> SeeStmt:
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.SEE)
        self.consume(TokenType.LPAREN)
        args = []
        if not self.check(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                args.append(self.parse_expression())
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.SEMICOLON)
        return SeeStmt(args, line, col)

    def parse_throw_stmt(self) -> ThrowStmt:
        """解析抛出异常: throw expr;"""
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.THROW)
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ThrowStmt(expr, line, col)

    def parse_try_stmt(self) -> TryStmt:
        """解析异常捕获: try { body } [catch (var) { body }] [finally { body }]"""
        line = self.current().line
        col = self.current().column
        self.consume(TokenType.TRY)
        self.consume(TokenType.LBRACE)
        try_body = []
        while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
            try_body.append(self.parse_statement())
        self.consume(TokenType.RBRACE)

        catch_var = None
        catch_body = None
        if self.match(TokenType.CATCH):
            self.consume(TokenType.LPAREN)
            var_tok = self.current()
            self.consume(TokenType.IDENTIFIER)
            catch_var = var_tok.value
            self.consume(TokenType.RPAREN)
            self.consume(TokenType.LBRACE)
            catch_body = []
            while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
                catch_body.append(self.parse_statement())
            self.consume(TokenType.RBRACE)

        finally_body = None
        if self.match(TokenType.FINALLY):
            self.consume(TokenType.LBRACE)
            finally_body = []
            while not self.check(TokenType.RBRACE) and not self.check(TokenType.EOF):
                finally_body.append(self.parse_statement())
            self.consume(TokenType.RBRACE)

        return TryStmt(try_body, catch_var, catch_body, finally_body, line, col)

    def parse_expr_stmt_no_semi(self) -> ExprStmt:
        line = self.current().line
        col = self.current().column
        expr = self.parse_assignment()
        return ExprStmt(expr, line, col)

    def parse_expr_stmt(self) -> ExprStmt:
        line = self.current().line
        col = self.current().column
        expr = self.parse_assignment()
        self.consume(TokenType.SEMICOLON)
        return ExprStmt(expr, line, col)

    # ─── 表达式解析 ────────────────────────────────────────────────
    # 优先级（从低到高）:
    #   assignment   = 
    #   or           ||
    #   and          &&  
    #   bitor        |
    #   bitand       &
    #   equality     == !=
    #   comparison   < > <= >=
    #   shift        << >> >>>
    #   term         + -
    #   factor       * / %
    #   unary        ! - ++ --
    #   postfix      ++ --
    #   primary

    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        line = self.current().line
        col = self.current().column
        expr = self.parse_or()
        if self.match(TokenType.ASSIGN):
            value = self.parse_assignment()
            if isinstance(expr, Identifier):
                return Assign(Identifier(expr.name), value, line, col)
            elif isinstance(expr, GetAttr):
                return Assign(expr, value, line, col)
            else:
                raise ParseError(f"[语法错误] 第{line}行: 无效的赋值目标")
        return expr

    def parse_or(self) -> ASTNode:
        expr = self.parse_and()
        while self.match(TokenType.OR):
            op = self.tokens[self.pos - 1]
            right = self.parse_and()
            expr = BinaryOp(expr, '||', right, op.line, op.column)
        return expr

    def parse_and(self) -> ASTNode:
        expr = self.parse_bitor()
        while self.match(TokenType.AND):
            op = self.tokens[self.pos - 1]
            right = self.parse_bitor()
            expr = BinaryOp(expr, '&&', right, op.line, op.column)
        return expr

    def parse_bitor(self) -> ASTNode:
        """按位或: |"""
        expr = self.parse_bitand()
        while self.match(TokenType.BIT_OR):
            op = self.tokens[self.pos - 1]
            right = self.parse_bitand()
            expr = BinaryOp(expr, '|', right, op.line, op.column)
        return expr

    def parse_bitand(self) -> ASTNode:
        """按位与: &"""
        expr = self.parse_equality()
        while self.match(TokenType.BIT_AND):
            op = self.tokens[self.pos - 1]
            right = self.parse_equality()
            expr = BinaryOp(expr, '&', right, op.line, op.column)
        return expr

    def parse_equality(self) -> ASTNode:
        expr = self.parse_comparison()
        while self.check(TokenType.EQ, TokenType.NEQ, TokenType.EQ_STRICT):
            op = self.current()
            self.pos += 1
            right = self.parse_comparison()
            expr = BinaryOp(expr, op.value, right, op.line, op.column)
        return expr

    def parse_comparison(self) -> ASTNode:
        expr = self.parse_shift()
        while self.check(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE,
                         TokenType.NGT, TokenType.NLT):
            op = self.current()
            self.pos += 1
            right = self.parse_shift()
            expr = BinaryOp(expr, op.value, right, op.line, op.column)
        return expr

    def parse_shift(self) -> ASTNode:
        """移位: << >> >>>"""
        expr = self.parse_term()
        while self.check(TokenType.SHL, TokenType.SHR, TokenType.USHR):
            op = self.current()
            self.pos += 1
            right = self.parse_term()
            expr = BinaryOp(expr, op.value, right, op.line, op.column)
        return expr

    def parse_term(self) -> ASTNode:
        expr = self.parse_factor()
        while self.check(TokenType.PLUS, TokenType.MINUS):
            op = self.current()
            self.pos += 1
            right = self.parse_factor()
            expr = BinaryOp(expr, op.value, right, op.line, op.column)
        return expr

    def parse_factor(self) -> ASTNode:
        expr = self.parse_unary()
        while self.check(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            op = self.current()
            self.pos += 1
            right = self.parse_unary()
            expr = BinaryOp(expr, op.value, right, op.line, op.column)
        return expr

    def parse_unary(self) -> ASTNode:
        if self.check(TokenType.NOT, TokenType.MINUS, TokenType.INCREMENT, TokenType.DECREMENT):
            op = self.current()
            self.pos += 1
            operand = self.parse_unary()
            return UnaryOp(op.value, operand, True, op.line, op.column)
        return self.parse_postfix()

    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        if self.check(TokenType.INCREMENT, TokenType.DECREMENT):
            op = self.current()
            self.pos += 1
            expr = UnaryOp(op.value, expr, False, op.line, op.column)
        return expr

    def parse_primary(self) -> ASTNode:
        tok = self.current()
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        if self.match(TokenType.LBRACKET):
            return self.parse_list_literal(tok.line, tok.column)
        if self.match(TokenType.NEW):
            name_tok = self.current()
            if self.check(TokenType.IDENTIFIER):
                self.consume(TokenType.IDENTIFIER)
                name = name_tok.value
            elif self.check(TokenType.SUPER):
                self.consume(TokenType.SUPER)
                name = 'SUPPER'
            else:
                raise self.error("new 后需要命途名或 SUPPER")
            # 解析构造参数（可选：无括号时视为空参 new ClassName）
            args = []
            if self.check(TokenType.LPAREN):
                args = self.parse_call_args()
            return NewExpr(name, args, name_tok.line, name_tok.column)
        if self.check(TokenType.NUMBER):
            self.pos += 1
            return Literal(tok.value, tok.line, tok.column)
        if self.check(TokenType.STRING):
            self.pos += 1
            return Literal(tok.value, tok.line, tok.column)
        if self.match(TokenType.TRUE):
            return Literal(True, tok.line, tok.column)
        if self.match(TokenType.FALSE):
            return Literal(False, tok.line, tok.column)
        if self.match(TokenType.NULL):
            return Literal(None, tok.line, tok.column)
        if self.check(TokenType.THIS):
            self.pos += 1
            expr = Identifier('this', tok.line, tok.column)
            expr = self._parse_chain(expr)
            return expr
        if self.check(TokenType.SUPER):
            self.pos += 1
            expr = Identifier('SUPPER', tok.line, tok.column)
            expr = self._parse_chain(expr)
            return expr
        if self.check(TokenType.FIX):
            self.pos += 1
            expr = Identifier('fix', tok.line, tok.column)
            if self.check(TokenType.LPAREN):
                expr = self.finish_call(expr)
            return expr
        # 允许关键字作为函数名出现在表达式里：see(), len(), int(), str() 等
        if self.check(TokenType.SEE, TokenType.LIST,
                      TokenType.INT, TokenType.FLOAT, TokenType.STR, TokenType.BOOL,
                      TokenType.INSERT):
            kw = self.current()
            self.pos += 1
            name = kw.type.name.lower()
            expr = Identifier(name, kw.line, kw.column)
            expr = self._parse_chain(expr)
            return expr
        if self.check(TokenType.IDENTIFIER):
            self.pos += 1
            expr = Identifier(tok.value, tok.line, tok.column)
            expr = self._parse_chain(expr)
            return expr
        raise self.error(f"期望表达式，但遇到 '{tok.value or tok.type.name}'")

    def parse_list_literal(self, line: int, col: int) -> ListLiteral:
        entries = []
        has_keys = False
        first = True
        while not self.check(TokenType.RBRACKET) and not self.check(TokenType.EOF):
            if not first:
                self.consume(TokenType.COMMA)
                if self.check(TokenType.RBRACKET):
                    break
            first = False
            if self.check(TokenType.IDENTIFIER) and self.peek(1) == TokenType.COLON:
                key_token = self.current()
                self.pos += 1
                self.consume(TokenType.COLON)
                value_node = self.parse_expression()
                entries.append((key_token.value, value_node))
                has_keys = True
            elif self.check(TokenType.STRING) and self.peek(1) == TokenType.COLON:
                key_token = self.current()
                self.pos += 1
                self.consume(TokenType.COLON)
                value_node = self.parse_expression()
                entries.append((key_token.value, value_node))
                has_keys = True
            elif self.check(TokenType.NUMBER) and self.peek(1) == TokenType.COLON:
                key_token = self.current()
                self.pos += 1
                self.consume(TokenType.COLON)
                value_node = self.parse_expression()
                entries.append((key_token.value, value_node))
                has_keys = True
            else:
                value_node = self.parse_expression()
                entries.append((None, value_node))
        self.consume(TokenType.RBRACKET)
        return ListLiteral(entries, has_keys, line, col)

    def _parse_chain(self, expr: ASTNode) -> ASTNode:
        while self.check(TokenType.DOT):
            dot_tok = self.current()
            self.pos += 1
            attr_tok = self.current()
            self.consume(TokenType.IDENTIFIER)
            expr = GetAttr(expr, attr_tok.value, dot_tok.line, dot_tok.column)
            if self.check(TokenType.LPAREN):
                expr = self.finish_call(expr)
        if self.check(TokenType.LPAREN):
            expr = self.finish_call(expr)
        return expr

    def finish_call(self, callee: ASTNode) -> CallExpr:
        line = self.current().line
        col = self.current().column
        args = self.parse_call_args()
        return CallExpr(callee, args, line, col)

    def parse_call_args(self) -> list:
        """解析调用参数列表 (arg1, arg2, ...)"""
        self.consume(TokenType.LPAREN)
        args = []
        if not self.check(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                args.append(self.parse_expression())
        self.consume(TokenType.RPAREN)
        return args
