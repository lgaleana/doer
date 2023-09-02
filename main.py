from code_tasks import perform_task
from utils.io import user_input


if __name__ == "__main__":
    task = user_input("Type a google search: ")
    perform_task(task)
