def _line_comment(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if stripped.startswith("def "):
        return "# 定义函数"
    if stripped.startswith("class "):
        return "# 定义类"
    if stripped.startswith("@"):
        return "# 应用装饰器"
    if stripped.startswith("try:"):
        return "# 尝试执行可能出错的代码"
    if stripped.startswith("except "):
        return "# 捕获指定异常"
    if stripped.startswith("else:"):
        return "# 没有异常或条件不满足时执行"
    if stripped.startswith("finally:"):
        return "# 无论是否出错都会执行"
    if stripped.startswith("with "):
        return "# 使用上下文管理器"
    if stripped.startswith("for "):
        return "# 循环遍历序列"
    if stripped.startswith("while "):
        return "# 条件循环"
    if stripped.startswith("if "):
        return "# 条件判断"
    if stripped.startswith("elif "):
        return "# 继续判断另一个条件"
    if stripped.startswith("match "):
        return "# 按值匹配分支"
    if stripped.startswith("case "):
        return "# 匹配到一个分支"
    if stripped.startswith("return "):
        return "# 返回结果"
    if stripped.startswith("yield"):
        return "# 产出生成器的一个值"
    if stripped.startswith("print("):
        return "# 输出结果"
    if "input().split()" in stripped:
        return "# 读取一行输入并按空格拆分"
    if "map(int" in stripped:
        return "# 将输入内容转换为整数"
    if stripped.startswith("import "):
        return "# 导入模块"
    if stripped.startswith("from "):
        return "# 从模块导入内容"
    if " = " in stripped and "(" in stripped:
        return "# 调用函数并把结果赋值给变量"
    if " = " in stripped:
        return "# 给变量赋值"
    if stripped.endswith(":"):
        return "# 进入该代码块"
    return "# 执行本行"


def add_line_comments(code: str) -> str:
    lines = []
    for line in code.splitlines():
        comment = _line_comment(line)
        if comment is None:
            lines.append(line)
        else:
            indent = line[: len(line) - len(line.lstrip())]
            lines.append(f"{line}  {comment}")
    return "\n".join(lines) + "\n"
