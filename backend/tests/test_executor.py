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
