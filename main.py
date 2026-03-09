from app.presentation.main_menu_controller import main_menu


def main():
    try:
        main_menu()
        print("Exiting the app...")
    except Exception as e:
        print(e)
        main()


if __name__ == '__main__':
    main()
