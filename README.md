# Timecard

Timecard is a Python command-line utility for tracking work hours. 
It allows you to clock in and out for different jobs, maintains a log of your work hours, and calculates the total hours worked for each day.

## Features

- **Clock In and Out:** Easily record your work hours by clocking in and out for different jobs.

- **Log Files:** Each job has its own log file (`timeCard_job_name.log`) that stores clock-in and clock-out timestamps.

- **Hours Calculation:** The program calculates the total hours worked for each day and stores the information in a separate hours log file (`hours_job_name.log`).

- **Show Hours:** View the total hours worked for the last N calendar days using the `timecard show-hours` command.

## Installation

1. Clone the repository:

    ```
    $ git clone https://github.com/your-username/timecard.git
    ```

2. Navigate to the `timecard` directory:

    ```
    $ cd timecard
    ```

3. Make the `timecard.py` script executable:

    ```
    $ chmod +x timecard.py
    ```

4. Optionally, copy the script to a directory in your `$PATH` for easier access:

    ```
    $ cp timecard.py /usr/local/bin/timecard
    ```

## Usage

### Clock In

```
$ timecard clock-in job_name
```

### Clock Out
```
$ timecard clock-out job_name
```

### Show Hours
```
$ timecard show-hours job_name number_of_days
```

## Configuration 

- Adjust the log file paths it the script **(`timecard.py`)** if needed.

## License

This repository is licensed under the GPLv3 license. See the [LICENSE](LICENSE) file for details.


