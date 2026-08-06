CASE_STUDY_PROBLEMS = [
    {
        "title": "案例：学生成绩分析",
        "description": (
            "输入第一行为学生人数 n，接下来 n 行每行包含姓名和成绩，"
            "姓名与成绩用空格分隔。输出两行：第一行为最高分学生的姓名和成绩"
            "（用空格分隔，若并列输出第一个出现的学生），"
            "第二行为全部学生的平均分，保留 1 位小数。\n\n"
            "示例输入：\n"
            "3\n"
            "Alice 90\n"
            "Bob 85\n"
            "Carol 92\n\n"
            "示例输出：\n"
            "Carol 92\n"
            "89.0"
        ),
        "language": "python",
        "difficulty": "medium",
        "tags": "案例检测,学生成绩分析,列表,循环,max,格式化",
        "starter_code": (
            "# 输入第一行为学生人数 n，接下来 n 行每行是 姓名 成绩\n"
            "# 输出最高分学生的姓名和成绩，以及平均分（保留 1 位小数）\n"
        ),
        "test_cases": [
            {
                "input": "3\nAlice 90\nBob 85\nCarol 92",
                "expected_output": "Carol 92\n89.0",
            },
            {
                "input": "2\nTom 70\nAmy 70",
                "expected_output": "Tom 70\n70.0",
            },
            {
                "input": "1\nLily 100",
                "expected_output": "Lily 100\n100.0",
            },
        ],
    },
    {
        "title": "案例：文本词频统计",
        "description": (
            "输入一行英文文本，单词之间用空格分隔。请把所有单词转为小写，"
            "统计每个单词出现的次数，并按字母顺序每行输出一个单词："
            "格式为 word:count。\n\n"
            "示例输入：\n"
            "the quick brown fox the quick\n\n"
            "示例输出：\n"
            "brown:1\n"
            "fox:1\n"
            "quick:2\n"
            "the:2"
        ),
        "language": "python",
        "difficulty": "medium",
        "tags": "案例检测,文本词频统计,字符串,字典,排序",
        "starter_code": (
            "# 输入一行英文文本，单词之间用空格分隔\n"
            "# 统计每个单词出现次数，并按字母顺序输出 word:count\n"
        ),
        "test_cases": [
            {
                "input": "the quick brown fox the quick",
                "expected_output": "brown:1\nfox:1\nquick:2\nthe:2",
            },
            {
                "input": "hello world hello",
                "expected_output": "hello:2\nworld:1",
            },
            {
                "input": "python python python",
                "expected_output": "python:3",
            },
        ],
    },
    {
        "title": "案例：商品库存管理",
        "description": (
            "输入第一行为商品数量 n，接下来 n 行每行包含商品名、库存量和单价，"
            "字段之间用空格分隔。输出两行：第一行为所有商品库存总价值"
            "（库存量乘单价之和，输出整数），第二行为库存量低于 10 的商品名，"
            "按输入顺序用空格分隔；如果没有低库存商品则输出 none。\n\n"
            "示例输入：\n"
            "3\n"
            "apple 5 2\n"
            "banana 20 3\n"
            "cherry 8 10\n\n"
            "示例输出：\n"
            "150\n"
            "apple cherry"
        ),
        "language": "python",
        "difficulty": "medium",
        "tags": "案例检测,商品库存管理,列表,循环,条件判断",
        "starter_code": (
            "# 输入第一行为商品数量 n，接下来 n 行每行是 商品名 库存量 单价\n"
            "# 输出库存总价值，以及库存量低于 10 的商品名（没有则输出 none）\n"
        ),
        "test_cases": [
            {
                "input": "3\napple 5 2\nbanana 20 3\ncherry 8 10",
                "expected_output": "150\napple cherry",
            },
            {
                "input": "2\npen 10 2\nbook 30 5",
                "expected_output": "170\nnone",
            },
            {
                "input": "1\nwater 100 1",
                "expected_output": "100\nnone",
            },
        ],
    },
]
