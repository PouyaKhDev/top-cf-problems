import shutil


def show_menu(menu: list, greeting: bool):
    width = shutil.get_terminal_size(fallback=(80, 20)).columns

    if greeting:
        print("Welcome to Codeforces problem extractor.".center(width))
        print("Enter -1 anytime to go back.".center(width))
        print("Choose an option [1-3]:\n")

    for i in range(0, len(menu)):
        print(f"{i+1}_ {menu[i]}")
    print("\n")
