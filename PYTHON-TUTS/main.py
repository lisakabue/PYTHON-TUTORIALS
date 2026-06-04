from task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)


def main():
    tasks = []

    while True:
        print("\nTask Management System")
        print("1. Add Task")
        print("2. Mark Task as Complete")
        print("3. View Pending Tasks")
        print("4. View Progress")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")

            if add_task(tasks, title, description, due_date):
                print("Task added successfully.")
            else:
                print("Invalid input. Task not added.")

        elif choice == "2":
            for index, task in enumerate(tasks):
                status = "Completed" if task["completed"] else "Pending"
                print(f"{index}. {task['title']} - {status}")

            try:
                task_index = int(input("Enter task number to mark complete: "))
                if mark_task_as_complete(tasks, task_index):
                    print("Task marked as complete.")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            pending_tasks = view_pending_tasks(tasks)
            if not pending_tasks:
                print("No pending tasks.")
            else:
                for task in pending_tasks:
                    print(f"- {task['title']} (Due: {task['due_date']})")

        elif choice == "4":
            progress = calculate_progress(tasks)
            print(f"Progress: {progress:.2f}%")

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
