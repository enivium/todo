# task_list.py
# Represents a list of tasks

import task

class Task_List:

    def __init__(self):
        self.tasks = []
        for i in range(100):
            self.tasks.append(task.Task('task ' + str(i)))

    def get_tasks(self, day):
        return self.tasks

    def add_task(task_name, task_date, task_recurr, task_recurr_from_due, task_priority):
        print(task_name)
        print('\n')
        print(task_date)
        print('\n')
        print(task_recurr)
        print('\n')
        print(task_recurr_from_due)
        print('\n')
        print(task_priority)
        print('\n')
