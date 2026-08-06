import base64
from types import SimpleNamespace

from app.services import executor


def test_docker_command_encodes_code_and_enables_sandbox_limits():
    code = "print(1 + 1)"
    command = executor._docker_command(code)

    assert command[:12] == [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
    ]
    assert "--cap-drop" in command
    assert "ALL" in command
    assert "--security-opt" in command
    assert "no-new-privileges" in command

    encoded = next(value.split("=", 1)[1] for value in command if value.startswith("CODE_B64="))
    assert base64.b64decode(encoded).decode() == code


def test_run_python_code_docker_accepts_output(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3 4", expected_output="7", is_sample=True),
        SimpleNamespace(id=2, input="10 -2", expected_output="8", is_sample=True),
    ]

    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "docker"
        return SimpleNamespace(returncode=0, stdout=input.strip() == "3 4" and "7\n" or "8\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.run_python_code_docker(
        "a, b = map(int, input().split())\nprint(a + b)",
        cases,
        timeout=5,
    )

    assert result.status == "accepted"
    assert [item.passed for item in result.results] == [True, True]


def test_run_custom_python_docker_success(monkeypatch):
    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        return SimpleNamespace(returncode=0, stdout="hello\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.run_custom_python_docker("print(input())", "hello", timeout=5)

    assert result.status == "success"
    assert result.results[0].actual_output.strip() == "hello"


def test_node_docker_command_encodes_code_and_sandbox_limits():
    code = "console.log('hi')"
    command = executor._node_docker_command(code)

    assert command[:12] == [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
    ]
    assert "--cap-drop" in command
    assert "ALL" in command
    assert "--security-opt" in command
    assert "no-new-privileges" in command

    encoded = next(value.split("=", 1)[1] for value in command if value.startswith("CODE_B64="))
    assert base64.b64decode(encoded).decode() == code


def test_run_javascript_code_docker_accepts_output(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3 4", expected_output="7", is_sample=True),
        SimpleNamespace(id=2, input="10 -2", expected_output="8", is_sample=True),
    ]

    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "docker"
        return SimpleNamespace(
            returncode=0,
            stdout=input.strip() == "3 4" and "7\n" or "8\n",
            stderr="",
        )

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.run_javascript_code_docker(
        "const fs = require('fs');\n"
        "const [a, b] = fs.readFileSync(0, 'utf8').trim().split(' ').map(Number);\n"
        "console.log(a + b);\n",
        cases,
        timeout=5,
    )

    assert result.status == "accepted"
    assert [item.passed for item in result.results] == [True, True]


def test_execute_code_routes_javascript(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3", expected_output="odd", is_sample=True),
    ]

    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "node"
        return SimpleNamespace(returncode=0, stdout="odd\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_code("console.log('odd')", "javascript", cases)

    assert result.status == "accepted"
    assert result.results[0].passed is True


def test_execute_custom_routes_javascript(monkeypatch):
    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "node"
        return SimpleNamespace(returncode=0, stdout="hello\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_custom("console.log(input())", "javascript", "hello")

    assert result.status == "success"
    assert result.results[0].actual_output.strip() == "hello"


def test_java_docker_command_encodes_code_and_sandbox_limits():
    code = "public class Main { public static void main(String[] args) { } }"
    command = executor._java_docker_command(code)

    assert command[:12] == [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
    ]
    assert "--cap-drop" in command
    assert "ALL" in command
    assert "--security-opt" in command
    assert "no-new-privileges" in command
    assert "-w" in command
    assert "/tmp" in command

    encoded = next(value.split("=", 1)[1] for value in command if value.startswith("CODE_B64="))
    assert base64.b64decode(encoded).decode() == code


def test_run_java_code_docker_accepts_output(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3 4", expected_output="7", is_sample=True),
        SimpleNamespace(id=2, input="10 -2", expected_output="8", is_sample=True),
    ]

    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "docker"
        return SimpleNamespace(
            returncode=0,
            stdout=input.strip() == "3 4" and "7\n" or "8\n",
            stderr="",
        )

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.run_java_code_docker(
        "import java.util.Scanner;\n"
        "public class Main {\n"
        "    public static void main(String[] args) {\n"
        "        Scanner sc = new Scanner(System.in);\n"
        "        System.out.println(sc.nextInt() + sc.nextInt());\n"
        "    }\n"
        "}\n",
        cases,
        timeout=5,
    )

    assert result.status == "accepted"
    assert [item.passed for item in result.results] == [True, True]


def test_execute_code_routes_java(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3", expected_output="odd", is_sample=True),
    ]

    def fake_run(command, input=None, capture_output=False, text=False, timeout=5, cwd="", env=None):
        if command[0] == "javac":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        assert command[0] == "java"
        return SimpleNamespace(returncode=0, stdout="odd\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_code("public class Main {}", "java", cases)

    assert result.status == "accepted"
    assert result.results[0].passed is True


def test_execute_custom_routes_java(monkeypatch):
    def fake_run(command, input=None, capture_output=False, text=False, timeout=5, cwd="", env=None):
        if command[0] == "javac":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        assert command[0] == "java"
        return SimpleNamespace(returncode=0, stdout="hello\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_custom("public class Main {}", "java", "hello")

    assert result.status == "success"
    assert result.results[0].actual_output.strip() == "hello"


def test_cpp_docker_command_encodes_code_and_sandbox_limits():
    code = "#include <iostream>\nint main(){ std::cout << 7; }\n"
    command = executor._cpp_docker_command(code)

    assert command[:12] == [
        "docker",
        "run",
        "--rm",
        "-i",
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "1",
        "--pids-limit",
        "64",
    ]
    assert "--cap-drop" in command
    assert "ALL" in command
    assert "--security-opt" in command
    assert "no-new-privileges" in command
    assert "-w" in command
    assert "/tmp" in command
    assert "g++ -std=c++17 -O2 -o solution solution.cpp" in command[-1]

    encoded = next(value.split("=", 1)[1] for value in command if value.startswith("CODE_B64="))
    assert base64.b64decode(encoded).decode() == code


def test_run_cpp_code_docker_accepts_output(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3 4", expected_output="7", is_sample=True),
        SimpleNamespace(id=2, input="10 -2", expected_output="8", is_sample=True),
    ]

    def fake_run(command, input, capture_output, text, timeout, cwd, env):
        assert command[0] == "docker"
        return SimpleNamespace(
            returncode=0,
            stdout=input.strip() == "3 4" and "7\n" or "8\n",
            stderr="",
        )

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.run_cpp_code_docker(
        "#include <iostream>\nint main(){ int a,b; std::cin>>a>>b; std::cout<<a+b; }\n",
        cases,
        timeout=5,
    )

    assert result.status == "accepted"
    assert [item.passed for item in result.results] == [True, True]


def test_execute_code_routes_cpp(monkeypatch):
    cases = [
        SimpleNamespace(id=1, input="3", expected_output="odd", is_sample=True),
    ]

    def fake_run(command, input=None, capture_output=False, text=False, timeout=5, cwd="", env=None):
        if command[0] == "g++":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=0, stdout="odd\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_code("#include <iostream>", "cpp", cases)

    assert result.status == "accepted"
    assert result.results[0].passed is True


def test_execute_custom_routes_cpp(monkeypatch):
    def fake_run(command, input=None, capture_output=False, text=False, timeout=5, cwd="", env=None):
        if command[0] == "g++":
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        return SimpleNamespace(returncode=0, stdout="hello\n", stderr="")

    monkeypatch.setattr(executor.subprocess, "run", fake_run)
    result = executor.execute_custom("#include <iostream>", "cpp", "hello")

    assert result.status == "success"
    assert result.results[0].actual_output.strip() == "hello"
