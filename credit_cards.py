from credit_card_object import CreditCard
import pickle
from datetime import datetime
import os

def load_credit_cards():
    credit_cards = []
    for file in os.listdir('credit_cards'):
        if file.endswith('pkl'):
            with open('credit_cards/'+file, 'rb') as handle:
                cc = pickle.load(handle)
                credit_cards.append(cc)
    return credit_cards

def askYesOrNo(message):
    while (True):
        answer = input(message)
        if (answer[0].lower() == 'y'): return True
        elif (answer[0].lower() == 'n'): return False
        else: print("Invalid Yes or No answer, try again.")

def modify_info_of_card(card_obj):
    actions = [
        'update_bank_name',
        'update_alias_name',
        'update_cut_date',
        'update_last_four_digits'
    ]
    cstr = ""
    for i, a in enumerate(actions):
        cstr += '\n'+str(i)+') '+a
    decision = input("""
What whould you like to do? """+cstr+"""

Enter the action to be taken: """)

    chosen_action = actions[int(decision)]

    if chosen_action == 'update_bank_name':
        issuing_bank = input("Enter the name of the issuing bank of the card: ")
        card_obj.update_bank_name(str(issuing_bank))

    elif chosen_action == 'update_alias_name':
        alias_name = input("Enter the alias you would like to use for this card: ")
        card_obj.update_alias_name(str(alias_name))

    elif chosen_action == 'update_cut_date':
        while True:
            cut_day = input('Enter the day of the month when the card cuts : ')
            try:
                cut_day = int(cut_day)
            except ValueError:
                raise ValueError('Invalid day, day must be a number')
            if cut_day > 31 or cut_day < 1:
                raise ValueError('Invalid month day, day must be between 1 and 31')
            card_obj.update_cut_date(cut_day)
            break

    elif chosen_action == 'update_last_four_digits':
        while True:
            last_four = input("Enter the last 4 digits of this card: ")
            try:
                int(last_four)
            except ValueError:
                raise ValueError('Invalid input, must be a four digit number')
            if len(last_four) != 4:
                raise ValueError('Invalid input, must be a four digit number')
            card_obj.update_last_four_digits(str(last_four))
            break
    else:
        raise ValueError('Invalid decision')

    # Save card object as pickle
    with open('credit_cards/{0}.pkl'.format(card_obj.alias_name), 'wb') as handle:
        pickle.dump(card_obj, handle)

    print('Done, data was updated successfully')

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

    while True:
        last_four = input("Enter the last 4 digits of this card: ")
        try:
            int(last_four)
        except ValueError:
            raise ValueError('Invalid input, must be a four digit number')
        if len(last_four) != 4:
            raise ValueError('Invalid input, must be a four digit number')
        credit_card.update_last_four_digits(str(last_four))
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
            credit_cards = load_credit_cards()
            ccs_str = ""
            for i, cc in enumerate(credit_cards):
                ccs_str += '\n'+str(i)+') '+cc.alias_name
                #print(i, cc.alias_name)
            while True:
                chosen_cc = input("""
I have this cards registered:"""+ccs_str+"""

Enter the number of the card you want to modify: """)
                try:
                    chosen_cc = int(chosen_cc)
                    if chosen_cc < 0 or chosen_cc > len(credit_cards) + 1:
                        print("Sorry, not available")
                    elif chosen_cc < len(credit_cards):
                        # credit
                        cc = credit_cards[chosen_cc]
                        modify_info_of_card(cc)
                        break
                except ValueError:
                    print("Sorry, not available")
            
        elif int(response) == 3:
            print("Sorry, not supported yet, about to come.")
        elif int(response) == 4:
            break
        else:
            print("That is not a supported answer.")
            
        cont = askYesOrNo("Would you like to do something else? ")
        if not cont:
            break



