#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta
import os

def clock_in(job_name):
    """
    Clock in for a specific job.

    Parameters:
    - job_name (str): The name of the job.
    """
    now = datetime.now()
    job_file = open(
        os.path.expanduser(f"~/.config/timecard/timeCard_{job_name}.log"),
        "a",
    )
    job_file.write("Clocked In: {}\n".format(now.strftime("%Y-%m-%d %H:%M:%S")))
    job_file.close()
    print(f"You have clocked in for {job_name}!")

def clock_out(job_name):
    """
    Clock out for a specific job.

    Parameters:
    - job_name (str): The name of the job.
    """
    now = datetime.now()
    job_file = open(
        os.path.expanduser(f"~/.config/timecard/timeCard_{job_name}.log"),
        "a+"
    )
    job_file.write("Clocked Out: {}\n".format(now.strftime("%Y-%m-%d %H:%M:%S")))
    job_file.write("\n")
    job_file.close()

    # Calculate total hours worked for the day
    file_path = os.path.expanduser(f"~/.config/timecard/timeCard_{job_name}.log")
    last_lines = read_last_three_lines(file_path)

    clock_in_string = last_lines[0]
    clock_out_string = last_lines[1]

    print(clock_in_string[12:])
    print(clock_out_string[13:])

    clock_in = datetime.strptime(clock_in_string[12:], '%Y-%m-%d %H:%M:%S')
    clock_out = datetime.strptime(clock_out_string[13:], '%Y-%m-%d %H:%M:%S')

    time_worked = clock_out - clock_in
    date = datetime.now().strftime("%Y-%m-%d")
    hours_worked_string = f"{time_worked}\n"

    # Open the hours file and check if there's an existing entry for the current date
    hours_file_path = os.path.expanduser(f"~/.config/timecard/hours_{job_name}.log")
    with open(hours_file_path, 'a+') as hours_file:
        hours_file.seek(0)
        existing_lines = hours_file.readlines()
        for i, line in enumerate(existing_lines):
            if date in line:
                # Update the existing entry with the total hours
                existing_hours = existing_lines[i + 1].strip()
                existing_hours_dt = datetime.strptime(existing_hours, '%H:%M:%S')
                total_hours = existing_hours_dt + time_worked
                existing_lines[i + 1] = f"{total_hours.hour:02d}:{total_hours.minute:02d}:{total_hours.second:02d}\n"
                break
        else:
            # If no existing entry, create a new one
            existing_lines.extend([f"Hours Worked {date}:\n", hours_worked_string])

        # Write the updated entries back to the hours file
        hours_file.seek(0)
        hours_file.truncate()
        hours_file.writelines(existing_lines)

    print(f"You have clocked out for {job_name}!")

def show_hours(job_name, days):
    """
    Print hours worked for the last n calendar days.

    Parameters:
    - job_name (str): The name of the job.
    - days (int): Number of days to consider for showing hours.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    hours_file_path = os.path.expanduser(f"~/.config/timecard/hours_{job_name}.log")
    with open(hours_file_path, 'r') as hours_file:
        for line in hours_file:
            if line.startswith("Hours Worked"):
                date_str, hours_str = line.split(':')
                date = datetime.strptime(date_str[13:], '%Y-%m-%d')
                if start_date <= date <= end_date:
                    next_line = hours_file.readline().strip()
                    print(f"{line.strip()} {next_line}")
                    
def read_last_three_lines(file_path):
    """
    Read the last three lines from a file.

    Parameters:
    - file_path (str): Path to the file.

    Returns:
    - list: List containing the last three lines.
    """
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        file_size = file.tell()
        current_position = file_size
        lines_to_read = 4
        lines = []

        while current_position > 0 and lines_to_read > 0:
            current_position -= 1
            file.seek(current_position)
            char = file.read(1)

            if char == '\n':
                lines_to_read -= 1
                lines.insert(0, file.readline().strip())

        return lines

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: timecard [clock-in/clock-out/show-hours] job_name [days]")
        sys.exit(1)

    command = sys.argv[1]
    job_name = sys.argv[2]

    if command == "clock-in":
        clock_in(job_name)
    elif command == "clock-out":
        clock_out(job_name)
    elif command == "show-hours":
        if len(sys.argv) < 4:
            print("Usage: timecard show-hours job_name days")
            sys.exit(1)
        days = int(sys.argv[3])
        show_hours(job_name, days)
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)
