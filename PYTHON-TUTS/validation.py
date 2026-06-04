from datetime import datetime


def validate_task_title(title):
    if isinstance(title, str) and len(title.strip()) > 0:
        return True
    return False


def validate_task_description(description):
    if isinstance(description, str) and len(description.strip()) > 0:
        return True
    return False


def validate_due_date(due_date):
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
