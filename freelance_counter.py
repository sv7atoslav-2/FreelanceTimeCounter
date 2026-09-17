import csv
import sys
from datetime import datetime, timedelta


def parse_time(time_str, row_date, is_start: bool):
    """Parse a time string (e.g., '15:06') into a datetime.time object."""
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError as ve:
        smg = "start" if is_start else "end"
        raise ValueError(f"Error: \"{smg} time\" is missing in row {row_date}. Program is crashed") from ve


def parse_time_diff(row) -> timedelta:
    """Parse a time difference string (e.g., '1:05') into a timedelta object."""
    try:
        diff = row.get('diff')
        hours, minutes = map(int, diff.split(':'))
        return timedelta(hours=hours, minutes=minutes)
    except ValueError:
        print(f"Warning: Discrepancy in row {row['date']} - using zero value", file=sys.stderr)
        return timedelta(hours=0, minutes=0)


def calculate_time_diff(start, end):
    """Calculate the time difference between start and end times."""
    if not start or not end:
        raise NotImplementedError("I turn on checks yet at parsing, but cheks failed, and values empty. Damn!")
    start_time = datetime.combine(datetime.min, start)
    end_time = datetime.combine(datetime.min, end)
    if end_time < start_time:
        raise NotImplementedError("Work at midnight it a very bad idea!")
    return end_time - start_time


def calculate_total_time(file_path):
    """Calculate the total time from a CSV file and validate diff values."""
    total_time = timedelta()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start = parse_time(row.get('start'), row['date'], True)
            end = parse_time(row.get('end'), row['date'], False)

            recorded_diff = parse_time_diff(row)
            calculated_diff = calculate_time_diff(start, end)

            if recorded_diff != calculated_diff:
                print(f"Warning: Discrepancy in row {row['date']}. Used calculated diff.", file=sys.stderr)
                rec_diff_min = int(recorded_diff.total_seconds() // 60)
                calc_diff_min = int(calculated_diff.total_seconds() // 60)
                print(f"{rec_diff_min=} ; {calc_diff_min=}")
                total_time += calculated_diff
            else:
                total_time += recorded_diff

    return total_time


def format_total_time(total_time):
    """Format the total time as hhh:mm with leading zeros if necessary."""
    total_minutes = total_time.total_seconds() // 60
    hours, minutes = divmod(int(total_minutes), 60)
    return f"{hours:03}:{minutes:02}"


def main():
    if len(sys.argv) != 3 or sys.argv[1] != '-f':
        print("Usage: hours.py -f <csv_file>")
        sys.exit(1)

    file_path = sys.argv[2]
    total_time = calculate_total_time(file_path)
    formatted_time = format_total_time(total_time)
    print(formatted_time)


if __name__ == "__main__":
    main()
