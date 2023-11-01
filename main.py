import cmd2
import argparse
import sys
from Utility.file_process import read_and_process_file


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

            process_file [FILE]: Adds file to database, given by filepath, to database. Removes duplicates in the process.
            skiptrace [OPTION]: Skiptraces data from database.
                Options
                    -no flag: Skiptraces data added on todays date
                    -date: Skiptraces data added on provided date
            email [OPTION]: Emails data added on todays date.
                Options
                    -date: Emails data added on given date. 
            set_file_path [FILE]: Sets the filepath of file to be used. Must be csv or xlsx.


        Type 'help' or '?' for more details on commands.
        """
        self.poutput(splash_text)


    """
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
            # Remove duplicates here

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
    Skiptrace

    TODO: Instead of checking for the filepath, we must see if they gave any flags. 
    If they gave the date, we must see if there are elements that can be pulled from that date (Or do nothing and try and skiptrace on that date since it will just throw an error)
    If no date is given, we must skiptrace on todays date

    """
    @cmd2.with_argparser(cmd2.Cmd2ArgumentParser())
    def do_skiptrace(self, _):
        """Skiptrace."""

        if self.filePath == "":
            # Tell them they must enter filepath first with the set_file_path function
            self.poutput("You must enter a filepath first using the set_file_path function.")
            return  # Exit the method 
        elif self.skiptraceCount > 0:
            # Ask user if they are sure they want to skiptrace as it has already been done
            user_response = input("You've already performed a skiptrace. Are you sure you want to proceed again? (Y/n) ")
            if user_response.lower() != "y":
                return  # Exit the method if user is not sure
            else:
                # Call skiptrace function with filePath param
                self.perform_skiptrace(
                    self.filePath
                ) 
                self.skiptraceCount += 1          
        else:
            # Call skiptrace function with filePath param
            self.perform_skiptrace(
                self.filePath
            ) 
            self.skiptraceCount += 1

    """
    THIS WILL BE IMPORTED FROM UTILITY FOR SKIPTRACE
    """

    def perform_skiptrace(self, filePath):
        # Placeholder for your actual skiptrace logic
        self.poutput(f"Performing skiptrace on file: {filePath}")

    @cmd2.with_argparser(cmd2.Cmd2ArgumentParser())
    def do_print(self, _):
        """Print the number."""
        self.poutput(self.number)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = CSVToDatabaseApp(sys.argv[1])
    else:
        app = CSVToDatabaseApp()
    app.cmdloop()
