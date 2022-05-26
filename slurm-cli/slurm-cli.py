import argparse
import parse

if __name__ == "__main__":

    # Parse arguments
    # Usage: python slurm-cli.py a.run
    # It will parse a.run and do next
    # Value of args.input is "a.run"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="input file")
    args = parser.parse_args()
    parse.parse(args.input)
