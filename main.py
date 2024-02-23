from log import NewLogger
from config import Config
from router import commands
from args import create_parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    config = Config(args.home)
    logger = NewLogger(config.get_log())

    # Run the command
    commands[args.command](logger, config)

if __name__ == '__main__':
    main()
