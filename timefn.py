import time
import os
import sqlite3

import numpy as np
from tqdm import tqdm


def returning_input(input_text: str) -> str:
    while True:
        answer = input(input_text)
        if answer == "yes" or answer == "no":
            return answer
        print('''Incorrect answer wite "yes" or "no" in console, and click enter''')




def function_timer(iteration=300, loops=30):
    def function_catcher(function):
        def measure_time(*args, **kwargs):
            time_list = np.zeros(iteration)
            for i in tqdm(range(iteration)):
                t1 = time.time()
                for _ in range(loops):
                    result = function(*args, **kwargs)
                t2 = time.time()
                time_list[i] = (t2-t1)
            median = np.median(time_list)
            minimum = np.min(time_list)
            maximum = np.max(time_list)
            standard_deviation = np.std(time_list)
            report_text = []
            report_text.append(f"Result: {result}")
            report_text.append(f"Median time of computing for {iteration} iterations: {median} s")
            report_text.append(f"Minimal time value: {minimum} s")
            report_text.append(f"Maximum time value: {maximum} s")
            report_text.append(f"Standard deviation: {standard_deviation} s")
            print()  # free line after tqdm bar
            [print(text) for text in report_text]

            connection = sqlite3.connect("reports.db")
            cursor = connection.cursor()
            reports_exists = cursor.execute(f"""SELECT name
                                            FROM sqlite_schema
                                            WHERE type='table' AND name='{function.__module__}';""").fetchone()

            if reports_exists:
                print("\nExist previous reports for than function.")
                display = returning_input("Display last report? 'yes' or 'no': ")
                if display == "yes":
                    print()  # a free line, for better reading
                    last_reports = cursor.execute(f"""Select *
                                                   FROM {function.__module__}
                                                   WHERE function_name='{function.__name__}'
                                                   ORDER BY measuring_date
                                                   LIMIT 15;
                                                   """)
                    for report in last_reports:
                        print(report)
            else:
                print("\nNo previous report for this function.")
            save = returning_input("Do you want to save this report? 'yes' or 'no': ")
            if save == "yes":
                if not reports_exists:
                    cursor.execute(f"""CREATE TABLE {function.__module__}
                                    (function_name text,
                                    result real,
                                    median real,
                                    standard_deviation real,
                                    maximum_value real,
                                    minimum_value real,
                                    measuring_date date,
                                    iteration int,
                                    loops int
                                    );""")
                values_to_save = (function.__name__, result, median, standard_deviation, maximum, minimum, time.time(),
                                  iteration, loops)
                cursor.execute(f"""INSERT INTO {function.__module__}
                               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
                               """, values_to_save)
                connection.commit()
        return measure_time
    return function_catcher


if __name__ == "__main__":
    @function_timer()
    def test_function():
        return 1

    test_function()
