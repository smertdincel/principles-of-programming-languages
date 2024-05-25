import threading  # Import threading for creating threads
import time  # Import time for handling delays
from queue import Queue  # Import Queue for task management

from printer import Printer  # Import Printer class from printer module
from printerTask import PrintTask  # Import PrintTask class from printerTask module


def worker(printer, queue, current_pattern_type):
    while True:  # Infinite loop for worker thread to continuously process tasks
        task, log_file, output_file = queue.get()  # Get a task from the queue
        if task is None:  # Check if the task is a termination signal
            break  # Exit the loop to terminate the worker
        if current_pattern_type[0] != task.pattern_type:  # Check if the current pattern type has changed
            current_pattern_type[0] = task.pattern_type  # Update the current pattern type
        task.start()  # Start the print task
        task.join()  # Wait for the print task to complete
        queue.task_done()  # Indicate that the task is done


def main():
    printer = Printer()  # Create an instance of Printer
    file_names = ['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt']  # List of input file names
    base_path = "C:/Users/USER/Desktop/files/"  # Base path for input files
    queue = Queue()  # Create a queue for task management
    current_pattern_type = [None]  # Mutable type to share current pattern type between threads

    # Create worker threads
    num_worker_threads = 2  # Number of worker threads to create
    threads = []  # List to keep track of thread objects
    for i in range(num_worker_threads):  # Loop to create worker threads
        t = threading.Thread(target=worker, args=(printer, queue, current_pattern_type))  # Create a worker thread
        t.start()  # Start the worker thread
        threads.append(t)  # Add the thread to the list

    for file_index, file_name in enumerate(file_names):  # Loop through each input file
        try:
            with open(base_path + file_name, 'r') as file:  # Open the input file
                lines = file.readlines()  # Read all lines from the file

            log_file = f"log{file_index + 1}.txt"  # Generate log file name
            output_file = f"output{file_index + 1}.txt"  # Generate output file name

            for line in lines:  # Loop through each line in the input file
                parts = line.strip().split("\t")  # Split the line into parts
                if len(parts) != 3:  # Check if the line has exactly 3 parts
                    print(f"Invalid line format in {file_name}: {line.strip()}")  # Print error message
                    continue  # Skip to the next line

                try:
                    request_time = int(parts[0])  # Parse request time from the line
                    pattern_type = parts[1]  # Get pattern type from the line
                    size = int(parts[2])  # Parse size from the line
                except ValueError:  # Handle parsing errors
                    print(f"Invalid data in {file_name}: {line.strip()}")  # Print error message
                    continue  # Skip to the next line

                task = PrintTask(printer, pattern_type, size, log_file, output_file)  # Create a print task
                queue.put((task, log_file, output_file))  # Add the task to the queue
                time.sleep(request_time / 1000)  # Delay for request_time milliseconds

        except FileNotFoundError:  # Handle file not found errors
            print(f"{file_name} bulunamadı.")  # Print error message
        except Exception as e:  # Handle other exceptions
            print(f"{file_name} dosyası açılırken bir hata oluştu:", e)  # Print error message
            exit(1)  # Exit the program

    # Stop workers
    queue.join()  # Wait for all tasks in the queue to be processed
    for i in range(num_worker_threads):  # Loop to send termination signals to workers
        queue.put((None, None, None))  # Add a termination signal to the queue
    for t in threads:  # Loop through all worker threads
        t.join()  # Wait for the worker thread to terminate


if __name__ == "__main__":  # Check if the script is being run directly
    main()  # Call the main function
