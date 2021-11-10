import argparse
import sys
from gtin import (
    calculate_check_digit,
    validate_check_digit,
    has_valid_check_digit,
    append_check_digit,
    get_gcp,
    GTIN,
)


def _get_command() -> str:
    command: str = ""
    if len(sys.argv) > 1:
        command = sys.argv.pop(1).lower().replace("_", "-")
    return command


def _calculate_check_digit() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gtin calculate-check-digit",
        usage=(
            "gtin calculate-check-digit [-h] GTIN\n"
            "       gtin ccd [-h] GTIN"
        ),
    )
    parser.add_argument(
        "GTIN",
        type=str,
        help="A GTIN without the check-digit",
    )
    arguments: argparse.Namespace = parser.parse_args()
    print(calculate_check_digit(arguments.GTIN))


def _append_check_digit() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gtin append-check-digit",
        usage=(
            "gtin append-check-digit [-h] [-l LENGTH] GTIN\n"
            "       gtin acd [-h] [-l LENGTH] GTIN"
        ),
    )
    parser.add_argument(
        "GTIN",
        type=str,
        help="A GTIN without the check-digit",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=0,
        help="The length of GTIN to return",
    )
    arguments: argparse.Namespace = parser.parse_args()
    if arguments.length:
        print(str(GTIN(raw=arguments.GTIN, length=arguments.length)))
    else:
        print(append_check_digit(arguments.gtin))


def _validate_check_digit() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gtin validate-check-digit",
        usage=(
            "gtin validate-check-digit [-h] GTIN\n" "       gtin vcd [-h] GTIN"
        ),
        description=(
            "If the provided GTIN is *invalid*, this command will terminate "
            "with a non-zero exit status."
        ),
    )
    parser.add_argument(
        "GTIN",
        type=str,
        help="A GTIN *with* check-digit",
    )
    arguments: argparse.Namespace = parser.parse_args()
    validate_check_digit(arguments.GTIN)


def _has_valid_check_digit() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gtin has-valid-check-digit",
        usage=(
            "gtin has-valid-check-digit [-h] GTIN\n"
            "       gtin hvcd [-h] GTIN"
        ),
        description=(
            "If the provided GTIN is *valid*, this command will return "
            '"YES". If the provided GTIN is *invalid*, this command will '
            'return "NO".'
        ),
    )
    parser.add_argument(
        "GTIN",
        type=str,
        help="A GTIN *with* check-digit",
    )
    arguments: argparse.Namespace = parser.parse_args()
    print("YES" if has_valid_check_digit(arguments.GTIN) else "NO")


def _get_gcp() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="gtin get-gcp",
        usage=("gtin get-gcp [-h] GTIN\n" "       gtin gcp [-h] GTIN"),
    )
    parser.add_argument(
        "GTIN",
        type=str,
        help="A GTIN *with* check-digit",
    )
    arguments: argparse.Namespace = parser.parse_args()
    print(get_gcp(arguments.GTIN))


def main() -> None:
    command: str = _get_command()
    if command in ("ccd", "calculate-check-digit"):
        _calculate_check_digit()
    elif command in ("acd", "append-check-digit"):
        _append_check_digit()
    elif command in ("vcd", "validate-check-digit"):
        _validate_check_digit()
    elif command in ("hvcd", "has-valid-check-digit"):
        _has_valid_check_digit()
    elif command in ("gcp", "get-gcp"):
        _get_gcp()


if __name__ == "__main__":
    main()
