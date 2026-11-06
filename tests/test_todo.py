"""Tests for the todo list. Run with: python3 -m pytest tests/ -v"""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from todo import TodoList  # noqa: E402


@pytest.fixture
def todo():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.unlink(path)
    yield TodoList(path)
    if os.path.exists(path):
        os.unlink(path)


def test_add_assigns_ids(todo):
    a = todo.add("first")
    b = todo.add("second")
    assert a.id == 1
    assert b.id == 2


def test_add_persists(todo):
    todo.add("persisted")
    reloaded = TodoList(todo.path)
    assert [t.title for t in reloaded.tasks] == ["persisted"]


def test_complete(todo):
    task = todo.add("finish me")
    assert todo.complete(task.id) is True
    assert todo.get(task.id).done is True


def test_complete_missing_returns_false(todo):
    assert todo.complete(999) is False


def test_remove(todo):
    task = todo.add("remove me")
    assert todo.remove(task.id) is True
    assert todo.get(task.id) is None


def test_clear_done(todo):
    a = todo.add("a")
    todo.add("b")
    todo.complete(a.id)
    assert todo.clear_done() == 1
    assert len(todo.tasks) == 1


def test_search_is_case_insensitive(todo):
    todo.add("Buy Milk")
    assert len(todo.search("milk")) == 1


def test_stats_on_empty_list(todo):
    assert todo.stats()["percent"] == 0.0


def test_stats_percent_with_tasks(todo):
    first = todo.add("first")
    todo.add("second")
    todo.complete(first.id)
    stats = todo.stats()
    assert stats["total"] == 2
    assert stats["done"] == 1
    assert stats["open"] == 1
    assert stats["percent"] == 50.0


def test_ids_unique_after_reload(todo):
    # Expected to fail: see ISSUES.md #1
    # Removing a task then adding one reuses a live id.
    todo.add("first")
    todo.add("second")
    todo.remove(1)
    reloaded = TodoList(todo.path)
    third = reloaded.add("third")
    live_ids = [t.id for t in reloaded.tasks if t.title != "third"]
    assert third.id not in live_ids


def test_tags_round_trip(todo):
    todo.add("tagged", ["work", "urgent"])
    reloaded = TodoList(todo.path)
    assert reloaded.tasks[0].tags == ["work", "urgent"]
