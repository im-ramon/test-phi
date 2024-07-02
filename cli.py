import argparse


def cli():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Clean the database.")
    args = parser.parse_args()

    if args.delete:
        print("Test CLI")
        print("✨ Clearing Database")
    else:
        print("Test CLI")
        print("🚀 Populating Database")


if __name__ == "__main__":
    cli()
