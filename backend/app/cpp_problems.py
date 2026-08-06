CPP_PROBLEMS = [
    {
        "title": "C++ 两数之和",
        "description": (
            "输入一行两个整数 a 和 b，用空格分隔，输出它们的和。\n\n"
            "示例输入：\n3 4\n\n示例输出：\n7"
        ),
        "language": "cpp",
        "difficulty": "easy",
        "tags": "C++,入门,运算",
        "starter_code": (
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    int a, b;\n"
            "    std::cin >> a >> b;\n"
            "    std::cout << a + b << std::endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "3 4", "expected_output": "7"},
            {"input": "10 -2", "expected_output": "8"},
            {"input": "0 0", "expected_output": "0"},
        ],
    },
    {
        "title": "C++ 判断奇偶",
        "description": "输入一个整数 n，如果是奇数输出 odd，偶数输出 even。",
        "language": "cpp",
        "difficulty": "easy",
        "tags": "C++,条件判断,取余",
        "starter_code": (
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    int n;\n"
            "    std::cin >> n;\n"
            "    std::cout << (n % 2 == 0 ? \"even\" : \"odd\") << std::endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "3", "expected_output": "odd"},
            {"input": "4", "expected_output": "even"},
            {"input": "0", "expected_output": "even"},
        ],
    },
    {
        "title": "C++ 字符串反转",
        "description": "输入一个字符串，输出它的反转结果。",
        "language": "cpp",
        "difficulty": "easy",
        "tags": "C++,字符串,反转",
        "starter_code": (
            "#include <algorithm>\n"
            "#include <iostream>\n"
            "#include <string>\n"
            "\n"
            "int main() {\n"
            "    std::string input;\n"
            "    std::cin >> input;\n"
            "    std::reverse(input.begin(), input.end());\n"
            "    std::cout << input << std::endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "abc", "expected_output": "cba"},
            {"input": "hello", "expected_output": "olleh"},
            {"input": "Cpp", "expected_output": "ppC"},
        ],
    },
    {
        "title": "C++ 数组求和",
        "description": "输入一行整数，用空格分隔，输出这些整数的和。",
        "language": "cpp",
        "difficulty": "easy",
        "tags": "C++,数组,循环",
        "starter_code": (
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    int sum = 0;\n"
            "    int value;\n"
            "    while (std::cin >> value) {\n"
            "        sum += value;\n"
            "    }\n"
            "    std::cout << sum << std::endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "1 2 3 4", "expected_output": "10"},
            {"input": "10 -2 8", "expected_output": "16"},
            {"input": "0", "expected_output": "0"},
        ],
    },
    {
        "title": "C++ 欢迎输出",
        "description": "不读取输入，直接输出 Hello C++。",
        "language": "cpp",
        "difficulty": "easy",
        "tags": "C++,入门,输出",
        "starter_code": (
            "#include <iostream>\n"
            "\n"
            "int main() {\n"
            "    std::cout << \"Hello C++\" << std::endl;\n"
            "    return 0;\n"
            "}\n"
        ),
        "test_cases": [
            {"input": "", "expected_output": "Hello C++"},
        ],
    },
]
