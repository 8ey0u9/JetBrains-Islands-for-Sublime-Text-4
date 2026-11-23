"""Build, check, test and regenerate Islands resources through one entry point."""
import argparse
import subprocess
import sys

from lib import ROOT


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="regenerate resources and build the development archive")
    build.add_argument("--release-ready", action="store_true", help="also require completed publication review")
    check = commands.add_parser("check", help="validate sources and the existing archive without modifying them")
    check.add_argument("--source-only", action="store_true", help="check sources without requiring an archive")
    check.add_argument("--release-ready", action="store_true", help="also require completed publication review")
    commands.add_parser("test", help="run all regression tests")
    icons = commands.add_parser("icons", help="regenerate recorded icons and attribution metadata")
    icons.add_argument("--check", action="store_true", help="compare with checked-in icons without modifying them")
    args = parser.parse_args(argv)

    if args.command == "test":
        return subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT
        ).returncode
    if args.command == "icons":
        from lib.icons import build
        build(check=args.check)
    else:
        from lib import package
        if args.command == "build":
            package.build(release_ready=args.release_ready)
        else:
            package.check(source_only=args.source_only, release_ready=args.release_ready)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
