import datetime
import copy

# Define an empty list to store tasks
tasks = []
# Define lists for undo and redo actions
undo_stack = []
redo_stack = []

# Function to add a task to the list
def add_task(task, due_date):
    task_info = {"task": task, "due_date": due_date, "completed": False}
    tasks.append(task_info)
    undo_stack.append(("add", copy.deepcopy(task_info)))  # Store the action for undo
    redo_stack.clear()  # Clear the redo stack when a new action is performed
    print(f"Task '{task}' added successfully with due date {due_date}.")

# Function to remove a task from the list
def remove_task(task_index):
    if 1 <= task_index <= len(tasks):
        removed_task = tasks.pop(task_index - 1)
        removed_task["completed"] = True
        undo_stack.append(("remove", copy.deepcopy(removed_task)))  # Store the action for undo
        redo_stack.clear()  # Clear the redo stack when a new action is performed
        print(f"Task '{removed_task['task']}' removed from the list and marked as completed.")
    else:
        print("Invalid task index. Please enter a valid index.")

# Function to undo the most recent action
def undo_action():
    if undo_stack:
        action, data = undo_stack.pop()
        if action == "add":
            task_index = next((i for i, t in enumerate(tasks) if t["task"] == data["task"]), None)
            if task_index is not None:
                tasks.pop(task_index)
                print(f"Undo: Task '{data['task']}' removed.")
        elif action == "remove":
            tasks.append(data)
            print(f"Undo: Task '{data['task']}' added back.")
        redo_stack.append((action, data))

# Function to redo the most recent undone action
def redo_action():
    if redo_stack:
        action, data = redo_stack.pop()
        if action == "add":
            add_task(data["task"], data["due_date"])
            print(f"Redo: Task '{data['task']}' added.")
        elif action == "remove":
            task_index = next((i for i, t in enumerate(tasks) if t["task"] == data["task"]), None)
            if task_index is not None:
                removed_task = tasks.pop(task_index)
                removed_task["completed"] = True
                print(f"Redo: Task '{removed_task['task']}' removed again.")

# Function to view tasks
def view_tasks(task_filter=None):
    if not tasks:
        print("No tasks found.")
    else:
        print("Tasks:")
        for i, task_info in enumerate(tasks, start=1):
            task = task_info["task"]
            due_date = task_info["due_date"]
            completed = task_info["completed"]
            status = "Completed" if completed else "Pending"
            
            if task_filter is None or (task_filter == "completed" and completed) or (task_filter == "remaining" and not completed):
                print(f"{i}. {task} (Due: {due_date}, Status: {status})")

# Main loop
while True:
    print("\nTo-Do List Manager")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Completed Tasks")
    print("4. View Remaining Tasks")
    print("5. Remove Task")
    print("6. Undo")
    print("7. Redo")
    print("8. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter the task: ")
        due_date = input("Enter the due date (format: YYYY-MM-DD): ")
        try:
            due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
            add_task(task, due_date)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        view_tasks("completed")
    elif choice == "4":
        view_tasks("remaining")
    elif choice == "5":
        if not tasks:
            print("No tasks to remove.")
        else:
            view_tasks()
            task_index = int(input("Enter the index of the task to remove: "))
            remove_task(task_index)
    elif choice == "6":
        undo_action()
    elif choice == "7":
        redo_action()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
