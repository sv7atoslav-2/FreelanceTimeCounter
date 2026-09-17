import csv
import sys
from datetime import datetime, timedelta

def parse_time(time_str):
    """Parse a time string (e.g., '15:06') into a datetime.time object."""
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        return None

def calculate_time_diff(start, end):
    """Calculate the time difference between start and end times."""
    if start and end:
        start_time = datetime.combine(datetime.min, start)
        end_time = datetime.combine(datetime.min, end)
        if end_time < start_time:
            end_time += timedelta(days=1)  # Handle times spanning midnight
        return end_time - start_time
    return timedelta(0)

def parse_time_diff(diff):
    """Parse a time difference string (e.g., '1:05') into a timedelta object."""
    try:
        hours, minutes = map(int, diff.split(':'))
        return timedelta(hours=hours, minutes=minutes)
    except ValueError:
        return timedelta(0)

def calculate_total_time(file_path):
    """Calculate the total time from a CSV file and validate diff values."""
    total_time = timedelta()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start = parse_time(row.get('start', '0:0'))
            end = parse_time(row.get('end', '0:0'))
            recorded_diff = parse_time_diff(row.get('diff', '0:0'))

            calculated_diff = calculate_time_diff(start, end)

            if recorded_diff != calculated_diff:
                print(f"Warning: Discrepancy in row {row['date']} - using calculated diff.", file=sys.stderr)
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