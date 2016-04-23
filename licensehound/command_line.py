import sys

from licensehound import get_metadata


def get_package_info():
    if len(sys.argv) < 2:
        print("Usage: {} <pypi package name>".format(sys.argv[0]))
        sys.exit(-1)
    result, warnings = get_metadata(sys.argv[1])

    print("Result: {}".format(result))
    if len(warnings) > 0:
        print("Warnings: {}".format(warnings))
