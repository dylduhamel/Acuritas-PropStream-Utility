import cmd2
import argparse
import sys

class CSVToDatabaseApp(cmd2.Cmd):
    def __init__(self, number):
        super().__init__()
        self.number = int(number)
        self.location = ""
        self.prompt = '(CSVToDatabase) '
        self.display_splash()

    def display_splash(self):
        """Display splash screen with basic instructions."""
        splash_text = """
        

   ___                      ____  __                                 ___      __                                 __
  / _ \  ____ ___    ___   / __/ / /_  ____ ___  ___ _  __ _        / _ | ___/ / _  __ ___ _  ___  ____ ___  ___/ /
 / ___/ / __// _ \  / _ \ _\ \  / __/ / __// -_)/ _ `/ /  ' \      / __ |/ _  / | |/ // _ `/ / _ \/ __// -_)/ _  / 
/_/    /_/   \___/ / .__//___/  \__/ /_/   \__/ \_,_/ /_/_/_/     /_/ |_|\_,_/  |___/ \_,_/ /_//_/\__/ \__/ \_,_/  
                  /_/                                                                                              


        
        Welcome to the PropStream Advanced command line interface!
        
        Available commands:
          - add_csv: Increments the current number.
          - set_to_zero: Resets the number to zero.
          - print: Displays the current number.

        Type 'help' or '?' for more details on commands.
        """
        self.poutput(splash_text)

    @cmd2.with_default_category("File Management")
    def do_set_file_path(self, args):
        """Set the file path for location."""
        parser = cmd2.Cmd2ArgumentParser()
        parser.add_argument('file_path', nargs=argparse.REMAINDER, type=str, help="The file path to set as the location.")

        parsed_args = parser.parse_args(args)

        # Join the characters back together into a single string
        file_path = ''.join(parsed_args.file_path)

        self.location = file_path
        self.poutput(f"File path set to: [{self.location}]")


    @cmd2.with_argparser(cmd2.Cmd2ArgumentParser())
    def do_increment(self, _):
        """Increment the number."""
        self.number += 1
        self.poutput(self.number)

    @cmd2.with_default_category("Data Manipulation")
    def do_set_value(self, args):
        """Set the number to a specific value."""
        parser = cmd2.Cmd2ArgumentParser()
        parser.add_argument('value', type=int,
                            help="The value to set the number to.")

        parsed_args = parser.parse_args(args)
        self.number = parsed_args.value
        self.poutput(self.number)

    @cmd2.with_argparser(cmd2.Cmd2ArgumentParser())
    def do_print(self, _):
        """Print the number."""
        self.poutput(self.number)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = CSVToDatabaseApp(sys.argv[1])
    else:
        app = CSVToDatabaseApp(0)
    app.cmdloop()
