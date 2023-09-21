"""
A menu - you need to add the database and fill in the functions. 
"""

from peewee import *

# define the database
db = SqliteDatabase('jugglers.sqlite')

# define the Juggler model
class Juggler(Model):
    name = CharField()
    country = CharField()
    catches = IntegerField()

    # use the jugglers.sqlite database
    class Meta:
            database = db

    def __str__(self):
            return f'{self.name}, {self.country}, {self.catches}'

# connect to the database and create the tables
db.connect()
db.create_tables([Juggler])

# clear the database before adding data
Juggler.delete().execute()

# add dummy data
janne = Juggler(name='Janne Mustonen', country='Finland', catches=98)
janne.save()

ian = Juggler(name='Ian Stewart', country='Canada', catches=94)
ian.save()

aaron = Juggler(name='Aaron Gregg', country='Canada', catches=88)
aaron.save()

# menu function
def main():
    menu_text = """
    1. Display all records
    2. Search by name
    3. Add new record
    4. Edit existing record
    5. Delete record 
    6. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_record()
        elif choice == '4':
            edit_existing_record()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():

    # get all jugglers in the database and print them
    jugglers = Juggler.select()
    for juggler in jugglers:
        print(juggler)

def search_by_name():
    juggler_name = input('Enter name: ')

    # match the name with the juggler
    juggler_match = Juggler.select().where(Juggler.name.contains(juggler_name))

    # if a juggler is found, print his name, otherwise print an error message
    if juggler_match:
        for juggler in juggler_match:
            print(juggler)
    else:
        print('Not found')

def add_new_record():
    juggler_name = input('Enter name: ')

    # use get_or_none to see if the juggler exists
    # this could be done more elegantly, time permitting
    juggler_exists = Juggler.get_or_none(name=juggler_name)

    # if the juggler already exists, print an error message
    if juggler_exists is not None:
        print('Juggler already exists')
    
    # otherwise ask for country and number of catches, add to the database and print a confirmation
    else:
        juggler_country = input('Enter country of origin: ')
        juggler_catches = input('Enter number of catches: ')
        juggler = Juggler(name=juggler_name, country=juggler_country, catches=juggler_catches)
        juggler.save()
        print('Juggler added.')

def edit_existing_record():
    juggler_name = input('Enter name: ')
    juggler_exists = Juggler.get_or_none(name=juggler_name)

    # if juggler not found, print an error message
    if juggler_exists is None:
        print('Juggler not found')

    # otherwise, ask for the new information, update the database and print the entries again to show the changes
    # an improvement would be to get the new entry and print just that to demonstrate it had been added
    else:
        juggler_new_name = input('Enter new name: ')
        juggler_new_country = input('Enter new country: ')
        juggler_new_catches = input('Enter new catch count: ')

        Juggler.update(name=juggler_new_name, country=juggler_new_country, catches=juggler_new_catches).where(Juggler.name.contains(juggler_name)).execute()

        jugglers = Juggler.select()
        for juggler in jugglers:
            print(juggler)

def delete_record():
    juggler_name = input('Enter name: ')
    juggler_exists = Juggler.get_or_none(name=juggler_name)

    if juggler_exists is None:
        print('Juggler not found')

    # if the name is found, delete the record from the database and reprint the entries
    else:
        Juggler.delete().where(Juggler.name.contains(juggler_name)).execute()
        jugglers = Juggler.select()
        for juggler in jugglers:
            print(juggler)

if __name__ == '__main__':
    main()
