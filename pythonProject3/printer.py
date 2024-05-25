import threading  # Import threading for thread management


class Printer:
    def __init__(self):
        self.lock = threading.Lock()  # Create a lock to synchronize access to shared resources
        self.current_pattern_type = None  # Initialize the current pattern type to None

    def print_pattern(self, pattern_type, size, log_file, output_file):
        with self.lock:  # Acquire the lock to ensure exclusive access
            if self.current_pattern_type is None:  # Check if the current pattern type is not set
                self.current_pattern_type = pattern_type  # Set the current pattern type
            if self.current_pattern_type != pattern_type:  # Check if the pattern type has changed
                self.current_pattern_type = pattern_type  # Update to the new pattern type
            with open(log_file, 'a') as log:  # Open the log file in append mode
                log.write(f"Start printing {pattern_type} pattern of size {size}\n")  # Log the start of printing

            self._print_pyramid(pattern_type, size, output_file)  # Call the method to print the pattern

            with open(log_file, 'a') as log:  # Open the log file in append mode again
                log.write(f"Finished printing {pattern_type} pattern of size {size}\n")  # Log the end of printing

    def _print_pyramid(self, pattern_type, size, output_file):
        output = ""  # Initialize the output string
        for i in range(1, size + 1):  # Loop through each row from 1 to size
            # Add leading spaces for pyramid alignment
            output += " " * (size - i) * 2  # Calculate and add leading spaces for the current row
            if pattern_type == "Star":  # Check if the pattern type is "Star"
                # Generate the star pattern with spaces in between
                for j in range(2 * i - 1):  # Loop to add the stars in the current row
                    output += "* "  # Add a star and a space
            elif pattern_type == "Alphabet":  # Check if the pattern type is "Alphabet"
                # Start character for the current row
                start_char = chr(ord('A') + i - 1)  # Determine the starting character for the current row
                # Generate the increasing part of the row
                for j in range(i):  # Loop to add the increasing part of the row
                    output += chr(ord(start_char) + j) + " "  # Add the current character and a space

                # Generate the decreasing part of the row
                for j in range(i - 2, -1, -1):  # Loop to add the decreasing part of the row
                    output += chr(ord(start_char) + j) + " "  # Add the current character and a space

            # Remove trailing space and add newline
            output = output.rstrip() + "\n"  # Remove trailing space and add a newline character

        print(output)  # Print the output string
        with open(output_file, 'a') as out_file:  # Open the output file in append mode
            out_file.write(output)  # Write the output string to the file

    # Example usage:
    # _print_pyramid("Star", 7, "output.txt")  # Call the method with pattern type "Star" and size 7
