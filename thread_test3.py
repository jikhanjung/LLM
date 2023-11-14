import cmd
import threading
import time
import sys

class MyCmd(cmd.Cmd):
    prompt = "> "
    message = ""
    message_lock = threading.Lock()

    def precmd(self, line):
        with self.message_lock:
            if self.message:
                self.print_above_prompt(self.message)
                self.message = ""  # Optionally clear the message after displaying
        return line

    def do_exit(self, inp):
        print("Bye")
        return True

    def do_hello(self, inp):
        print(f"Hello, {inp}")

    def print_above_prompt(self, message):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line
        print(message)
        sys.stdout.write("\033[E")  # Move cursor back down one line

def update_message(cmd_instance):
    while True:
        with cmd_instance.message_lock:
            cmd_instance.message = "Updated message at: " + time.strftime("%H:%M:%S")
        time.sleep(5)

cmd_instance = MyCmd()
thread = threading.Thread(target=update_message, args=(cmd_instance,), daemon=True)
thread.start()

cmd_instance.cmdloop()
