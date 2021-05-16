import argparse


def setup_args():
    parser = argparse.ArgumentParser()
    # app args
    parser.add_argument(
        "-H",
        "--host",
        help="Enter the ip of the server on which it will be launched, only the string is accepted: '0.0.0.0'",
        type=str,
        default="0.0.0.0",
    )
    parser.add_argument(
        "-P",
        "--port",
        help="Enter the port of the server on which it will run: port 3000",
        type=int,
        default=3000,
    )
    parser.add_argument(
        "-D", "--debug", help="on debug mode True | default: False", action="store_true"
    )
    # database args
    parser.add_argument(
        "--no_env",
        help="By explicitly specifying the --no_env flag, you will not use the. env settings.",
        action="store_false",
    )
    parser.add_argument(
        "--pg-url",
        help="postgres url",
        type=str,
        default="postgresql://admin:admin@0.0.0.0:5442/simalend",
    )

    return parser.parse_args()
