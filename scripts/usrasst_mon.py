import os
import re
import sys
sys.path.append("..")
import fmt
import json
import logging
import argparse
from userassist import regmon

VERSION = "0.1.0"
VALID_DEBUG_LEVELS = ["ERROR", "WARN", "INFO", "DEBUG"]
RE_USER_ASSIST = re.compile(r"CurrentVersion\\Explorer\\UserAssist")

logging.basicConfig(
    level=logging.DEBUG
)

available_keys = [
    "timestamp",
    "key_name",
    "value_name",
    "value_decoded_name",
    "session",
    "run_count",
    "focus_count",
    "focus_time",
    "last_execution"
]


def set_debug_level(debug_level):
    if debug_level in VALID_DEBUG_LEVELS:
        logging.basicConfig(
            level=getattr(
                logging,
                debug_level
            )
        )
    else:
        raise(
            Exception(
                "{} is not a valid debug level.".format(
                    debug_level
                )
            )
        )


def get_arguments():
    usage = u"""Monitor UserAssist Registry Keys. This tool will also display current values before monitoring starts.
Version: {}
    """.format(VERSION)

    arguments = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    arguments.add_argument(
        "--format",
        dest="format",
        action="store",
        default=None,
        help="Python fstring."
    )

    arguments.add_argument(
        "--debug",
        dest="debug",
        action="store",
        default="ERROR",
        choices=VALID_DEBUG_LEVELS,
        help="Debug level [default=ERROR]"
    )

    return arguments


def main():
    arguments = get_arguments()
    options = arguments.parse_args()

    set_debug_level(
        options.debug
    )

    output_handler = OutputHandler(
        options.format
    )

    mon = regmon.UserAssistMonitor(
        output_handler.callback
    )
    mon.start()
    mon.join()


class OutputHandler(object):
    def __init__(self, format=None):
        self.format = format

    def callback(self, record):
        if self.format:
            print(fmt(self.format))
        else:
            print(json.dumps(dict(record)))


if __name__ == "__main__":
    main()
