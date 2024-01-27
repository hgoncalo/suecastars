import random,time
values_constants = {'A':11,'7':10,'K':4,'J':3,'Q':2,'2':0,'3':0,'4':0,'5':0,'6':0}
suits = ('♣️','♠️','♥️','♦️')
#TODO : Fix error that changes partners mid-games / Improve AI play

def screen(players,played,deck,trump,suit_played):
    screen = [f"{'ㅤ'*len(players[1]) + players[0]} | [{played['0']}]",'',f"{players[1]} | [{played['1']}] ㅤㅤㅤㅤㅤㅤ{players[3]} | [{played['3']}]",'',f"{'ㅤ'*len(players[1]) + players[2]} | [{played['2']}]"]
    print()
    print()
    print('Current Game:')
    print(f"Trump: {trump}")
    print(f"Played suit: {suit_played}")
    print(f"Your deck: {deck[0]}")
    print()
    for line in screen:
        print(line)
    pass

def decks():
    cards = []
    deck = []
    trump = random.choice(suits)
    for card in values_constants.keys():
        for suit in suits:
            cards.append(suit + card)
    random.shuffle(cards)
    for i in range(0,len(cards),10):
        deck.append(cards[i:i+10])
    #se menos de 10 pontos e sem trunfos, então pode desistir
    return deck,trump

def main(seed2):
    random.seed(seed2)
    names = ('Leonard','Sheldon','Howard','Raj','Penny','Bernadette','Amy','Ted','Barney','Marshall','Robin','Lily','Will','Geoffrey','Carlton','Vivian','Ashley','Phil','Hilary')
    chosen_names = random.sample(names,3)
    player1 = str(input('Write your username here: '))
    print('Setting the table...')
    time.sleep(3)
    print()
    print()
    print()
    print()
    players = (player1,chosen_names[0],chosen_names[1],chosen_names[2])
    print(f"The teams are: TEAM 1 [{players[0]},{players[2]}] and TEAM 2 [{players[1]},{players[3]}]")
    return players


def play_rounds(seed2,i=0):
    deck_return = decks()
    deck = deck_return[0]
    trump = deck_return[1]
    players = main(seed2)
    played = {'0':'','1':'','2':'','3':''}
    starter = 0
    team1_points = team2_points = 0
    screen(players,played,deck,trump,'None')
    while i<10:
        if i==0:
            rp = round(starter,players,deck,trump,played)
        else:
            rp = round(next_starter,players,new_deck,trump,played)
        new_deck = rp[3]
        next_starter = rp[2]
        team1_points += rp[0]
        team2_points += rp[1]
        played = {'0':'','1':'','2':'','3':''}
        i += 1
    return team1_points,team2_points

def victories():
    team1_victories = team2_victories = 0
    seed2 = random.choice([1,100])
    while (team1_victories or team2_victories)<4:
        points = play_rounds(seed2)
        #debugging
        print(points[0],points[1])

        if points[0] > points[1]:
            print(f"Team 1 won the round!")
            team1_victories += 1
        elif points[1] > points[0]:
            print(f"Team 2 won the round!")
            team2_victories += 1
        else: #it was a tie
            print(f"A tie occured!")
            continue
        print(f"Current result: TEAM 1 {team1_victories} vs {team2_victories} TEAM 2")
        print()
    if team1_victories==4:
        return f"Team 1 won the game!"
    else:
        return f"Team 2 won the game!"
    
def round(starter,players,deck,trump,played):
    #starter means its his/hers turn
    team1_points = team2_points = turns = winner = 0
    highest_card = '♦️6'
    possible = []
    possible_t = []
    others = []
    while turns<4: #4 turns
        if starter == 0: #if player0 turn
            prompt = int(input(f"Choose the index of the card you want to play (starting at index 0): "))
            selected = deck[0][prompt]
            try:
                if turns == 0: #it's the first turn
                    played[str(starter)] = selected
                    suit_played = str(selected[0])
                    deck[starter].pop(deck[starter].index(selected))
                else:
                    if selected[0] == suit_played:
                        pass
                    else:
                        if selected[0] != suit_played: #could be trump or other card
                            for card in deck[starter]: #verify if player is 'resigning'
                                if card[0] == suit_played:
                                    raise Exception #resigned 
                    played[str(starter)] = selected
                    deck[starter].pop(deck[starter].index(selected))
            except: #impossible choice
                print(f"You tried a illegal move, you lose.")
                exit(1)
        else: #player1,player2,player3 (bots)
            if turns==0: #it's the first turn
                selected = random.choice(deck[starter])
                played[str(starter)] = selected
                suit_played = str(selected[0])
                deck[starter].pop(deck[starter].index(selected))     
            else:
                for card in deck[starter]:
                    if card[0] == suit_played: #check if there are any possible cards
                        possible.append(card)
                    elif card[0] == trump: #check for trumps
                        possible_t.append(card)
                    else:
                        others.append(card)
                if len(possible) > 0:
                    possible_sorted = sorted(possible, key=lambda x:values_constants[x[2]],reverse=True) #sort by value
                    selected = random.choice(possible_sorted)
                elif len(possible) == 0 and len(possible_t) > 0:
                    possible_t_sorted = sorted(possible_t, key=lambda x:values_constants[x[2]])
                    if random.choice([1,2,3]) == 1:
                        selected = random.choice(possible_t_sorted)
                    else:
                        selected = random.choice(others)
                else:
                    selected = random.choice(deck[starter])
                played[str(starter)] = selected 
                deck[starter].pop(deck[starter].index(selected)) 

        starter = (starter+1)%4
        screen(players,played,deck,trump,suit_played)
        print() #go to the next player
        possible = []
        possible_t = []
        others = []
        turns += 1
        time.sleep(1)

    for j in range(4):
        if (j==0 or j==2):
            team1_points += values_constants[played[str(j)][2]]
        else:
            team2_points += values_constants[played[str(j)][2]]

    for p in played:
        if played[p]==played['0']:
            if played[p][0] == suit_played:
                highest_card = played[p]
                winner = p
            else:
                pass
        else:
            if played[p][0] == highest_card[0]: #if card is from the same suit
                if values_constants[played[p][2]] > values_constants[highest_card[2]]:
                    highest_card = played[p]
                    winner = p
            else:
                if played[p][0] == trump:
                    if highest_card[0] == trump:
                        if values_constants[played[p][2]] > values_constants[highest_card[2]]:
                            highest_card = played[p]
                            winner = p
                    else:
                        highest_card = played[p]
                        winner = p
                else:
                    pass
                
    return team1_points,team2_points,int(winner),deck

victories()