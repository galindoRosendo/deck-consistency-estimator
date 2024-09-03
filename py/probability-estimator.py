#Yugioh probability estimator that takes Prosperity, Desires, Upstart, Extravagance, Duality into account
#Can copy all this into https://www.online-python.com/online_python_compiler or another online compiler if you don't want to learn how to download python.


#In input_cards_here: Enter card name *space* quantity, then hit enter. Leave no spaces in card names
#After the quantity, you can write other names the card can by. For instance, things it directly/indirectly searches...
#or something like Monster or TriBrigadeMonster etc if you have some combos that can use any card of that type.
#Certain draw/excavation cards have their effects built in. Write Desires, Prosperity, Extravagance, Upstart, Duality as the names for those cards

#For input_possibilities_heare, list the acceptable combinations of cards in hand. Follow the syntax in the example
#For example 2 + A AND 1 - B AND 0 = C means "2 or more of A, 1 or fewer of B, exactly 0 of C
#Instead of 1 + A, you can just write A. So the first line means "1 or more Fluffal and 1 or more Edge and 1 or more poly"
#Each line represents a different acceptable combination of cards in hand

#Final line is the number of trials

#outputs the estimated probability you get one of these desired combinations

deck_size = 40
hand_size = 5
input_cards_here="""
FirstPlaceHolder 3
SecondPlaceHolder 3
"""
input_possibilities_here="""
FirstPlaceHolder AND SecondPlaceHolder
"""
num_trials=10000

#Below is the actual code; can ignore


from itertools import product
import random
import sys

def empty_deck(n):
	deck=[]
	for i in range(0, n):
		deck.append("blank")
	return deck


def add_card(deck, name, quantity):
	for i in range(0, quantity):
		del deck[0]
		deck.append(name)
	return deck

def get_hand(deck, k, num_extras):
	for i in range(0,k+num_extras):
		rand=random.randint(i,len(deck)-1)
		temp=deck[rand]
		deck[rand]=deck[i]
		deck[i]=temp
	hand=[]
	extras=[]
	for i in range(0,k):
		hand.append(deck[i])
	for i in range(k,k+num_extras):
		extras.append(deck[i])
	return([hand,extras])

def hand_comb(hand):
	cats=[]
	for c in hand:
		if c!="blank":
			cats.append(card_hash[c])
	return product(*cats)


def is_valid(hand, condition):
	for cond in condition:
		card=cond[0]
		sign=cond[2]
		num=0
		for c in hand:
			if c==card:
				num+=1
		if num<cond[1] and sign!="-":
			return False
		if num>cond[1] and sign!="+":
			return False
	return True

def is_one_valid(hand,possibilities):
	combs = hand_comb(hand)
	for comb in combs:
		for p in possibilities:
			if is_valid(comb,p):
				return True
	return False

def is_one_valid_draw(hand,extras,possibilities,can_extrav,can_desires,can_upstart,can_prosperity,can_duality):
	if is_one_valid(hand,possibilities):
		return True
	if can_desires and "Desires" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(temp_extras.pop())
		temp_hand.append(temp_extras.pop())
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,can_upstart,False,can_duality):
			return True
	if can_extrav and "Extravagance" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(temp_extras.pop())
		temp_hand.append(temp_extras.pop())
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,False,False,can_duality):
			return True
	if can_prosperity and "Prosperity" in hand:
		for i in range(0,6):
			temp_hand=hand.copy()
			temp_extras=extras.copy()
			temp_hand.append(temp_extras[i])
			del temp_extras[0:6]
			if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,False,False,can_duality):
				return True
	if can_upstart and "Upstart" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(temp_extras.pop())
		temp_hand.remove("Upstart")
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,can_desires,can_upstart,False,can_duality):
			return True
	if can_duality and "Duality" in hand:
		for i in range(0,3):
			temp_hand=hand.copy()
			temp_extras=extras.copy()
			temp_hand.append(temp_extras[i])
			del temp_extras[0:3]
			if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,can_desires,can_upstart,can_prosperity,False):
				return True
	return False

card_hash = dict()
deck=empty_deck(deck_size)
all_cats=[]
deck_count=0
num_extras=0
cardlines=input_cards_here.splitlines()
cardlines.pop(0)
for cardline in cardlines:
	s=cardline.split(" ")
	#catch int error here
	try:
		deck=add_card(deck,s[0],int(s[1]))
	except:
		print("Error in input_cards_here, check line "+cardline)
		sys.exit(0)
	deck_count+=int(s[1])
	all_cats.append(s[0])
	if s[0]=="Upstart":
	    num_extras+=int(s[1])
	card_cats=[]
	card_cats.append(s[0])
	for i in range(2, len(s)):
		card_cats.append(s[i])
		if s[i] not in all_cats:
			all_cats.append(s[i])
	card_hash[s[0]]=card_cats
if "Prosperity" in deck or "Extravagance" in deck:
    num_extras+=6
if "Duality" in deck:
    num_extras+=3
if "Desires" in deck:
    num_extras+=2
if deck_count>deck_size:
	print("Inputted cards: "+str(deck_count)+". Exceeds deck size: "+str(deck_size))
	sys.exit(0)

possibilities=[]
text_possibilities=input_possibilities_here.splitlines()
text_possibilities.pop(0)
for possibility in text_possibilities:
	if len(possibility)==0:
		continue
	conditions=[]
	text_conditions=possibility.split("AND")
	for condition in text_conditions:
		parts=condition.split()
		if len(parts)==3:
			if parts[2] not in all_cats:
				print("Possibility: " +possibility+ " contains unlisted card or category "+ parts[2])
				sys.exit(0)
			if parts[1] not in ['-','+','='] or not parts[0].isdigit():
				print("Check formatting of line: "+possibility)
				sys.exit(0)
			conditions.append([parts[2],int(parts[0]),parts[1]])
		elif len(parts)==1:
			if parts[0] not in all_cats:
				print("Possibility: " +possibility+ " contains unlisted card or category "+ parts[0])
				sys.exit(0)			
			conditions.append([parts[0], 1, '+'])
		else:
			print("Check formatting of input_possibilities_here, line: "+possibility)	
	possibilities.append(conditions)

counter=0
for i in range(0,num_trials):
	hand=get_hand(deck,hand_size, num_extras)
	if is_one_valid_draw(hand[0],hand[1],possibilities,True,True,True,True,True):
		counter+=1
print("probability of success: "+ str(counter/num_trials*100)+"%")