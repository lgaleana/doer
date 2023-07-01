from code_tasks import perform_task
from utils.io import user_input


if __name__ == "__main__":
    task = user_input("What information are you looking for? ")
    perform_task(task)
