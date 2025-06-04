import os
import json
import subprocess
import sys
import unittest

TODO_FILE = 'todo.json'

class TodoCLITest(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TODO_FILE):
            os.remove(TODO_FILE)

    def tearDown(self):
        if os.path.exists(TODO_FILE):
            os.remove(TODO_FILE)

    def run_cli(self, *args):
        cmd = [sys.executable, 'todo_cli.py'] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()

    def test_add_and_list(self):
        self.run_cli('add', 'Test Task')
        output = self.run_cli('list')
        self.assertIn('Test Task', output)

    def test_complete(self):
        self.run_cli('add', 'Task')
        self.run_cli('complete', '1')
        with open(TODO_FILE) as f:
            tasks = json.load(f)
        self.assertTrue(tasks[0]['completed'])

    def test_remove(self):
        self.run_cli('add', 'Task')
        self.run_cli('remove', '1')
        output = self.run_cli('list')
        self.assertEqual('', output)

    def test_timestamp_added(self):
        self.run_cli('add', 'Timed Task')
        with open(TODO_FILE) as f:
            tasks = json.load(f)
        self.assertIn('created_at', tasks[0])
        # Validate ISO format
        from datetime import datetime
        datetime.fromisoformat(tasks[0]['created_at'])

if __name__ == '__main__':
    unittest.main()
