import cmd
import threading
import time

class MyCmd(cmd.Cmd):
    prompt = "> "

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_hello(self, inp):
        print(f"Hello, {inp}")

# Function to print messages asynchronously
def print_messages():
    while True:
        print("Printing message...")
        time.sleep(5)  # Adjust the time interval as needed

# Create and start the message printing thread
thread = threading.Thread(target=print_messages, daemon=True)
thread.start()

# Run the command loop
MyCmd().cmdloop()
