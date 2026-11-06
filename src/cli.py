"""Command line front end for the todo list."""

from __future__ import annotations

import argparse
import sys

from todo import TodoList


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="A tiny task list.")
    p.add_argument("--file", default=None, help="path to the task file")

    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add a task")
    a.add_argument("title")
    a.add_argument("-t", "--tag", action="append", default=[], dest="tags")

    d = sub.add_parser("done", help="mark a task complete")
    d.add_argument("id", type=int)

    r = sub.add_parser("rm", help="remove a task")
    r.add_argument("id", type=int)

    sub.add_parser("ls", help="list tasks")
    sub.add_parser("stats", help="show task statistics")
    sub.add_parser("clear", help="remove completed tasks")

    s = sub.add_parser("search", help="find tasks by title")
    s.add_argument("term")

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    todo = TodoList(args.file) if args.file else TodoList()

    if args.command == "add":
        task = todo.add(args.title, args.tags)
        print(f"added {task.id}: {task.title}")
    elif args.command == "done":
        print("completed" if todo.complete(args.id) else f"no task {args.id}")
    elif args.command == "rm":
        print("removed" if todo.remove(args.id) else f"no task {args.id}")
    elif args.command == "ls":
        print(todo.render())
    elif args.command == "stats":
        s = todo.stats()
        print(f"{s['done']}/{s['total']} done ({s['percent']}%), {s['open']} open")
    elif args.command == "clear":
        print(f"cleared {todo.clear_done()}")
    elif args.command == "search":
        found = todo.search(args.term)
        print("\n".join(t.label() for t in found) if found else "no match")
    else:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
