from credit_card_object import CreditCard
import pickle
from datetime import datetime

def askYesOrNo(message):
    while (True):
        answer = input(message)
        if (answer[0].lower() == 'y'): return True
        elif (answer[0].lower() == 'n'): return False
        else: print("Invalid Yes or No answer, try again.")


def register_new_card():
    print("All right !!, we are abought to register a new credit card, how fun.")
    print(" ")

    credit_card = CreditCard()

    issuing_bank = input("Enter the name of the issuing bank of the card: ")
    credit_card.update_bank_name(str(issuing_bank))

    alias_name = input("Enter the alias you would like to use for this card: ")
    credit_card.update_alias_name(str(alias_name))

    while True:
        cut_day = input('Enter the day of the month when the card cuts : ')
        try:
            cut_day = int(cut_day)
        except ValueError:
            raise ValueError('Invalid day, day must be a number')
        if cut_day > 31 or cut_day < 1:
            raise ValueError('Invalid month day, day must be between 1 and 31')
        credit_card.update_cut_date(cut_day)
        break

    # Save card object as pickle
    with open('credit_cards/{0}.pkl'.format(alias_name), 'wb') as handle:
        pickle.dump(credit_card, handle)

    print(" ")
    print("Cool! a new card was registered correctly.")

if __name__ == "__main__":
    # execute only if run as a script
    while True:
        response = input("""
What would you like to do ? 
    1) Register a new card
    2) Modify a card
    3) Delete a card
    4) Nothing, just leave

your response: """)

        if int(response) == 1:
            register_new_card()
        elif int(response) == 2:
            print("Sorry, not supported yet, about to come.")
        elif int(response) == 3:
            print("Sorry, not supported yet, about to come.")
        elif int(response) == 4:
            break
        else:
            print("That is not a supported answer.")
            
        cont = askYesOrNo("Would you like to do something else? ")
        if not cont:
            break



