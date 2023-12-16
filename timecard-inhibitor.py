#!/usr/bin/env python
import os
import subprocess
import signal
import sys

def get_last_entry(file_path):
    """
    Get the last entry from a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The last entry from the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        return None

def inhibit_shutdown():
    """
    Inhibit shutdown by ignoring interrupt and termination signals.
    """
    # Ignore interrupt (e.g., Ctrl+C) and termination signals
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    print("Inhibiting shutdown.")

def open_kitty_terminal(message):
    """
    Open a new kitty terminal with a specified message.

    Args:
        message (str): The message to display in the kitty terminal.
    """
    # Specify the path to an empty directory
    empty_dir = os.path.expanduser("~/.config/kitty/empty_dir")
    
    # Create the empty directory if it doesn't exist
    os.makedirs(empty_dir, exist_ok=True)
    
    # Set the ZDOTDIR environment variable to the empty directory
    command = ["env", f"ZDOTDIR={empty_dir}", "kitty", "--hold", "--title", "Timecard Reminder", "bash", "-c", f"echo '{message}'; exec $SHELL"]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error opening kitty terminal: {e}")

if __name__ == "__main__":
    # Check if the script is invoked with a shutdown signal
    if len(sys.argv) > 1 and sys.argv[1] == "shutdown_signal":
        # Set the directory where timecard files are stored
        timecard_directory = os.path.expanduser("~/.config/timecard")

        # Extract job names from timecard filenames
        job_names = [f.split('_')[1].split('.')[0] for f in os.listdir(timecard_directory) if f.startswith("timeCard_")]

        # Iterate over each job name
        for job_name in job_names:
            # Construct the path to the timecard file for the current job
            timecard_file = os.path.join(timecard_directory, f"timeCard_{job_name}.log")
            
            # Get the last entry from the timecard file
            last_entry = get_last_entry(timecard_file)

            # Check if the last entry is a clock-in entry
            if last_entry and "Clocked In:" in last_entry:
                # If so, inhibit shutdown and open a kitty terminal with a reminder
                inhibit_shutdown()
                message = f"Please clock out for {job_name}."
                open_kitty_terminal(message)

        # Print a message if no action is needed for all job names
        print("No action needed. Last entries checked for all possible job names.")
    else:
        # If the script is not invoked with a shutdown signal, print a warning
        print("This script should be invoked only when a shutdown signal is received.")
        sys.exit(1)
