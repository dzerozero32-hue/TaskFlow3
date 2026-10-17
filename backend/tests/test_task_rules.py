import pytest
from app.task_rules import TaskRuleError, check_stored_task, validate_title

def code(value):
    with pytest.raises(TaskRuleError) as exc: validate_title(value)
    return exc.value.code

def test_title_rules():
    assert code("") == "title_empty"
    assert code("   ") == "title_empty"
    assert validate_title("\t\n Купить хлеб \n") == "Купить хлеб"
    assert validate_title("Купить   хлеб") == "Купить   хлеб"
    assert code("a" * 201) == "title_too_long"
    assert validate_title("👍" * 200) == "👍" * 200
    assert code(None) == "title_invalid"

def test_stored_task_rules():
    check_stored_task(1, "Задача", False)
    with pytest.raises(TaskRuleError) as exc: check_stored_task(1, " ", False)
    assert exc.value.code == "record_invalid"
