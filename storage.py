import sqlite3

from reports import Report

connection = sqlite3.connect("reports.db")
cursor = connection.cursor()


def get_last_reports(function_module, function_name):
    query = f"""SELECT *
                FROM measurements
                WHERE function_module = '{function_module}'
                and function_name = '{function_name}'
                ORDER BY measure_date DESC
                LIMIT 15;"""
    last_reports = cursor.execute(query).fetchall()
    return last_reports


def save_report(report: Report):
    query = """INSERT INTO measurements
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(query, (report.function_module,
                           report.function_name,
                           report.n_iterations,
                           report.n_loops,
                           report.mean,
                           report.median,
                           report.max_,
                           report.min_,
                           report.std,
                           report.measurement_date,
                           report.time_series)
                   )
    connection.commit()


def check_reports_exist(function_module: str, function_name: str) -> bool:
    query = f"""SELECT function_name
                FROM measurements
                WHERE function_module = '{function_module}'
                and function_name = '{function_name}';"""
    first_row = cursor.execute(query).fetchone()
    if first_row:
        return True
    else:
        return False


def init_database():
    query = """CREATE TABLE IF NOT EXISTS measurements
                (
                function_module text,
                function_name text,
                n_iterations int,
                n_loops int,
                mean real,
                median real,
                max real,
                min real,
                std real,
                measure_date datetime,
                time_series text
                );"""
    cursor.execute(query)
    connection.commit()
