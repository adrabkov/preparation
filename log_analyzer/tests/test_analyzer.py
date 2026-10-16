from analyzer import parse_log_line, read_log_file, calc_log_lines
import pytest
import os
from pathlib import Path

LOG1 = """2024-08-08 12:34:56 INFO Started
2024-08-08 12:35:00 ERROR Failed
2024-08-08 12:36:00 INFO Finished"""

LOG2 = """2024-08-08 13:00:00 WARNING Slow response
2024-08-08 13:01:00 ERROR Database failed"""

def test_parse_log_line():
    line = "2024-08-08 12:34:56 ERROR Database failed"

    out = parse_log_line(line)

    assert out["timestamp"] == "2024-08-08 12:34:56"
    assert out["level"] == "ERROR"
    assert out["message"] == "Database failed"

def test_parse_invalid_line():
    line = "broken line"

    result = parse_log_line(line)

    assert result is None

def test_parse_invalid_level():
    line = "2024-08-08 12:34:56 DEBUG Something happened"

    out = parse_log_line(line)

    assert out is None

@pytest.mark.parametrize(
    "line", [
    "broken line",
    "",
    "2024-08-08 12:34:56 DEBUG Something happened",
    "2024-08-08 INFO",
    ]
)
def test_parse_invalid_line(line):
    out = parse_log_line(line)
    assert out is None

@pytest.mark.parametrize("line, expected_level",[
    ("2024-08-08 12:34:56 INFO Started", "INFO"),
    ("2024-08-08 12:34:56 WARNING Slow response", "WARNING"),
    ("2024-08-08 12:34:56 ERROR Failed", "ERROR"),
])
def test_parse_level(line, expected_level):
    out = parse_log_line(line)
    assert out["level"] == expected_level

@pytest.fixture
def valid_log_line():
    return "2024-08-08 12:34:56 ERROR Database failed"

def test_parse_error_level(valid_log_line):
    result = parse_log_line(valid_log_line)
    assert result["level"] == "ERROR"

@pytest.fixture
def temp_log_file(tmp_path, valid_log_line):
    file_path = tmp_path / "temp.log"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(valid_log_line)

    yield file_path


@pytest.fixture
def temp_logs_dir(tmp_path):
    files_to_create = {
        "app1.log": LOG1,
        "app2.log": LOG2
    }
    path_dir = tmp_path / "temp_dir"
    path_dir.mkdir()

    for filename, content in files_to_create.items():
        with open(path_dir / filename, "w", encoding="utf-8") as f:
            f.write(content)  

    yield path_dir


def test_fixture(temp_log_file):
    result = read_log_file(temp_log_file)
    assert len(result) == 1

def test_check_log_dir(temp_logs_dir):
    out = calc_log_lines(temp_logs_dir)
    print(out)
