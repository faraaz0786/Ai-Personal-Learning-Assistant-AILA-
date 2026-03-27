import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt test placeholder.")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--task", choices=["explain", "quiz", "flashcards"])
    args = parser.parse_args()
    print(f"Prompt test scaffold ready. all={args.all} task={args.task}")


if __name__ == "__main__":
    main()
