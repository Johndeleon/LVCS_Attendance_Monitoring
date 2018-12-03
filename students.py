import amarissedb
import os

menuItems = [
    { "Search Student": bar },
    { "Exit": exit },
]

def main():
    while True:
        os.system('cls')
        for option in menuItems:
            print(option)
        

main()