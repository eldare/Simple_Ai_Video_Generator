#
#  log.py
#
#  Created by Eldar Eliav on 2023/05/11.
#

import datetime
import inspect

class log:  # pylint: disable=invalid-name
    @staticmethod
    def info(text: str):
        log._print("INFO", text)

    @staticmethod
    def warning(text: str, exception: Exception):
        log._print("WARNING", f"{text} (Exception: {exception})")

    @staticmethod
    def error(text: str, exception: Exception):
        log._print("ERROR", f"{text} (Exception: {exception})")

    @staticmethod
    def _print(level: str, text: str):
        caller_frame = inspect.stack()[2]
        caller_class = caller_frame[0].f_locals.get('self', None).__class__.__name__
        caller_class_line_number = caller_frame[2]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"{timestamp} {caller_class}:{caller_class_line_number} - [{level}] {text}")
