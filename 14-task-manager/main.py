import argparse
import json
from pathlib import Path


def load_tasks(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save_tasks(path: Path, tasks: list[dict]) -> None:
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(tasks: list[dict], title: str) -> dict:
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title.strip(), "done": False}
    tasks.append(task)
    return task


def complete_task(tasks: list[dict], task_id: int) -> bool:
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def delete_task(tasks: list[dict], task_id: int) -> list[dict]:
    return [task for task in tasks if task["id"] != task_id]


def main() -> None:
    parser = argparse.ArgumentParser(description="Persistent task manager")
    parser.add_argument("--file", type=Path, default=Path("tasks.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    commands.add_parser("list")
    complete = commands.add_parser("complete")
    complete.add_argument("id", type=int)
    delete = commands.add_parser("delete")
    delete.add_argument("id", type=int)
    args = parser.parse_args()
    tasks = load_tasks(args.file)

    if args.command == "add":
        task = add_task(tasks, args.title)
        save_tasks(args.file, tasks)
        print(f"Added task #{task['id']}")
    elif args.command == "complete":
        print("Task completed." if complete_task(tasks, args.id) else "Task not found.")
        save_tasks(args.file, tasks)
    elif args.command == "delete":
        save_tasks(args.file, delete_task(tasks, args.id))
        print("Task deleted if it existed.")
    else:
        for task in tasks:
            print(f"[{'x' if task['done'] else ' '}] {task['id']}: {task['title']}")


if __name__ == "__main__":
    main()
