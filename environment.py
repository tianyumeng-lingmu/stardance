# 群星之舞 (Star Dance) - 环境与作用域管理

from typing import Optional


class ReturnException(Exception):
    """用于实现 return 语句的异常控制流"""
    def __init__(self, value):
        self.value = value


class Environment:
    """作用域环境，管理变量绑定"""

    def __init__(self, parent: Optional['Environment'] = None, name: str = "<global>"):
        self.parent = parent
        self.name = name
        self._values = {}       # dict[str, object]
        self._classes = {}      # dict[str, LifeClass]  - 命途定义
        self._consts = set()    # set[str] - 常量名集合
        self._return_value = None

    def define(self, name: str, value) -> None:
        """定义或更新当前作用域的变量"""
        self._values[name] = value

    def define_constant(self, name: str, value) -> None:
        """定义常量（不可变）"""
        self._values[name] = value
        self._consts.add(name)

    def is_constant(self, name: str) -> bool:
        """检查变量是否是常量"""
        if name in self._consts:
            return True
        if self.parent is not None:
            return self.parent.is_constant(name)
        return False

    def get(self, name: str):
        """获取变量的值，沿作用域链向上查找"""
        if name in self._values:
            return self._values[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"[运行时错误] 未定义的变量: '{name}'")

    def has(self, name: str) -> bool:
        """检查变量是否在当前作用域或父作用域中定义"""
        if name in self._values:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def assign(self, name: str, value) -> None:
        """为已有的变量赋值（沿作用域链查找）"""
        # 检查是否为常量
        if name in self._consts:
            raise NameError(f"[运行时错误] 常量 '{name}' 不可修改")
        if name in self._values:
            self._values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(name, value)
            return
        raise NameError(f"[运行时错误] 未定义的变量: '{name}'")

    # ─── 命途管理 ──────────────────────────────────────────────────

    def define_class(self, name: str, life_class) -> None:
        """注册命途定义"""
        self._classes[name] = life_class

    def get_class(self, name: str):
        """获取命途定义"""
        if name in self._classes:
            return self._classes[name]
        if self.parent is not None:
            return self.parent.get_class(name)
        raise NameError(f"[运行时错误] 未定义的命途: '{name}'")

    def has_class(self, name: str) -> bool:
        """检查命途是否定义"""
        if name in self._classes:
            return True
        if self.parent is not None:
            return self.parent.has_class(name)
        return False

    def create_child(self, name: str = "<block>") -> 'Environment':
        """创建子作用域"""
        return Environment(parent=self, name=name)

    def __repr__(self):
        return f"Environment({self.name}, vars={list(self._values.keys())}, classes={list(self._classes.keys())})"
