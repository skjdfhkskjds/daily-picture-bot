import argparse

# Create parser for command line arguments
# The parser requires:
#  - command: Command to run.
#  - home: Location of the project root.
# The parser also accepts the following optional flags:
#  - no-annotate: Flag to disable annotation.
# @return: parser object
def create_parser():
    parser = argparse.ArgumentParser()

    # Mandatory arguments
    parser.add_argument("command", type=str, help="Command to run.")
    
    # Flags with custom destination names
    parser.add_argument("--home", type=str, required=True, help="Location of the project root.")
    parser.add_argument("--no-annotate", action='store_true', help="Flag to disable annotation.")
 
    return parser

def validate_args(args, valid_commands):
    if args.command not in valid_commands:
        raise Exception("Invalid command. Please provide a valid command.")

    if args.home[-1] != '/':
        raise Exception("home must end with a '/'")
