import time
import threading


class IO:
    def __init__(self, print_delay=0.05):
        self.print_delay = print_delay

    def type_print(self, message, delay=None):
        """Print a message with a delay between each character."""
        if delay is None:
            delay = self.print_delay
        for character in message:
            print(character, end="", flush=True)
            time.sleep(delay)
        print()

    def delayed_action(self, func, delay=2, *args, **kwargs):
        """Execute a function after a delay in a separated thread."""

        def action():
            time.sleep(delay)
            func(*args, **kwargs)

        thread = threading.Thread(target=action)
        thread.start()
        return thread
