import cmd2
import argparse
import sys
import datetime
import re
from Utility.file_process import read_and_process_file
from Utility.lead_database_operations import remove_duplicates, json_to_database
from Utility.skiptrace import skiptrace_leads
from Utility.sengdrid_api import email_csv


class CSVToDatabaseApp(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.filePath = ""
        self.skiptraceCount = 0
        self.prompt = " > "
        self.display_splash()

    def display_splash(self):
        """Display splash screen with basic instructions."""
        splash_text = """

   ______                      _____  _                                 
   | ___ \                    /  ___|| |                                
   | |_/ / _ __   ___   _ __  \ `--. | |_  _ __   ___   __ _  _ __ ___  
   |  __/ | '__| / _ \ | '_ \  `--. \| __|| '__| / _ \ / _` || '_ ` _ \ 
   | |    | |   | (_) || |_) |/\__/ /| |_ | |   |  __/| (_| || | | | | |
   \_|    |_|    \___/ | .__/ \____/  \__||_|    \___| \__,_||_| |_| |_|
                       | |                                              
                       |_|                                              
     ___       _                                       _                
    / _ \     | |                                     | |               
   / /_\ \  __| |__   __  __ _  _ __    ___   ___   __| |               
   |  _  | / _` |\ \ / / / _` || '_ \  / __| / _ \ / _` |               
   | | | || (_| | \ V / | (_| || | | || (__ |  __/| (_| |               
   \_| |_/ \__,_|  \_/   \__,_||_| |_| \___| \___| \__,_|               
                                                                        
        
        Welcome to the PropStream Advanced command line interface!
        
        Available commands:

            process_file [FILE]: Adds file to database, given by filepath, to database.
            Removes duplicates in the process.

            skiptrace [OPTION]: Skiptraces data from database.
                Options
                    no flag: Skiptraces data added on todays date
                    -d: Skiptraces data added on provided date. Ex: [skiptrace -d 2023-11-01]

            email [OPTION]: Emails data added on todays date.
                Options
                    -d: Emails data added on given date. Ex: [email -d 2023-11-01]

            set_file_path [FILE]: Sets the filepath of file to be used. Must be csv or xlsx.

        Type 'help' or '?' for more details on commands.
        """
        self.poutput(splash_text)


    """
    Process file

    Process file data and add to database. Removes any duplicates (from those newly added) if they already exist.


    """
    @cmd2.with_default_category("File Management")
    def do_process_file(self, args):
        """Set the file path for location of CSV."""
        parser = cmd2.Cmd2ArgumentParser()
        parser.add_argument(
            "process_file",
            nargs=argparse.REMAINDER,
            type=str,
            help="Process the given csv or xlsx and add to database.",
        )

        parsed_args = parser.parse_args(args)

        # Join the characters back together into a single string
        self.filePath = "".join(parsed_args.process_file)

        # Add file contents to database
        response = read_and_process_file(self.filePath)

        if response:
            self.poutput("You must provide a XLSX or CSV file")
        else:
            self.poutput("File content successfully added to database.")
            # Remove duplicates
            remove_duplicates()

    """
    Skiptrace

    TODO: Instead of checking for the filepath, we must see if they gave any flags. 
    If they gave the date, we must see if there are elements that can be pulled from that date (Or do nothing and try and skiptrace on that date since it will just throw an error)
    If no date is given, we must skiptrace on todays date

    """
    skiptrace_parser = cmd2.Cmd2ArgumentParser()
    skiptrace_parser.add_argument('-d', '--date', type=str, help='Date in yyyy-mm-dd format', default=None)

    @cmd2.with_argparser(skiptrace_parser)
    def do_skiptrace(self, args):
        """Skiptrace."""

        date_to_use = None

        if args.date:
            # Check if the provided date is valid
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', args.date):
                print("Invalid date format. Please use yyyy-mm-dd.")
                return
            try:
                datetime.datetime.strptime(args.date, '%Y-%m-%d')
                date_to_use = args.date
            except ValueError:
                print("Invalid date provided.")
                return

        if self.skiptraceCount > 0:
            # Ask user if they are sure they want to skiptrace as it has already been done
            user_response = input("You've already performed a skiptrace. Are you sure you want to proceed again? (Y/n) ")
            if user_response.lower() != "y":
                return  # Exit the method if user is not sure
            else:
                # Call skiptrace function with filePath param and date
                skiptrace_leads(date_to_use)
                json_to_database()

                self.skiptraceCount += 1     

        else:
            # Call skiptrace function with filePath param and date
            skiptrace_leads(date_to_use)
            json_to_database()

            self.skiptraceCount += 1

    """
    Set file path

    Sets the path used to read in a CSV file from local machine. 
    
    """
    @cmd2.with_default_category("File Management")
    def do_set_file_path(self, args):
        """Set the file path for location of CSV."""
        parser = cmd2.Cmd2ArgumentParser()
        parser.add_argument(
            "file_path",
            nargs=argparse.REMAINDER,
            type=str,
            help="The file path to set as the location.",
        )

        parsed_args = parser.parse_args(args)

        # Join the characters back together into a single string
        self.filePath = "".join(parsed_args.file_path).strip("'")

        self.poutput(f"File path set to: [{self.filePath}]")


    """
    Email

    Email skiptraced data. 
    """
    email_parser = cmd2.Cmd2ArgumentParser()
    email_parser.add_argument('-d', '--date', type=str, help='Date in yyyy-mm-dd format', default=None)

    @cmd2.with_argparser(email_parser)
    def do_email(self, args):
        """Send data via email"""

        date_to_use = None

        if args.date:
            # Check if the provided date is valid
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', args.date):
                print("Invalid date format. Please use yyyy-mm-dd.")
                return
            try:
                datetime.datetime.strptime(args.date, '%Y-%m-%d')
                date_to_use = args.date
            except ValueError:
                print("Invalid date provided.")
                return

        email_csv(date_to_use)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = CSVToDatabaseApp(sys.argv[1])
    else:
        app = CSVToDatabaseApp()
    app.cmdloop()
