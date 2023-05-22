import deck
import hand
import sys
from textwrap import dedent
from collections import namedtuple

def get_int(prompt_text = '', range = None, error_text = None):
    if error_text != None:
        print(error_text + '\n')
    try:
        the_int = int(input(prompt_text))
    except ValueError:
        return get_int(prompt_text, range, "Invalid input: enter a whole number (no decimal).")
    if (range != None and the_int >= range[0] and the_int <= range[1]) or range == None:
        return the_int
    else:
        return get_int(prompt_text, range, f"Invalid input: enter a number within {range[0]} and {range[1]}")



def get_float(prompt_text = '', range = None, error_text = None):
    if error_text != None:
        print(error_text + '\n')
    try:
        the_float = float(input(prompt_text))
    except ValueError:
        return get_float(prompt_text, range, "Invalid input: enter a number (it can have a decimal).")
    if range != None and the_float >= range[0] and the_float <= range[1]:
        return the_float
    else:
        return get_float(prompt_text, range, f"Invalid input: enter a number within {range[0]} and {range[1]}")



def initialize():
    should_start = get_int("""Welcome to Sears' sketchy blackjack >:) Are you ready to play?
        1: Yes
        2: No
        """, (1, 2))
    if should_start == 1:
        pass
    else:
        print("Alright. Bye.")
        sys.exit()

    nosd = get_int("\nHow many standard (52-card) decks do you want the dealer to use?\n\t")
    the_deck = deck.Deck(nosd)

    min_bet = get_float("What will be the minimum bet at your table?\n\t", (0.01, 100))
    bet = get_float("You have $100 to start with. How much of that do you want to bet?\n\t", (min_bet, 100))
    wallet = 100.0

    return (the_deck, nosd, wallet, min_bet, bet)



def deal(the_deck):
    players_hand = hand.Hand()
    dealers_hand = hand.Hand()

    for i in range(0, 2):
        players_hand.add(the_deck.popCard())
    for i in range(0, 2):
        dealers_hand.add(the_deck.popCard())

    print(dedent(f"""
        Your hand: {players_hand.getInfo(0)}, {players_hand.getInfo(1)}
        Dealer shows: {dealers_hand.getInfo(0)}
        """))

    return(the_deck, players_hand, dealers_hand)

def hit(the_deck, players_hand):
    players_hand.add(the_deck.popCard())
    players_hand.switchAce()

def insurance(dealers_hand, players_hand):
    print(dedent("""
    The dealer shows an Ace, which means you can place an insurance bet.
    (An insurance bet is half of your first bet.)
    If you place this bet and the dealer has a Blackjack,
    the dealer will win, but you won't lose any money.
    If the dealer does not have blackjack, you will lose the insurance bet.
    """))
    insurance = get_float(""" Would you like to place an insurance bet?
    1: Yes
    2: No
    """, (1, 2))
    if insurance == 1:
        if dealers_hand.getTotalNumValue() == 21:
            print(f"Dealer's hole card: {dealers_hand.getInfo(1)}—blackjack!")
            if  players_hand.getTotalNumValue() != 21:
                print(f"You lose the round, but get your money back.")
                players_hand.outcome = "insurance"
            elif players_hand.getTotalNumValue() == 21:
                print("Push!")
                players_hand.outcome == "push"
        else:
            print("The dealer does not have a natural blackjack. You will lose your insurance bet.")
            insurance_bet = players_hand.bet / 2
    else:
        return None

def split(the_deck, players_hand):
    new_players_hand = hand.Hand()
    new_players_hand.add(players_hand.popCard())
    new_players_hand.bet = players_hand.bet
    hit(the_deck, players_hand)
    hit(the_deck, new_players_hand)
    print(dedent(f"""
    Hand 1: {players_hand.getInfo(0)}, {players_hand.getInfo(1)}
    Hand 2: {new_players_hand.getInfo(0)}, {new_players_hand.getInfo(1)}
    """))
    return [players_hand, new_players_hand]



