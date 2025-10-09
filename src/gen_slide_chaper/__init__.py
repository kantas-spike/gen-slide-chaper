import argparse
import logging
import os
import subprocess

logging.basicConfig(level=logging.DEBUG)


def get_script_path_for_blender():
    return os.path.join(os.path.dirname(__file__), "blender", "__init__.py")


def parse_args(args=None) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    DEFAULT_BLENDER_PATH = "/usr/local/bin/blender"
    parser.add_argument(
        "--blender",
        default=DEFAULT_BLENDER_PATH,
        help=f"実行するBlenderコマンド. デフォルト: {DEFAULT_BLENDER_PATH}",
    )
    return parser.parse_known_args(args)


def main() -> None:
    logger = logging.getLogger(__name__)
    args, remaining = parse_args()

    cli_args = [
        args.blender,
        "-P",
        get_script_path_for_blender(),
        "--",
    ] + remaining

    logger.debug(f"cli_args: {cli_args}")

    result = subprocess.run(cli_args)
    return result.returncode
