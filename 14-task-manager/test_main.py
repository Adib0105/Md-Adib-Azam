import unittest

from main import add_task, complete_task, delete_task


class TaskTests(unittest.TestCase):
    def test_lifecycle(self):
        tasks = []
        task = add_task(tasks, "Learn testing")
        self.assertTrue(complete_task(tasks, task["id"]))
        self.assertTrue(tasks[0]["done"])
        self.assertEqual(delete_task(tasks, task["id"]), [])


if __name__ == "__main__":
    unittest.main()