def play_a_hand(the_deck, players_hand, wallet):
    wants_to_continue = True
    while (players_hand.getTotalNumValue() <= 21) and (wants_to_continue == True):

        #Give them their options
        input = get_int("""\nWhat do you want to do?
        1: Hit
        2: Stand
        3: Surrender
        4: Double Down
        5: Quit
        """, (1, 5))
        #Evaluate their decision
        if input == 1:
            hit(the_deck, players_hand)
            print(f"\n{players_hand.getInfo(-1)}\n")
        elif input == 2:
            wants_to_continue = False
        elif input == 3:
            wants_to_continue = False
            players_hand.outcome = "surrender"
        elif input == 4:
            if wallet >= players_hand.bet * 2:
                players_hand.bet *= 2
                hit(the_deck, players_hand)
                print(f"\n{players_hand.getInfo(-1)}\n")
                wants_to_continue = False
            else:
                print("\nYou don't have enough $ to double down :/\n")
        else:
            print("\nOk. See ya later!\n")
            sys.exit()

def play_a_round(the_deck, bet, wallet):

    #Deal the players, unpack the results, attach 'bet' to the player's hand
    the_deal = deal(the_deck)
    the_deck = the_deal[0]
    players_hand = the_deal[1]
    players_hands = [players_hand]
    dealers_hand = the_deal[2]
    players_hand.bet = bet

    #See if the player has a natural
    if players_hand.getTotalNumValue() == 21:
        print("Blackjack!!")
        players_hand.outcome = "blackjack"
    #Offer the insurance bet, if the situation demands it
    insurance_bet = None
    if dealers_hand.getFaceValue(0) == "Ace":
        if wallet < players_hand.bet / 2:
            print("Insufficient $ for an insurance bet—the game will continue.")
        else:
            insurance_bet = insurance(dealers_hand, players_hand)
            if players_hand.outcome == "insurance":
                return (the_deck, players_hands, insurance_bet)
            elif players_hand.outcome == "push":
                return (the_deck, players_hands, insurance_bet)
            else:
                pass
    #Evaluate any natural the player might have been dealt, or move on
    if players_hand.getTotalNumValue() == 21 and dealers_hand.getTotalNumValue() != 21:
        print("You win!")
        return (the_deck, players_hands, None)
    elif players_hand.getTotalNumValue() == dealers_hand.getTotalNumValue() == 21:
        players_hand.outcome == "push"
        return (the_deck, players_hands, None)
    else:
        pass


    #Handle splitting:
    #If it's possible, and they have the $, offer the player the chance to split
    if players_hand.getNumValue(0) == players_hand.getNumValue(1) and wallet >= players_hand.bet * 2:
        should_split = get_int("""Do you want to split your hand? You can only do this once.
        1: Yes
        2: No
        """)
        if should_split == 1:
            players_hands = split(the_deck, players_hand)
    #Or if they're almost broke...
    elif players_hand.getNumValue(0) == players_hand.getNumValue(1) and wallet < players_hand.bet * 2:
        print("\nYou don't have enough $ to split—the game will continue.\n")
    #Or, most of the time, just keep moving
    else:
        pass

    #Play each players_hand (usually there is only one)
    dealer_should_play = False
    for num, players_hand in enumerate(players_hands, 1):
        if len(players_hands) > 1:
            print(f"\nHand {num}: {players_hand.getInfo(0)}, {players_hand.getInfo(1)}")
        play_a_hand(the_deck, players_hand, wallet)
        if len(players_hands) > 1 and players_hand.getTotalNumValue() > 21:
            print("\nBust!!\n")
        if players_hand.outcome == None and players_hand.getTotalNumValue() <= 21:
            dealer_should_play = True

    #If at least one hand isn't a bust or surrendered, the dealer plays
    if dealer_should_play:
        print(f"\nDealers hand: {dealers_hand.getInfo(0)}, {dealers_hand.getInfo(1)}")
        #Dealer plays according to the usual algorithm, hits on soft 16s
        while dealers_hand.getTotalNumValue() < 17:
            results = hit(the_deck, dealers_hand)
            print(f"Dealer takes a hit: {dealers_hand.getInfo(-1)}")

    #for num ,players_hand in enumerate(players_hands, 1):
        #if len(players_hands) > 1:
            #print(f"\nHand {num}:\n")
        #evaluateHand(players_hand, dealers_hand)

    return (the_deck, players_hands, dealers_hand, insurance_bet)

