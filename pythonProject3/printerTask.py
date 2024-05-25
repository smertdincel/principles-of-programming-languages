import threading  # Import threading for thread management


class PrintTask(threading.Thread):  # Define the PrintTask class inheriting from threading.Thread
    def __init__(self, printer, pattern_type, size, log_file, output_file):
        threading.Thread.__init__(self)  # Initialize the threading.Thread base class
        self.printer = printer  # Assign the printer object to an instance variable
        self.pattern_type = pattern_type  # Assign the pattern type to an instance variable
        self.size = size  # Assign the size to an instance variable
        self.log_file = log_file  # Assign the log file name to an instance variable
        self.output_file = output_file  # Assign the output file name to an instance variable

    def run(self):  # Define the run method, which is executed when the thread starts
        try:
            self.printer.print_pattern(self.pattern_type, self.size, self.log_file, self.output_file)  # Call the print_pattern method on the printer object
        except Exception as e:  # Handle any exceptions that occur during the print process
            print(f"Error: {e}")  # Print the error message
