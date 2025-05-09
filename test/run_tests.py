#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""
Runs unit tests and generates an HTML report.
"""
import argparse
import os
import shlex
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path

import argcomplete
import HTMLTestRunner
import xmlrunner

# Define command-line arguments using argparse
parser = argparse.ArgumentParser(description="Run tests and generate an HTML report.")
parser.add_argument(
    "--format",
    "-f",
    default="text",
    choices=("text", "html", "junit"),
    help="Output format (defaults to 'text').",
)
parser.add_argument(
    "--test-directory",
    default="systests",
    type=Path,
    help="Directory where test files are located",
)
parser.add_argument(
    "--output-dir",
    default="report",
    type=Path,
    help="Directory where the reports will be saved",
)
parser.add_argument(
    "--verbosity", default=2, type=int, help="Verbosity level for test output"
)
parser.add_argument(
    "--copy-logs", action="store_true", help="Copy Kubernetes logs to the report dir."
)


text_group = parser.add_argument_group("Text output")
text_group.add_argument("--failfast", action="store_true", default=False)

html_group = parser.add_argument_group("HTML output")
html_group.add_argument(
    "--output-file",
    type=Path,
    help="Filename of the report HTML file (incompatible with --output-dir).",
)
html_group.add_argument(
    "--title", default="System Tests", help="Title of the HTML report"
)
html_group.add_argument(
    "--report-name", default="systests", help="Name of the HTML report file"
)
html_group.add_argument(
    "--open-in-browser", action="store_true", help="Open the report in the browser"
)
html_group.add_argument(
    "--description", default="Reports", help="Description of the report"
)
html_group.add_argument(
    "--tested-by", default="", help="Person who conducted the tests"
)
html_group.add_argument(
    "--remove-traceback", action="store_false", help="Remove traceback to the report"
)
html_group.add_argument(
    "--log", action="store_true", help="Enable logging during test execution"
)


def main():
    "main()"
    # Allow argument completion from the console
    argcomplete.autocomplete(parser)

    # Add some dependencies to the PYTHONPATH
    sys.path.append(str(Path(__file__).parent / "test_util"))

    # Allow execution from any directory
    os.chdir(Path(__file__).parent)

    # Parse the command-line arguments
    args = parser.parse_args()

    print("Hostname:", socket.gethostname())

    Path("report/").mkdir(parents=True, exist_ok=True)

    # Create a variable to load unittest tests
    loader = unittest.TestLoader()

    # Discover and load all tests that match the 'test_*.py' pattern in the specified directory
    suite = unittest.TestSuite(
        loader.discover(start_dir=str(args.test_directory), pattern="test_*.py")
    )
    match args.format:
        case "text":
            runner = get_text_runner(args)
            test_result = runner.run(suite)
        case "html":
            runner = get_html_runner(args)
            test_result = runner.run(suite)
        case "junit":
            with open("report/junit.xml", "wb") as output:
                runner = xmlrunner.XMLTestRunner(output=output, verbosity=2)
                test_result = runner.run(suite)

    if args.copy_logs:
        os.chdir(args.output_dir)
        for k8s_obj in ("pod", "svc", "ingress"):
            with open(f"k8s_{k8s_obj}.txt", "w", encoding="utf8") as f:
                cmd = ["kubectl", "get", k8s_obj]
                print(shlex.join(cmd), "...")
                subprocess.check_call(cmd, stdout=f)
        os.system(
            """
            kubectl get svc -o=name | while read pod ; do
                echo $pod ...
                kubectl logs --tail=50 --all-containers ${pod} > $(echo ${pod}.log | tr / _)
            done
            """
        )

    # Check the result of the tests and set the exit code accordingly
    if len(test_result.errors) == len(test_result.failures) == 0:
        sys.exit(0)  # Exit code 0 for success
    else:
        sys.exit(1)  # Exit code 1 for failure


def get_text_runner(args):
    "Creates a TextTestRunner object to generate the text output in the console."
    return unittest.TextTestRunner(failfast=args.failfast, verbosity=args.verbosity)


def get_html_runner(args):
    "Creates an HTMLTestRunner object to generate the HTML report."
    if args.output_file is not None:
        args.output_dir = str(args.output_file.parent)

    runner = HTMLTestRunner.HTMLTestRunner(
        log=args.log,
        verbosity=args.verbosity,
        output=args.output_dir,
        title=args.title,
        report_name=args.report_name,
        open_in_browser=args.open_in_browser,
        description=args.description,
        tested_by=args.tested_by,
        add_traceback=args.remove_traceback,
    )

    # Embed style and script
    static_files = Path(HTMLTestRunner.__path__[0]) / "static"
    with open(str(static_files / "stylesheet.css"), encoding="utf8") as f:
        runner.style = f.read()
    with open(str(static_files / "script.js"), encoding="utf8") as f:
        runner.script = f.read()

    if args.output_file is not None:
        if args.output_file.suffix != ".html":
            sys.exit("Output file must end with '.html': " + str(args.output_file))
        runner.html_report_file_name = args.output_file
    else:
        runner.html_report_file_name = (
            Path(runner.output_dir)
            / f'{runner.report_name}_{time.strftime("%Y-%m-%d_%H-%M-%S")}.html'
        )

    print("Report path:", runner.html_report_file_name, file=sys.stderr)

    return runner


def is_safe_mode():
    """
    Returns the value of the --safe-mode option.
    """
    return parser.parse_args().safe_mode


def long_tests_enabled():
    """
    Checks whether long tests are enabled.
    """
    return parser.parse_args().no_long


if __name__ == "__main__":
    main()
