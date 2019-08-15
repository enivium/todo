# task.py
# An object to represent tasks for the list

import datetime

class Task:

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_priority(self):
        return 1

    def get_date(self):
        return datetime.date.today()
