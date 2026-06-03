# 群星之舞 (Star Dance) - 标记定义

from enum import Enum, auto


class TokenType(Enum):
    # 关键字
    LIFE = auto()       # life (命途，相当于class)
    THING = auto()      # thing (方法/函数)
    OBJECT = auto()     # object (声明变量)
    NEW = auto()        # new (创建实例)
    START = auto()      # start (入口配置块)
    MAIN = auto()       # main (主程序块)
    IF = auto()         # if
    ELSE = auto()       # else
    WHILE = auto()      # while
    FOR = auto()        # for
    FOREACH = auto()    # foreach
    IN = auto()         # in
    RETURN = auto()     # return
    BREAK = auto()      # break
    CONTINUE = auto()   # continue
    CUTDOWN = auto()    # cutdown (跳出所有循环)
    TRUE = auto()       # true
    FALSE = auto()      # false
    NULL = auto()       # null
    VAR = auto()        # var (类型化变量声明)
    THIS = auto()       # this (当前实例引用)
    SUPER = auto()      # super (父类引用)
    EXTENDS = auto()    # extends (继承)
    STATIC = auto()     # static (静态)
    SEE = auto()        # see (打印)
    INSERT = auto()     # insert (输入)
    LIST = auto()       # list (列表/字典类型)
    FIX = auto()        # fix (固定命途/冻结为不可变)
    FINISH = auto()     # finish (完成命途，不可被继承)
    JOIN = auto()       # join (继承，相当于extends)
    INT = auto()        # int 类型
    FLOAT = auto()      # float 类型
    STR = auto()        # str 类型
    BOOL = auto()       # bool 类型
    CASE = auto()       # case (switch)
    WHEN = auto()       # when (case 分支)
    # 错误处理
    THROW = auto()      # throw (抛出异常)
    TRY = auto()        # try (异常捕获)
    CATCH = auto()      # catch (捕获异常)
    FINALLY = auto()    # finally (最终执行)

    # 符号
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACKET = auto()   # [
    RBRACKET = auto()   # ]
    SEMICOLON = auto()  # ;
    DOT = auto()        # .
    COMMA = auto()      # ,
    COLON = auto()      # :
    ASSIGN = auto()     # =
    PLUS = auto()       # +
    MINUS = auto()      # -
    STAR = auto()       # *
    SLASH = auto()      # /
    MOD = auto()        # %
    EQ = auto()         # ==
    NEQ = auto()        # !=
    EQ_STRICT = auto()  # === (严格相等)
    LT = auto()         # <
    GT = auto()         # >
    LE = auto()         # <=
    GE = auto()         # >=
    NGT = auto()        # !> (不大于)
    NLT = auto()        # !< (不小于)
    AND = auto()        # &&
    OR = auto()         # ||
    NOT = auto()        # !
    BIT_AND = auto()    # &  (按位与)
    BIT_OR = auto()     # |  (按位或)
    SHL = auto()        # << (左移)
    SHR = auto()        # >> (右移)
    USHR = auto()       # >>> (无符号右移)
    INCREMENT = auto()  # ++
    DECREMENT = auto()  # --

    # 字面量 & 标识符
    IDENTIFIER = auto()   # 标识符
    STRING = auto()       # 字符串
    NUMBER = auto()       # 数字 (整数/浮点数)

    # 特殊
    EOF = auto()          # 文件结束


class Token:
    def __init__(self, type_: TokenType, value: object, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, L{self.line}:{self.column})"


# 关键字映射
KEYWORDS = {
    'life': TokenType.LIFE,
    'thing': TokenType.THING,
    'object': TokenType.OBJECT,
    'new': TokenType.NEW,
    'start': TokenType.START,
    'main': TokenType.MAIN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'foreach': TokenType.FOREACH,
    'in': TokenType.IN,
    'return': TokenType.RETURN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'cutdown': TokenType.CUTDOWN,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'null': TokenType.NULL,
    'var': TokenType.VAR,
    'this': TokenType.THIS,
    'SUPPER': TokenType.SUPER,
    'extends': TokenType.EXTENDS,
    'static': TokenType.STATIC,
    'see': TokenType.SEE,
    'insert': TokenType.INSERT,
    'list': TokenType.LIST,
    'fix': TokenType.FIX,
    'finish': TokenType.FINISH,
    'join': TokenType.JOIN,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'str': TokenType.STR,
    'bool': TokenType.BOOL,
    'case': TokenType.CASE,
    'when': TokenType.WHEN,
    'throw': TokenType.THROW,
    'try': TokenType.TRY,
    'catch': TokenType.CATCH,
    'finally': TokenType.FINALLY,
}
