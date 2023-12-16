#!/bin/bash

get_last_entry() {
    # Get the last entry from a file
    local file_path="$1"
    if [ -f "$file_path" ]; then
        local last_line=$(tail -n 1 "$file_path")
        if [ "$last_line" ]; then
            echo "$last_line" | tr -d '\n'
        fi
    fi
}

inhibit_shutdown() {
    # Inhibit shutdown by ignoring interrupt and termination signals
    trap '' INT TERM
    echo "Inhibiting shutdown."
}

open_kitty_terminal() {
    # Open a new kitty terminal with a reminder message
    message="Please clock out for $job_name."
    env ZDOTDIR="$empty_dir" kitty --hold --title "Timecard Reminder" bash -c "echo '$message'; exec $SHELL"
}

# Check if the script is invoked with a shutdown signal
if [ "$1" == "shutdown_signal" ]; then
    # Set the directory where timecard files are stored
    timecard_directory=~/.config/timecard

    # Extract job names from timecard filenames
    job_names=($(ls "$timecard_directory" | grep "^timeCard_" | sed 's/timeCard_\(.*\)\.log/\1/'))

    # Iterate over each job name
    for job_name in "${job_names[@]}"; do
        # Construct the path to the timecard file for the current job
        timecard_file="$timecard_directory/timeCard_$job_name.log"
        
        # Get the last entry from the timecard file
        last_entry=$(get_last_entry "$timecard_file")

        # Check if the last entry is a clock-in entry
        if [ "$last_entry" ] && [ "$(echo "$last_entry" | grep "Clocked In:")" ]; then
            # If so, inhibit shutdown and open a kitty terminal with a reminder
            inhibit_shutdown
            open_kitty_terminal
        fi
    done

    # Print a message if no action is needed for all job names
    echo "No action needed. Last entries checked for all possible job names."
else
    # If the script is not invoked with a shutdown signal, print a warning
    echo "This script should be invoked only when a shutdown signal is received."
    exit 1
fi