def evaluateHand(players_hand, dealers_hand):
    if (players_hand.getTotalNumValue() > 21):
        print("Bust!!")
        players_hand.outcome = "lost"
    elif (dealers_hand.getTotalNumValue() > 21):
        print("Dealer busts—you win!!")
        players_hand.outcome = "won"
    elif dealers_hand.getTotalNumValue() < players_hand.getTotalNumValue() <= 21:
        print(dedent(f"""
        Congrats, you win!!!
        Dealer's Hand: {dealers_hand.getTotalNumValue()},
        Your Hand: {players_hand.getTotalNumValue()}"""))
        players_hand.outcome = "won"
    elif dealers_hand.getTotalNumValue() == players_hand.getTotalNumValue():
        print(dedent(f"""
        Push!
        Dealer's Hand: {dealers_hand.getTotalNumValue()},
        Your Hand: {players_hand.getTotalNumValue()}"""))
        players_hand.outcome = "push"
    else:
        print(dedent(f"""
        Sorry, you lose!
        Dealer's Hand: {dealers_hand.getTotalNumValue()},
        Your Hand: {players_hand.getTotalNumValue()}"""))
        players_hand.outcome = "lost"

def evaluatePayout(players_hand, wallet):
    if players_hand.outcome == "lost":
        wallet -= players_hand.bet
        print(f'You lost ${players_hand.bet}. You have ${wallet} left.')
    elif players_hand.outcome == "surrender":
        wallet += players_hand.bet /2
        print(f'Surrender—you forfeit ${players_hand.bet/2}. You have ${wallet} left.')
        #Includes pushing an insurance bet
    elif players_hand.outcome == "push":
        print(f'You get your original bet back. You have ${wallet} in total.')
    elif players_hand.outcome == "insurance":
        print(f'You have ${wallet} in total.')
    elif players_hand.outcome == "won":
        wallet += players_hand.bet
        print(f'You won ${players_hand.bet}! You have ${wallet} in total.')
    #Payout for natural blackjacks
    else:
        wallet += 1.5 * players_hand.bet
        print(f'You won ${players_hand.bet * 1.5}! You have ${wallet} in total.')
    return wallet

def full_game(initialize_info):
    #Unpack info from the initializing process
    the_deck = initialize_info[0]
    nosd = initialize_info[1]
    wallet = initialize_info[2]
    min_bet = initialize_info[3]
    bet = initialize_info[4]

    #Place the user in a betting/evaluation loop
    wants_to_play = True
    while wants_to_play:
        last_round_results = play_a_round(the_deck, bet, wallet)
        #Unpack the results from the last round
        the_deck = last_round_results[0]
        players_hands = last_round_results[1]
        dealers_hand = last_round_results[2]
        insurance_outcome = last_round_results[3]

        #If any insurance_outcome was passed, it was the insurance bet they lost
        if insurance_outcome != None:
            wallet -= insurance_outcome
            print(f"You lost ${insurance_outcome} from the insurance bet.")

        #Evaluate the results of the round
        for num ,players_hand in enumerate(players_hands, 1):
            if len(players_hands) > 1:
                print(f"\nHand {num}:")
            evaluateHand(players_hand, dealers_hand)
            wallet = evaluatePayout(players_hand, wallet)
        #If they aren't broke, see if they want to continue
        if wallet > 0:
            input = get_int("\nContinue?\n\t1: Yes\n\t2: No\n\t")
            if input == 1:
                bet = get_float("\nIt's time for the next round. How much do you want to bet?\n\t", (min_bet, wallet))
            else:
                wants_to_play = False
                print("\nOk, see ya later!\n")
        #Otherwise, show them the door...XD
        else:
            print("You're broke, buddy. Better luck next time!")
            wants_to_play = False


full_game(initialize())
