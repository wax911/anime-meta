import argparse

from app import Main

from domain.model import Parameters


def __description() -> str:
    return "Create your own anime meta data"


def __usage() -> str:
    return "vrv-meta.py --service vrv"


def __init_cli() -> argparse:
    parser = argparse.ArgumentParser(description=__description(), usage=__usage())
    parser.add_argument(
        '-s', '--service', default='usecase', help="generate using the specified service"
    )
    parser.add_argument(
        '-u', '--username', help="username for the selected service"
    )
    parser.add_argument(
        '-p', '--password', help="password for the selected service"
    )
    return parser


def __print_program_end() -> None:
    print("-----------------------------------")
    print("End of execution")
    print("-----------------------------------")


def __init_app(parameters: Parameters) -> None:
    Main(parameters).start()


if __name__ == '__main__':
    __cli_args = __init_cli().parse_args()
    __parameters = Parameters(
        __cli_args.service,
        __cli_args.username,
        __cli_args.password
    )
    __init_app(__parameters)
