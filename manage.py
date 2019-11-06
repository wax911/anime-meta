import argparse
from data.model import Parameters


def __description() -> str:
    return "Create your own anime meta data"


def __usage() -> str:
    return "manage.py --service vrv"


def __init_cli() -> argparse:
    parser = argparse.ArgumentParser(description=__description(), usage=__usage())
    parser.add_argument(
        '-s', '--service', default='crunchyroll', help="generate using the specified service"
    )
    parser.add_argument(
        '-u', '--username', help="service username"
    )
    parser.add_argument(
        '-p', '--password', help="service password"
    )
    return parser


def __print_program_end() -> None:
    print("-----------------------------------")
    print("End of execution")
    print("-----------------------------------")


def __init_app(parameters: Parameters) -> None:
    if parameters.service is not None:
        # app.vrv.start_app()
        pass
    else:
        print()
        print("For instructions on how to use this program, please run:\nmanage.py --help")


if __name__ == '__main__':
    cli_args = __init_cli().parse_args()
    __parameters = Parameters(
        cli_args.service,
        cli_args.username,
        cli_args.password
    )
    __init_app(__parameters)
