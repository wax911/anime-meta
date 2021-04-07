import argparse

from app import Main

from domain.model import Parameters


def __description() -> str:
    return "Create your own anime meta data"


def __usage() -> str:
    return "vrv-meta.py --service crunchyroll"


def __init_cli() -> argparse:
    parser = argparse.ArgumentParser(description=__description(), usage=__usage())
    parser.add_argument(
        '-s', '--service', help="generate using the specified service"
    )
    parser.add_argument(
        '-c', '--credentials', help="credentials to use for logging in"
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
        __cli_args.credentials
    )
    try:
        __init_app(__parameters)
    except KeyboardInterrupt as e:
        pass
