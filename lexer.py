# 群星之舞 (Star Dance) - 词法分析器

from tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    pass


class Lexer:
    """词法分析器：将 .star 源码转换为 Token 流"""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0          # 当前字符位置
        self.line = 1         # 当前行号
        self.col = 1          # 当前列号
        self.tokens = []      # 生成的 token 列表

    def error(self, message: str) -> LexerError:
        return LexerError(f"[词法错误] 第{self.line}行第{self.col}列: {message}")

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= len(self.source):
            return '\0'
        return self.source[idx]

    def advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        self.col += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch in ' \t\r':
                self.advance()
            elif ch == '\n':
                self.advance()
                self.line += 1
                self.col = 1
            else:
                break

    def skip_comment(self):
        if self.peek() == '/':
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.advance()
        elif self.peek() == '*':
            self.advance()
            while self.pos < len(self.source):
                if self.source[self.pos] == '\n':
                    self.line += 1
                    self.col = 1
                if self.source[self.pos] == '*' and self.peek(1) == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()

    def read_string(self, quote: str) -> str:
        result = []
        start_line = self.line
        while self.pos < len(self.source):
            ch = self.advance()
            if ch == '\\':
                next_ch = self.advance()
                escape_map = {
                    'n': '\n', 't': '\t', 'r': '\r',
                    '"': '"', "'": "'", '\\': '\\',
                }
                result.append(escape_map.get(next_ch, next_ch))
            elif ch == quote:
                return ''.join(result)
            elif ch == '\n':
                self.line += 1
                self.col = 1
                result.append(ch)
            else:
                result.append(ch)
        raise self.error(f"未闭合的字符串，起始于第{start_line}行")

    def read_number(self) -> Token:
        line = self.line
        col = self.col
        num_str = []
        is_float = False
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            if self.source[self.pos] == '.':
                if is_float:
                    break
                is_float = True
            num_str.append(self.advance())
        value = float(''.join(num_str)) if is_float else int(''.join(num_str))
        return Token(TokenType.NUMBER, value, line, col)

    def read_identifier(self) -> Token:
        line = self.line
        col = self.col
        ident = []
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            ident.append(self.advance())
        word = ''.join(ident)
        token_type = KEYWORDS.get(word, TokenType.IDENTIFIER)
        value = word if token_type == TokenType.IDENTIFIER else None
        return Token(token_type, value, line, col)

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch in ' \t\r\n':
                self.skip_whitespace()
                continue
            if ch == '/' and self.peek(1) in ('/', '*'):
                self.skip_comment()
                continue
            line = self.line
            col = self.col
            if ch in ('"', "'"):
                self.advance()
                value = self.read_string(ch)
                tokens.append(Token(TokenType.STRING, value, line, col))
                continue
            if ch.isdigit():
                tokens.append(self.read_number())
                continue
            if ch.isalpha() or ch == '_':
                tokens.append(self.read_identifier())
                continue

            # 三字符运算符: >>>, <<<, ===
            three_char = ch + self.peek(1) + self.peek(2) if self.pos + 2 < len(self.source) else ''
            if three_char == '>>>':
                self.advance(); self.advance(); self.advance()
                tokens.append(Token(TokenType.USHR, '>>>', line, col))
                continue
            if three_char == '<<<':
                self.advance(); self.advance(); self.advance()
                tokens.append(Token(TokenType.SHL, '<<<', line, col))
                continue
            if three_char == '===':
                self.advance(); self.advance(); self.advance()
                tokens.append(Token(TokenType.EQ_STRICT, '===', line, col))
                continue

            # 双字符运算符
            two_char = ch + self.peek(1) if self.pos + 1 < len(self.source) else ch
            two_char_map = {
                '==': TokenType.EQ, '!=': TokenType.NEQ,
                '<=': TokenType.LE, '>=': TokenType.GE,
                '&&': TokenType.AND, '||': TokenType.OR,
                '++': TokenType.INCREMENT, '--': TokenType.DECREMENT,
                '<<': TokenType.SHL, '>>': TokenType.SHR,
                '!>': TokenType.NGT, '!<': TokenType.NLT,
                '/^': TokenType.IDIV,
            }
            if two_char in two_char_map:
                self.advance()
                self.advance()
                tokens.append(Token(two_char_map[two_char], two_char, line, col))
                continue

            # 单字符
            single_char_map = {
                '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON, '.': TokenType.DOT,
                ',': TokenType.COMMA, ':': TokenType.COLON,
                '=': TokenType.ASSIGN, '+': TokenType.PLUS,
                '-': TokenType.MINUS, '*': TokenType.STAR,
                '/': TokenType.SLASH, '%': TokenType.MOD,
                '<': TokenType.LT, '>': TokenType.GT,
                '!': TokenType.NOT,
                '&': TokenType.BIT_AND,
                '|': TokenType.BIT_OR,
            }
            if ch in single_char_map:
                self.advance()
                tokens.append(Token(single_char_map[ch], ch, line, col))
                continue
            raise self.error(f"无法识别的字符: '{ch}' (U+{ord(ch):04X})")
        tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return tokens
