"""A tiny task list, stored as JSON on disk.

This is a deliberately small example project used as a sandbox for
dsh-superagent. Some behaviours are intentionally left broken; see ISSUES.md.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from typing import Iterable

DEFAULT_PATH = os.path.join(os.path.expanduser("~"), ".todo.json")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)

    def label(self) -> str:
        mark = "x" if self.done else " "
        tags = ("  #" + " #".join(self.tags)) if self.tags else ""
        return f"[{mark}] {self.id}. {self.title}{tags}"


class TodoList:
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.tasks: list[Task] = []
        self.load()

    # ---------------------------------------------------------------- storage

    def load(self) -> None:
        if not os.path.exists(self.path):
            self.tasks = []
            return
        with open(self.path) as fh:
            raw = json.load(fh)
        self.tasks = [Task(**item) for item in raw]

    def save(self) -> None:
        with open(self.path, "w") as fh:
            json.dump([asdict(t) for t in self.tasks], fh, indent=2)

    # ------------------------------------------------------------------ query

    def _next_id(self) -> int:
        # BUG: starts at 1 every time, so ids collide after a reload.
        return len(self.tasks) + 1

    def get(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def search(self, term: str) -> list[Task]:
        term = term.lower()
        return [t for t in self.tasks if term in t.title.lower()]

    # ----------------------------------------------------------------- mutate

    def add(self, title: str, tags: Iterable[str] = ()) -> Task:
        task = Task(id=self._next_id(), title=title, tags=list(tags))
        self.tasks.append(task)
        self.save()
        return task

    def complete(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        task.done = True
        self.save()
        return True

    def remove(self, task_id: int) -> bool:
        task = self.get(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        self.save()
        return True

    def clear_done(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        self.save()
        return before - len(self.tasks)

    # ------------------------------------------------------------------ stats

    def stats(self) -> dict:
        done = sum(1 for t in self.tasks if t.done)
        # BUG: divides by len(self.tasks) without guarding the empty case.
        return {
            "total": len(self.tasks),
            "done": done,
            "open": len(self.tasks) - done,
            "percent": round(done / len(self.tasks) * 100, 1),
        }

    def render(self) -> str:
        if not self.tasks:
            return "(nothing to do)"
        lines = [t.label() for t in sorted(self.tasks, key=lambda t: t.done)]
        s = self.stats()
        lines.append("")
        lines.append(f"{s['done']}/{s['total']} done ({s['percent']}%)")
        return "\n".join(lines)
