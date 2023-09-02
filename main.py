import signal

from code_tasks import perform_task
from utils.io import user_input
from utils import logging


signal.signal(signal.SIGINT, logging.interrupt_dump)
signal.signal(signal.SIGTERM, logging.interrupt_dump)


if __name__ == "__main__":
    try:
        task = user_input("Type a google search: ")
        perform_task(task)

        print()
        feedback = user_input("Were the results useful (y/n)? ")
        logging.log(feedback=feedback != "n")
    except:
        pass
    finally:
        logging.dump(name="query")
