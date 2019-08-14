# user_interface.py
# Handles interactions with the user

import curses
import enum
import datetime

import task_list
import color_enum

class User_Interface:

    def __init__(self):
        # Consants for setting up display
        self.num_reserved_lines = 3
        self.num_menu_options = 8

        # Member objects
        self.task_list = task_list.Task_List()
        self.date = datetime.date.today()
        self.current_date = datetime.date.today()
      
        # Initialize curses screen
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)

        # Initialize task_pad
        self.task_pad_lines = 1000
        self.task_pad_cols = 1000
        self.task_pad_pos = 0
        self.tasks = []
        self.task_pad_size = curses.LINES - self.num_menu_options - self.num_reserved_lines
        self.task_pad = curses.newpad(self.task_pad_lines, self.task_pad_cols)

        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(Color.P1, curses.COLOR_GREEN, -1)
        curses.init_pair(Color.P2, curses.COLOR_CYAN, -1)
        curses.init_pair(Color.P3, curses.COLOR_BLUE, -1)

    def run(self):
        # Main run loop

        # Initialize display
        self.display()

        command = 0
        while (command != ord('q')):
            # Get user input
            command = self.stdscr.getch()
   
            if (command == curses.KEY_DOWN):
                if (self.task_pad_pos < len(self.tasks) - self.task_pad_size):
                    self.task_pad_pos += 1
                    self.display_tasks()
            elif (command == curses.KEY_UP):
                if (self.task_pad_pos > 0):
                    self.task_pad_pos -= 1
                    self.display_tasks()
            elif (command == ord('a')):
                self.stdscr.clear()
                self.add_task()
                self.display()

        # Exit program and return terminal to normal state
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def display(self):
        # Macro for tasks and menu display
        self.display_date()
        self.display_menu() 
        self.update_tasks()
        self.display_tasks()

    def display_date(self):
        # Display the date
        display_date_str = str(self.date.month) + '/' + str(self.date.day) \
                           + '/' + str(self.date.year)
        self.stdscr.addstr(0, 0, display_date_str, curses.A_BOLD)

    def update_tasks(self):
        # Update the tasks list
        self.tasks = self.task_list.get_tasks(self.date)
        self.task_pad.clear()
        for i in range(len(self.tasks)):
            priority = self.tasks[i].get_priority()
            self.task_pad.addstr(i, 0, str(i + 1) + ") " + self.tasks[i].get_name(), \
                                 curses.color_pair(priority))
            if (self.tasks[i].get_date() > current_date):
                self.task_pad.addstr('*')

    def display_tasks(self):
        # Display tasks on the screen
        if (len(self.tasks) <= curses.LINES - self.num_menu_options - self.num_reserved_lines \
            or self.task_pad_pos == len(self.tasks) - self.task_pad_size):
            self.task_pad.refresh(self.task_pad_pos, 0,  2, 0, \
                                  self.task_pad_size + 1, curses.COLS - 1)
        else:
            self.stdscr.move(self.task_pad_size + 1, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(self.task_pad_size + 1, 0, '...')
            self.task_pad.refresh(self.task_pad_pos, 0,  2, 0,  \
                                  self.task_pad_size, curses.COLS - 1)
            
    def display_menu(self):
        # Display menu options 
        self.stdscr.addstr(curses.LINES - self.num_menu_options, 0, '[c]omplete task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 1, 0, '[a]dd task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 2, 0, '[r]eschedule task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 3, 0, '[e]dit task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 4, 0, '[d]elete task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 5, 0, '[s]earch task')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 6, 0, '[v]iew date')
        self.stdscr.addstr(curses.LINES - self.num_menu_options + 7, 0, '[q]uit')
        self.stdscr.refresh()

    def get_input_str(self):
        # Get string input from user
        curses.curs_set(1) 
        curses.echo()
        curses.nocbreak()         

        input = curses.getch()
        while (input != '\n'):
            input_str += chr(input)
            input = curses.getch()

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

        input_str.lower()
        return input_str

    def add_task(self):
        # Collect input from the user to create a new task

        # Variable to control text location
        line_num = 0

        # Get task name
        self.stdscr.addstr(line_num, 0, 'Task Name:')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '> ')
        line_num += 1
        task_name = self.get_input_str()
        if (task_name == 'q'):
            return

        # Get due date
        self.stdscr.addstr(line_num, 0, 'Due Date:')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '> ') 
        line_num += 1
        task_date = self.get_input_str()
        if (task_date == 'q'):
            return

        # Get recurrence
        self.stdscr.addstr(line_num, 0, 'Recurrence:')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '> ')
        line_num += 1
        task_recurr = self.get_input_str()
        if (task_recurr == 'q'):
            return

        # Get when to recurr from
        task_recurr_from_due = false
        if (task_recurr != 'none' and task_recurr != 'n'):
            self.stdscr.addstr(line_num, 0, 'Recurr From:')
            line_num += 1
            self.stdscr.addstr(line_num, 0, '[d]ue date')
            line_num += 1
            self.stdscr.addstr(line_num, 0, '[c]ompletion date')
            line_num += 1
            input = 0
            valid_input = false
            while (!valid_input):
                input = curses.getch()
                if (input == ord('q')):
                    return
                elif (input == ord('d')):
                    valid_input = true
                    task_recurr_from_due = true
                elif (input == ord('c')):
                    valid_input = true

        # Get priority
        self.stdscr.addstr(line_num, 0, 'Priority:')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '[1]')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '[2]')
        line_num += 1
        self.stdscr.addstr(line_num, 0, '[3]')
        input = 0
        valid_input = false
        while (!valid_input):
            input = curses.getch()
            if (input == ord('1')):
                return
            elif (input == ord('1')):
                task_priority = 1
            elif (input == ord('2')):
                task_priority = 2
            elif (input == ord('3')):
                task_priority = 3

        self.task_list.add_task(task_name, task_date, task_recurr, task_recurr_from_due, \
                                task_priority)
