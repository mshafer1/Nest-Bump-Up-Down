import pytest


def main(file):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-V', dest="verbosity", action='count', default=0,
                        help="Increase the level of logging output")
    args = parser.parse_args()
    verbosity = ['-v'] * args.verbosity

    pytest_args = [file, '-l'] + verbosity
    pytest.main(pytest_args)
