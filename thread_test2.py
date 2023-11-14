import cmd
import sys

class MyCmd(cmd.Cmd):
    prompt = "> "

    def preloop(self):
        self.print_above_prompt("Initial Message")

    def precmd(self, line):
        self.print_above_prompt("Message before each command")
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

# Run the command loop
MyCmd().cmdloop()
