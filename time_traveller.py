import random
import subprocess
from datetime import datetime, timedelta


def clear_working_tree():
    result = subprocess.run(['git', 'reset', '--hard'], check=True,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def should_commit(percentage=30):
    # Ensure percentage is between 0 and 100
    percentage = max(0, min(100, percentage))

    # Generate a random number between 0 and 100
    random_number = random.randint(0, 100)

    # Check if the random number is less than the specified percentage
    return random_number < percentage


def get_dates_between(start_date, end_date):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    current_date = start_date
    while current_date <= end_date:
        if(should_commit()):
            print(current_date.strftime(date_format))
            with open("README.md", "w") as readme_file:
                readme_file.write(str(current_date))

            result = subprocess.run(['git', 'add', '.'], check=True,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            commit_message = 'commit ' + str(current_date)


            result = subprocess.run(['git', 'commit', '--allow-empty', '-m', commit_message, '--date', str(current_date)],
                        check=True, text=True, env={'GIT_COMMITTER_DATE': str(current_date), 'GIT_AUTHOR_DATE': str(current_date)}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


            result = subprocess.run(['git', 'commit', '--amend', '--reset-author', '-m', commit_message, '--date', str(current_date)],
                        check=True, text=True, env={'GIT_COMMITTER_DATE': str(current_date), 'GIT_AUTHOR_DATE': str(current_date)}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(result.stdout)

        current_date += timedelta(days=1)


if __name__ == "__main__":
    start_date_input = input("Enter the start date (YYYY-MM-DD): ")
    end_date_input = input("Enter the end date (YYYY-MM-DD): ")
    clear_working_tree()

    try:
        get_dates_between(start_date_input, end_date_input)
    except ValueError as e:
        print(f"Error: {e}. Please enter valid date formats.")
