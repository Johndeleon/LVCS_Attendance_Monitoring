import amarissedb
import os

def search():
    print('die')

menuItems = [
    "Search Student",
    "Exit"
]

def main():
    while True:
        os.system('cls')
        i=1
        for item in menuItems:
            print('[',i,']',item)
            i+=1
        choice = input('Enter Number of Choice >> ')
        try:
            

main()