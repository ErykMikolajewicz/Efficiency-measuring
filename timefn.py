import time
import os

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
            average = np.average(time_list)
            minimum = np.min(time_list)
            maximum = np.max(time_list)
            standard_deviation = np.std(time_list)
            report_text = []
            report_text.append(f"Result: {result} s")
            report_text.append(f"Average time of computing for {iteration} iterations: {average} s")
            report_text.append(f"Minimal time value: {minimum} s")
            report_text.append(f"Maximum time value: {maximum} s")
            report_text.append(f"Standard deviation: {standard_deviation} s")
            print()  # free line after tqdm bar
            [print(text) for text in report_text]
            path = f"Efficiency test/{function.__name__}"
            previous_report_exist = os.path.exists(path)
            if previous_report_exist:
                print("\nExist previous reports for than function.")
                display = input("Display last report? 'yes' or 'no': ")
                if display == "yes":
                    print()  # a free line, for better reading
                    with open(path, "r") as report:
                        last_report_line = report.readlines()[-len(report_text):]
                        [print(line, end="") for line in last_report_line]
            else:
                print("\nNo previous report for this function.")
            save = returning_input("Do you want to save this report? 'yes' or 'no': ")
            if save == "yes":
                if previous_report_exist:
                    pass
                else:
                    dir_exist = os.path.exists("Efficiency test")
                    if dir_exist:
                        pass
                    else:
                        os.mkdir("Efficiency test")
                    os.mknod(path)
                with open(path, "a") as report:
                    [report.writelines(line + '\n') for line in report_text]
        return measure_time
    return function_catcher
