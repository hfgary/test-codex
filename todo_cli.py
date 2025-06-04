import argparse
import json
import os
from datetime import datetime

TODO_FILE = 'todo.json'


def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


def add_task(description):
    tasks = load_tasks()
    task_id = tasks[-1]['id'] + 1 if tasks else 1
    tasks.append({
        'id': task_id,
        'description': description,
        'completed': False,
        'created_at': datetime.now().isoformat(),
    })
    save_tasks(tasks)
    print(f"Added task {task_id}: {description}")


def list_tasks(show_all=False):
    tasks = load_tasks()
    for task in tasks:
        if not show_all and task['completed']:
            continue
        status = '✓' if task['completed'] else ' '
        created_at = task.get('created_at')
        if created_at:
            print(f"[{status}] {task['id']}: {task['description']} ({created_at})")
        else:
            print(f"[{status}] {task['id']}: {task['description']}")


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            save_tasks(tasks)
            print(f"Completed task {task_id}")
            return
    print(f"Task {task_id} not found")


def remove_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t['id'] != task_id]
    if len(updated_tasks) == len(tasks):
        print(f"Task {task_id} not found")
        return
    save_tasks(updated_tasks)
    print(f"Removed task {task_id}")


def parse_args():
    parser = argparse.ArgumentParser(description='Simple TODO list CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_p = subparsers.add_parser('add', help='Add a new task')
    add_p.add_argument('description', nargs='+', help='Task description')

    list_p = subparsers.add_parser('list', help='List tasks')
    list_p.add_argument('-a', '--all', action='store_true', help='Show completed tasks')

    complete_p = subparsers.add_parser('complete', help='Mark task as completed')
    complete_p.add_argument('id', type=int, help='Task ID')

    remove_p = subparsers.add_parser('remove', help='Remove task')
    remove_p.add_argument('id', type=int, help='Task ID')

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == 'add':
        add_task(' '.join(args.description))
    elif args.command == 'list':
        list_tasks(show_all=args.all)
    elif args.command == 'complete':
        complete_task(args.id)
    elif args.command == 'remove':
        remove_task(args.id)
    else:
        print('No command specified. Use -h for help.')


if __name__ == '__main__':
    main()
