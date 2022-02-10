

def show_menu(menu: list) -> int:
    for i in range(len(menu)):
        print(f"{i + 1}. {menu[i]}")
    print('0. Выход')
    choose = int(input('>>> '))

    return choose

