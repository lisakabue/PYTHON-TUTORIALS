from validation import (
    validate_task_title,
    validate_task_description,
    validate_due_date
)


def add_task(tasks, title, description, due_date):
    if (
        validate_task_title(title)
        and validate_task_description(description)
        and validate_due_date(due_date)
    ):
        task = {
            "title": title.strip(),
            "description": description.strip(),
            "due_date": due_date,
            "completed": False
        }
        tasks.append(task)
        return True
    return False


def mark_task_as_complete(tasks, task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        return True
    return False


def view_pending_tasks(tasks):
    pending = []
    for task in tasks:
        if not task["completed"]:
            pending.append(task)
    return pending


def calculate_progress(tasks):
    if len(tasks) == 0:
        return 0

    completed_count = 0
    for task in tasks:
        if task["completed"]:
            completed_count += 1

    return (completed_count / len(tasks)) * 100
