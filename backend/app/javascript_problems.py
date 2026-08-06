JAVASCRIPT_PROBLEMS = [
    {
        "title": "JavaScript 两数之和",
        "description": (
            "输入一行两个整数 a 和 b，用空格分隔，输出它们的和。\n\n"
            "示例输入：\n3 4\n\n示例输出：\n7"
        ),
        "language": "javascript",
        "difficulty": "easy",
        "tags": "JavaScript,入门,运算",
        "starter_code": (
            "const fs = require('fs');\n"
            "const input = fs.readFileSync(0, 'utf8').trim();\n"
            "const [a, b] = input.split(' ').map(Number);\n"
            "console.log(a + b);\n"
        ),
        "test_cases": [
            {"input": "3 4", "expected_output": "7"},
            {"input": "10 -2", "expected_output": "8"},
            {"input": "0 0", "expected_output": "0"},
        ],
    },
    {
        "title": "JavaScript 判断奇偶",
        "description": "输入一个整数 n，如果是奇数输出 odd，偶数输出 even。",
        "language": "javascript",
        "difficulty": "easy",
        "tags": "JavaScript,条件判断,取余",
        "starter_code": (
            "const fs = require('fs');\n"
            "const n = Number(fs.readFileSync(0, 'utf8').trim());\n"
            "console.log(n % 2 === 0 ? 'even' : 'odd');\n"
        ),
        "test_cases": [
            {"input": "3", "expected_output": "odd"},
            {"input": "4", "expected_output": "even"},
            {"input": "0", "expected_output": "even"},
        ],
    },
    {
        "title": "JavaScript 字符串反转",
        "description": "输入一个字符串，输出它的反转结果。",
        "language": "javascript",
        "difficulty": "easy",
        "tags": "JavaScript,字符串,数组",
        "starter_code": (
            "const fs = require('fs');\n"
            "const input = fs.readFileSync(0, 'utf8').trim();\n"
            "console.log(input.split('').reverse().join(''));\n"
        ),
        "test_cases": [
            {"input": "abc", "expected_output": "cba"},
            {"input": "hello", "expected_output": "olleh"},
            {"input": "JavaScript", "expected_output": "tpircSavaJ"},
        ],
    },
    {
        "title": "JavaScript 数组求和",
        "description": "输入一行整数，用空格分隔，输出这些整数的和。",
        "language": "javascript",
        "difficulty": "easy",
        "tags": "JavaScript,数组,reduce",
        "starter_code": (
            "const fs = require('fs');\n"
            "const input = fs.readFileSync(0, 'utf8').trim();\n"
            "const nums = input.split(/\\s+/).map(Number);\n"
            "console.log(nums.reduce((sum, n) => sum + n, 0));\n"
        ),
        "test_cases": [
            {"input": "1 2 3 4", "expected_output": "10"},
            {"input": "10 -2 8", "expected_output": "16"},
            {"input": "0", "expected_output": "0"},
        ],
    },
    {
        "title": "JavaScript 欢迎输出",
        "description": "不读取输入，直接输出 Hello JavaScript。",
        "language": "javascript",
        "difficulty": "easy",
        "tags": "JavaScript,入门,输出",
        "starter_code": "console.log('Hello JavaScript');\n",
        "test_cases": [
            {"input": "", "expected_output": "Hello JavaScript"},
        ],
    },
]
