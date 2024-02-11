from typing import Callable
from datetime import datetime

from computations import compute_stats, measure_times
from printing import returning_input, print_report
from storage import check_reports_exist, save_report, init_database, get_last_reports
from reports import Report


def function_timer(n_iterations=300, n_loops=30):
    def function_catcher(function: Callable):
        def time_report(*args, **kwargs):
            function_module = function.__module__
            function_name = function.__name__
            measurement_date = datetime.now()

            init_database()

            times = measure_times(function, n_iterations, n_loops, *args, **kwargs)

            stats = compute_stats(times)

            report = Report(function_module,
                            function_name,
                            n_iterations,
                            n_loops,
                            stats['mean'],
                            stats['median'],
                            stats['max'],
                            stats['min'],
                            stats['std'],
                            measurement_date)

            print_report(report)

            reports_exist = check_reports_exist(function_module, function_name)

            if reports_exist:
                print("\nExist previous reports for than function.")
                display = returning_input("Display last reports? 'yes' or 'no': ")
                if display == "yes":
                    reports_data = get_last_reports(function_module, function_name)
                    for report_data in reports_data:
                        report = Report(*report_data)
                        print_report(report)

            else:
                print("\nNo previous report for this function.")
            save_answer = returning_input("Do you want to save current report? 'yes' or 'no': ")
            if save_answer == "yes":
                save_report(report)

        return time_report
    return function_catcher


if __name__ == "__main__":
    @function_timer()
    def test_function():
        return 1

    test_function()
