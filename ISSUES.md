# Known issues

Small, self-contained problems in this project. Each one is meant to be
fixable in a single pull request.

## 1. Task ids collide after a reload

`TodoList._next_id()` returns `len(self.tasks) + 1`, so after removing a task
the next id can repeat one that is still in use:

```python
todo.add("a")        # id 1
todo.add("b")        # id 2
todo.remove(1)
todo.add("c")        # id 2 again — collides with "b"
```

Ids should be stable and never reused for the lifetime of the file. See
`tests/test_todo.py::test_ids_unique_after_reload`.

## 3. `render()` sorts completed tasks unpredictably

`sorted(self.tasks, key=lambda t: t.done)` only partitions done from not-done;
within each group the order depends on insertion. Sorting should be stable and
by id, so output does not shuffle between runs.

## 4. No `--json` output

The CLI only prints human-readable text. Scripts need machine-readable output:
add a `--json` flag that prints the task list as JSON.
