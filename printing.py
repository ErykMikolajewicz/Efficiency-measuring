from reports import Report


def returning_input(input_text: str) -> str:
    while True:
        answer = input(input_text)
        if answer == "yes" or answer == "no":
            return answer
        print('''Incorrect answer write "yes" or "no" in console, and click enter''')


def print_report(report: Report):
    print(f"""
    ---------------------------- Report ----------------------------
    Created: {report.measurement_date}
    Function: {report.function_name} from module: {report.function_module}
    Number of iterations: {report.n_iterations}
    Number of loops: {report.n_loops}
    Mean: {report.mean} s
    Median: {report.median} s
    Minimal time value: {report.max_} s
    Maximum time value: {report.min_} s
    Standard deviation: {report.std} s
    """)
