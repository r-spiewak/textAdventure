''' let's see...
 I can make a game like the example.
 First I should ask the player's name. 
 Then I will tell player they wake up in a room and see two doors, red and blue.
 Red door has dragon, fire hurts X hp.
 Out of hp -> game over.
 Blue door has maybe a chest and a guard gyarding another door. Maybe can check guard to see he is sleepong, or something.
 Should keep track of hp, and can always cgeck hp or check health to see how much is left. Maybe can gwt armor to multiply current remaining health and full health amounts, and potions to replenish.
 Can check guard or dragon to also see their health?
 Can talk to dragon and stuff, maybe its friendly? Maybe can actually have conversations, and not just single lines of speech?
 Maybe use method 'Ask dragon about key' (or equivalent 'talk to' and 'speak to'), and use 'key' as the key in a special speech keyval (and there's a default value if no 'about' given)? And a default 'I'm sorry, I don't know anything about a key.' for an unknown extra object. First noun will respond, second noun will be subject of response. And I guess the speech keyval will be fed in as an option to the character decalaration.
 Maybe there should be traps, like pitfalls, in some of the rooms for an automatic loss? Maybe not, I don't really likr automatic losses, only losses because the player did something stupid...
 Also attack power, ans better swords as multipliers.
 Check inventory or items. Also, inspect, look at. 
 Can drop items in random rooms too?
 Enemies can drop items?
 Python class for characters and enemies, but hide enemy inventory from being checked (until they are defeated)
 Python class for items, imcludimg the type and if equipped (one item of each type can be equipped at a time) 
 Maybe Character class can havevan Equip method, which calls an Equip method of the item, and checks if there is already an item of that type equipped?
 Pythom class for doors. Enter or go through doors. Check doors for keys or puzzles?
 Run or flee to go back to oreviousvrooms.
 Handle unrecognized commands.
 Maybe include some puzzles to solve also?
 Locks can be puzzles to solve.
 Maybe also need to find keys in other rooms.
'''

'''
Color names:
	
white
pearl
alabaster
snow
ivory
cream
eggshell
cotton
chiffon
salt
lace
coconut
linen
bone
daisy
powder
frost
porcelain
parchment
rice

tan
beige
macaroon
hazelwood
granola
oat
eggnog
fawn
sugar cookie
sand
sepia
ltte
oyster
biscotti
parmesan
hazelnut
sandcastle
buttermilk
sand dollar
shortbread

yellow
canary
gold
daffodil
flaxen
butter
lemon
mustard
corn
medallion
dandelion
fire
bumblebee
banana
butterscotch
dijon
honey
blonde
pineapple
tuscan sun

orange
tangerine
marigold
cider
rust
ginger
tiger
fire
bronze
cantaloupe
apricot
clay
honey
carrot
squash
spice
marmalade
amber
sandstone
yam

red
cherry
rose
jam
merlot
garnet
crimson
ruby
scarlet
wine
brick
apple
mahogany
blood
sangria
berry
currant
blush
candy
lipstick

pink
rose
fuchsia
punch
blush
watermelon
flamingo
rouge
salmon
coral
peach
strawberry
rosewood
lemonade
taffy
bubblegum
ballet slipper
crepe
magenta
hot pink

purple
mauve
violet
boysenberry
lavender
plum
magenta
lilac
grape
periwinkle
sangria
eggplant
jam
iris
heather
amethyst
raisin
orchid
mulberry
wine

blue
slate
sky
navy
indigo
cobalt
teal
ocean
peacock
azure
cerulean
lapis
spruce
stone
aegean
berry
denim
admiral
sapphire
arctic

green
chartreuse
juniper
sage
lime
fern
olive
emerald
pear
moss
shamrock
seafoam
pine
parakeet
mint
seaweed
pickle
pistachio
basil
crocodile

brown
coffee
mocha
peanut
carob
hickory
wood
pecan
walnut
caramel
gingerbread
syrup
chocolate
tortilla
umber
tawny
brunette
cinnamon
penny
cedar

grey
shadow
graphite
iron
pewter
cloud
silver
smoke
slate
anchor
ash
porpoise
dove
fog
flint
charcoal
pebble
lead
coin
fossil

black
ebony
crow
charcoal
midnight
ink
raven
oil
grease
onyx
pitch
soot
sable
jet black
coal
metal
obsidian
jade
spider
leather

'''

import sys, getopt
from . import Character
from . import Adventurer
from . import TextImages
from . import Door
from . import Room
import re
from . import Lock
import string
import random
from . import Item
from . import Puzzle
from . import Potion
from . import Chest

debug=0

def codeGen(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
def shuffle(array):
	random.shuffle(array)
	return array

#TextImages.print_game_over()

def gameOver():
	TextImages.print_game_over()
	sys.exit()
	return
def youWin():
	print("Daylight streams through a large hole in the opposite wall.")
	print("You climb through the hole in the wall into the daylight.")
	print("You made it outside!")
	print("You found a way out of the dungeon!")
	TextImages.print_victory()
	sys.exit()
	return
def quitGame():
	confirmQuit=0
	while not confirmQuit:
		var=input("Do you really want to quit the game?\n>")
		var=var.lower()
		if var[0]=='y':
			gameOver()
			confirmQuit=1
			sys.exit()
		elif var[0]=='n':
			confirmQuit=1
			return
		else:
			print("I'm sorry, I didn't catch that. Please try again.")
			confirmQuit=0

def parse(text,dict,keyvals,currRoom):
	textList=text.lower().split()
	#can maybe try to parse the words for their types, e.g., verb, noun, adjective...
	#maybe just have different lists for the different types of expected words (verbs->commands, some nouns + adjectives->objects, other nound->arguments)?
	#Also make sure to check for duplicate entries in the string, and reject the string if duplicates
	#Also reject it if not given commamd or attribute (maybe not attribute though, since check red door shoukd be ok...)
	'''for st in textList:
		print(st)'''
	object='adventurer'
	subject=None
	command=None
	adjective=None
	attribute=None
	argument=None #attribute?
	#argument=[]
	verbCount=0
	objCount=0
	subjCount=0
	adjCount=0
	attribCount=0
	if len(textList)<1:
		print("I'm sorry, I did not recieve your input. Please try again.")
		inputAccepted=0
	#elif textList[0] in dict:
		#print("Do ",textList[0])
		#inputAccepted=1
	else:
		for word in range(0,len(textList)):
			if textList[word] in ['quit']:
				quitGame()
			elif textList[word] in dict[0]:#verb
				if textList[word] == 'go' and len(textList)>word+1 and textList[word+1] in ['in','into','through','back','to']:
					command=' '.join([textList[word],textList[word+1]])
					verbCount+=1
					word+=1
				elif textList[word]=='attack' and len(textList)>word+1 and textList[word+1]=='power':
					argument=' '.join([textList[word],textList[word+1]])
					attribCount+=1
				#elif textList[word] in ['talk,']
				elif textList[word]=='put' and len(textList)>word+1 and textList[word+1] in ['down','on']:
					command=' '.join([textList[word],textList[word+1]])
					verbCount+=1
				elif textList[word]=='put' and ((len(textList)>word+2 and textList[word+2] in ['in']) or (len(textList)>word+3 and textList[word+3] in ['in'])):
					command='give'
					verbCount+=1
				elif textList[word]=='pick' and len(textList)>word+1 and textList[word+1] in ['up','on']:
					command=' '.join([textList[word],textList[word+1]])
					verbCount+=1
				elif textList[word]=='take' and len(textList)>word+1 and textList[word+1] in ['out']:
					command=' '.join([textList[word],textList[word+1]])
					verbCount+=1
				else:
					command=textList[word]
					verbCount+=1
			elif textList[word] in dict[1]:#objects
				if command in ['ask','talk','speak','say'] and not object=='adventurer':
					subject=textList[word]
					argument=subject
					subjCount+=1
				elif command in ['give','get','take','pick up']:
					object='adventurer'
					if debug: print(textList[word])
					if textList[word] in dict[5]:
						if debug: print(object)
						if textList[word] in ['amulet']:
							key=textList[word]
						else:
							key=''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])
						if debug: print(key)
						if key not in keyvals:
							print("Please use an adjective to describe the {}.".format(textList[word]))
							inputAccepted=0
							return inputAccepted,object,command,adjective,attribute,argument
						if debug: print(argument)
						if not argument:
							argument=[None,None]
						#this is the item
						#	argument[0]=keyvals[textList[word]]
						if not argument[0]:
							argument[0]=keyvals[key]
						else:
							argument[1]=keyvals[key]
						if not argument[1]:
							argument[1]=currRoom
						if debug: print(argument)
					else:
						if not argument:
							argument=[None,None]
						argument[1]=keyvals[textList[word]]
						if debug: print(argument)
				elif command in ['equip','wear','put on','take out','unequip']:
					if textList[word] in dict[5]:
						if debug: print(object)
						if textList[word] in ['amulet']:
							key=textList[word]
						else:
							key=''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])
						if key not in keyvals:
							print("Please use an adjective to describe the {}.".format(textList[word]))
							inputAccepted=0
							return inputAccepted,object,command,adjective,attribute,argument
						argument=keyvals[key]
						#object='adventurer'
						#object=textList[word]
						#object=''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])
				elif command in ['check','inspect','go to','approach']:
					if textList[word] in dict[5]:
						#argument=keyvals[''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])]
						#object='adventurer'
						#object=textList[word]
						if debug: print(object)
						if textList[word] in ['amulet']:
							object=textList[word]
						else:
							object=''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])
						argument=object
					else:
						object=textList[word]
						objCount+=1
				#elif command in ['take','pick up']:
				#	if textList[word] in dict[5]:
				#		if not argument:
				#			argument=[None,None]
				#		argument[0]=keyvals[''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])]
				#		argument[1]=currRoom
				#		#object=textList[word]
				#		#objCount+=1
				#	else:
				#		if not argument:
				#			argument=[None,None]
				#		argument[1]=keyvals[textList[word]]
				else:
					object=textList[word]
					objCount+=1
					if textList[word] in dict[5]:
						if debug: print(object)
						if textList[word] in ['amulet']:
							key=textList[word]
						else:
							key=''.join([textList[word-1],textList[word][0].upper(),textList[word][1:]])
						if key not in keyvals:
							print("Please use an adjective to describe the {}.".format(textList[word]))
							inputAccepted=0
							return inputAccepted,object,command,adjective,attribute,argument
						if command in ['drink']:
							object=key
							if debug: print(object)
							argument=keyvals['adventurer']
							inputAccepted=1
							return inputAccepted,object,command,adjective,attribute,argument
						if not argument:
							argument=[None,None]
						if command in ['take','give'] and textList[word] in ['chest']:
							argument[1]=keyvals[key]
						argument[0]=keyvals[key]
						if not argument[1]:
							argument[1]=currRoom
			elif textList[word] in dict[2]:#adjectiv
				if command in ['ask','talk','speak','say'] and not object=='adventurer':
					subject=textList[word]
					argument=subject
					subjCount+=1
				else:
					adjective=textList[word]
					adjCount+=1
			elif textList[word] in dict[3]:#attribute
				argument=textList[word]
				attribute=textList[word]
				attribCount+=1
		if verbCount==1 and objCount<=1 and adjCount<=1 and attribCount<=1 and subjCount<=1:
			inputAccepted=1
		elif verbCount<1:
			print("I'm sorry, I didn't catch that verb. Please try again.")
			inputAccepted=0
		elif verbCount==1 and objCount<=1 and adjCount<=2 and attribCount<=1 and subjCount<=1:
			if command in ['take','give'] and textList[word] in ['chest']:
				inputAccepted=1
			else:
				print("Something is wrong...")
		elif verbCount>1 or objCount>2 or adjCount> 2 or attribCount>1 or subjCount>1:
			print("verbs:",verbCount,"objs:",objCount,"adjs:",adjCount,"attribs:",attribCount,"subjs:",subjCount)
			print("I'm sorry, you have specified too many things. Please try them one thing at a time.")
			inputAccepted=0
		else:
			print("I'm sorry, I did not recognize your input. Please try again.")
			inputAccepted=0
	return inputAccepted,object,command,adjective,attribute,argument
	
def sanitize(adventurer,currRoom,dict,keyvals,adjective,attribute,object,command,argument):
	if command in ['check','inspect','go to','approach']:
		command='check'
	elif command in ['talk','speak','ask','say']:
		command='talk'
		if not argument:
			argument='default'
	elif command in ['wake']:
		command='wake'
	elif command in ['attack','slay','kill','fight']:
		command='attack'
	elif command in ['enter','go through','go into','go in']:
		command='enter'
	elif command in ['unlock']:
		command='unlock'
		argument=adventurer
	elif command in ['open']:
		command='open'
	elif command in ['exit','leave','run','flee','go back']:
		command='exitRoom'
		object='room'
	elif command in ['take','pick up','get']:
		command='take'
	elif command in ['drop','put down']:
		command='drop'
	elif command in ['equip','put on','wear','take out']:
		command='equip'
	elif command in ['unequip']:
		command='unequip'
	elif command in ['give']:
		command='give'
	elif command in ['drink']:
		command='drink'
	else:
		print("Did not properly sanitize command",command)
		return None,None
	if object in ['adventurer',adventurer.name,'self','me']:
		object='adventurer'
	elif object in ['door']:
		object='door'
	elif object in ['chest']:
		object='chest'
	elif object in ['lock']:
		#object='lock'
		#key=''.join()
		if adjective+'Door' in keyvals:
			object='door'
		elif adjective+'Chest' in keyvals:
			object='chest'
		else:
			print("Something is wrong in sanitizing the lock!")
	elif object in ['dragon']:
		object='dragon'
	elif object in ['guard']:
		object='guard'
	elif object in ['princess']:
		object='princess'
	elif object in ['thief']:
		object='thief'
	elif object in ['goblin']:
		object='goblin'
	elif object in ['ogre']:
		object='ogre'
	elif object in ['zombie']:
		object='zombie'
	elif object in ['troll']:
		object='troll'
	elif object in ['gremlin']:
		object='gremlin'
	elif object in ['orc']:
		object='orc'
	elif object in ['room']:
		object=currRoom.name
	elif object in ['sword','key']:
		if command not in ['check']:
			object='adventurer'
	elif object in dict[5]:
		if command not in ['check','drink']:
			object='adventurer'
		elif command in ['drink']:
			argument=adventurer
	else:
		print("Did not properly sanitize object",object)
		return None,None
	if object=='door':
		if adjective:
			object=adjective+'Door'
		else: 
			print("Please include an adjective describing the door.")
			return None,None
		if command=='open' or command=='enter':
			command=command+'Door'
	if object=='lock':
		if adjective:
			object=adjective+'Lock'
		else: 
			print("Please include an adjective describing the door or chest on which the lock resides.")
			return None,None
	if object=='chest':
		if adjective:
			object=adjective+'Chest'
			if command=='open':
				argument=[dict,keyvals]
		else: 
			print("Please include an adjective describing the chest.")
			return None,None
	if command=='check' and object!='adventurer' and not adjective and not attribute:
		argument=object
	func='.'.join([object,command])
	return func,argument
    	
def mergeDict(dict1,dict2):
	for ii in range(0,len(dict1)):
		dict1[ii].extend(dict2[ii])
	return

def main(debug):
  allArgs=sys.argv
  inputArgs=allArgs[1:]
  shortOpts="d"
  longOpts=["debug"]
  try:
  	args,values = getopt.getopt(inputArgs,shortOpts,longOpts)
  except getopt.error as err:
  	print(str(err))
  	sys.exit(2)
  for currArg,currVal in args:
  	if currArg in ("-d","--debug"):
  		print("Starting in debug mode.")
  		debug=1
  firstdict=[['check','inspect','approach'],[],[],[],[],[]]#verbs,objects,adjectives,attributes,extra words for verbs like go or attack,items
  firstkeyvals={}
  adventurer=Adventurer.Adventurer(hideInventory=0)
  #dict.extend(adventurer.dict)
  mergeDict(firstdict,adventurer.dict)
  #firstkeyvals['adventurer.check']=adventurer.check
  firstkeyvals=adventurer.keyvals
  print("Welcome, Adventurer!")
  adventurer.name=input("What is your name?\n> ")
  #dict.append(adventurer.name)
  #mergeDict(dict[1],adventurer.name)
  firstdict[1].append(adventurer.name)
  #print(dict)
  TextImages.print_dungeon()
  print("Welcome to the dungeon, {}!".format(adventurer.name))
  print("You wake up alone in a strange room with no memory of how you got here.")
  #make door objects. add door statuses and actions and stuff to dict. add door functions for what comes in the next room.
  #dict.append('open')
  initialRoom=Room.room(dict=firstdict,keyvals=firstkeyvals)
  redRoom=Room.room(name='redRoom',prev=initialRoom,dict=firstdict,keyvals=firstkeyvals)
  #make the purple code randomly generated 5 or so alphanumeric characters
  #purpleCode='1A2B3C4D5E'
  purpleCode=codeGen()
  purpleNote=Item.item(name='purpleNote',takeable=1,status=0,itemType='note',attack=0,defense=0,inventory=None,hasInventory=0,message="It's a purple note, on which is written the following message:\n''One of these should be the code for the lock on the purple door:\n{}\n{}\n{}\n{}\n{}''".format(*shuffle([purpleCode,codeGen(),codeGen(),codeGen(),codeGen()])))
  #Oh, the lock on that green door? It is very old and will likely crumble at the slightest touch.'
  dragonsNote=Item.item(name='dragonsNote',takeable=1,status=0,itemType='note',attack=0,defense=0,inventory=None,hasInventory=0,message='{}'.format(purpleCode))
  dragon=Character.Character(name='dragon',hideInventory=1,health=1000,attack=200,description='Dragon',speech={'default': 'Hello! This is unusual. Adventurers do not usually talk to me.', 'red': 'Oh, the red door? I think you figured that one out already, considering you went through it to get here.', 'blue': 'Oh, the lock on that green door? It is very old and will likely crumble at the slightest touch.', 'green': 'Oh, the lock on that green door? I think there is a key for it in one of these rooms.', 'purple': 'Oh, you want to know the code for the lock on the purple door? Since you asked so nicely and you seem like a nice person, I will tell you: It is {}. And, actually, here is a note on which I have written it down for you.'.format(purpleCode), 'yellow': 'A yellow door? I do not recall there being a yellow door. Maybe it is new.', 'orange': 'Oh, the orange door? Arithmetic is necessary to solve that puzzle.','teal': 'Oh, the lock on that teal door? I think there is a key for it in one of these rooms.', 'black': '...', 'rusty': 'Oh, the rusty door? I am a bit rusty on that one too.','out': 'Oh, you seek a way out from the dungeon? I think in the room behind the purple door there may be a hole in the wall just big enough for you to squeeze through.' },inventory=[dragonsNote])
  redRoom.addContents(dragon)
  greenRoom=Room.room(name='greenRoom',prev=redRoom,dict=firstdict,keyvals=firstkeyvals)
  greenDoor=Door.door(name='greenDoor',status=2,room=greenRoom)
  purpleLock=Lock.lock(name='purpleLock',lockType=1,code=purpleCode)
  purpleRoom=Room.room(name='purpleRoom',prev=redRoom,dict=firstdict,keyvals=firstkeyvals)
  purpleRoom.dict[1].append('outside')
  purpleDoor=Door.door(name='purpleDoor',status=2,lock=purpleLock,room=purpleRoom)
  redRoom.addContents(greenDoor)
  #redRoom.addContents(purpleDoor)
  redDoor=Door.door(name='redDoor',room=redRoom)
  initialRoom.addContents(redDoor)
  #dict.extend(redDoor.dict)
  #mergeDict(dict,redDoor.dict)
  #keyvals['redDoor.check']=redDoor.check
  #keyvals['redDoor.unlock']=redDoor.unlock
  #keyvals['redDoor.openDoor']=redDoor.openDoor
  #keyvals['redDoor.enterDoor']=redDoor.enterDoor
  #keyvals['redDoor.attack']=redDoor.attack
  blueRoom=Room.room(name='blueRoom',prev=initialRoom,dict=firstdict,keyvals=firstkeyvals)
  rustySword=Item.item(name='rustySword',takeable=1,status=0,itemType='sword',attack=5,defense=0,inventory=None,hideInventory=0)
  greenKey=Item.item(name='greenKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hideInventory=0)
  greenLock=Lock.lock(name='greenLock',lockType=2,key=greenKey)
  greenDoor.lock=greenLock
  blueRoom.addContents(rustySword)
  blueRoom.addContents(greenKey)
  blueLock=Lock.lock(name='blueLock',lockType=0)
  blueDoor=Door.door(name='blueDoor',status=2,room=blueRoom,lock=blueLock)
  orangePotion=Potion.potion(name='orangePotion')
  orangePuzzle=Puzzle.puzzle(name='orangePuzzle',puzzleType=0,iters=3)
  orangeRoom=Room.room(name='orangeRoom',prev=blueRoom,dict=firstdict,keyvals=firstkeyvals)
  orangeRoom.addContents(orangePotion)
  #initialRoom.addContents(orangePotion)
  orangeLock=Lock.lock(name='orangeLock',lockType=3,puzzle=orangePuzzle)
  orangeDoor=Door.door(name='orangeDoor',status=2,lock=orangeLock,room=orangeRoom)
  blueRoom.addContents(orangeDoor)
  rustyHelmet=Item.item(name='rustyHelmet',takeable=1,status=0,itemType='helmet',attack=0,defense=5,inventory=None,hideInventory=0)
  greenRoom.addContents(rustyHelmet)
  tealKey=Item.item(name='tealKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hideInventory=0)
  tealLock=Lock.lock(name='tealLock',lockType=2,key=tealKey)
  tealRoom=Room.room(name='tealRoom',prev=blueRoom,dict=firstdict,keyvals=firstkeyvals)
  tealDoor=Door.door(name='tealDoor',lock=tealLock,status=2,room=tealRoom)
  rustyShield=Item.item(name='rustyShield',takeable=1,status=0,itemType='shield',attack=0,defense=5,inventory=None,hideInventory=0)
  tealRoom.addContents(rustyShield)
  rustyArmor=Item.item(name='rustyArmor',takeable=1,status=0,itemType='armor',attack=0,defense=25,inventory=None,hideInventory=0)
  tealRoom.addContents(rustyArmor)
  greenRoom.addContents(tealKey)
  rustyPuzzle=Puzzle.puzzle(name='rustyPuzzle',puzzleType=2,clue='Only those weathered like me are granted passage.',answer='rusty')
  rustyLock=Lock.lock(name='rustyLock',lockType=3,puzzle=rustyPuzzle)
  rustyRoom=Room.room(name='rustyRoom',prev=orangeRoom,dict=firstdict,keyvals=firstkeyvals)
  rustyDoor=Door.door(name='rustyDoor',status=2,lock=rustyLock,room=rustyRoom)
  rustyRoom.addContents(purpleDoor)
  orangeRoom.addContents(rustyDoor)
  blueRoom.addContents(tealDoor)
  ironSword=Item.item(name='ironSword',takeable=1,status=0,itemType='sword',attack=50,defense=0,inventory=None,hasInventory=0)
  silverRoom=Room.room(name='silverRoom',prev=tealRoom,dict=firstdict,keyvals=firstkeyvals)
  silverKey=Item.item(name='silverKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hasInventory=0)
  silverLock=Lock.lock(name='silverLock',lockType=2,key=silverKey)
  silverDoor=Door.door(name='silverDoor',status=2,lock=silverLock,room=silverRoom)
  guard=Character.Character(name='guard',inventory=[],hideInventory=1,attack=305,health=320,description='guard',speech={'default': 'I have no time to talk. I must protect the princess and recover her stolen amulet.', 'foundamulet': 'What? You found the thief and recovered the stolen amulet?!?! You must take this gold key and go give return the amulet to the princess right away!'})
  silverRoom.addContents(guard)
  greyKey=Item.item(name='greyKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hasInventory=0)
  obliteratorSword=Item.item(name='obliteratorSword',takeable=1,status=0,itemType='sword',attack=3000,defense=0,inventory=None,hasInventory=0)
  platinumKey=Item.item(name='platinumKey',takeable=1,status=0,itemType='key',attack=0,defense=0,hasInventory=None)
  princess=Character.Character(name='princess',hideInventory=1,inventory=[obliteratorSword,platinumKey],attack=3005,health=3020,description='Princess',speech={'default': 'Hello! It is nice to see a friendly face down here in this dingy dungeon. I hope we find my amulet soon so we can leave.', 'amulet': 'My amulet was stolen, and we think the theif is hiding here somewhere. There will be a great reward for whoever finds it.', 'amuletthanks': 'Thank you so much for returning my amulet! Please take this obliterator sword as a reward.'})
  amulet=Item.item(name='amulet',takeable=1,itemType='amulet',attack=0,defense=0,hasInventory=0)
  thief=Character.Character(name='thief',hideInventory=1,inventory=[amulet],attack=200,health=450,description='Thief',speech={'default': 'I will find a way out and escape those who pursue me, and I will defeat anyone who gets in my way!'})
  #initialRoom.addContents(amulet)
  goldKey=Item.item(name='goldKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hasInventory=0)
  guard.addInventory(goldKey)
  goldRoom=Room.room(name='goldRoom',prev=silverRoom,dict=firstdict,keyvals=firstkeyvals)
  goldLock=Lock.lock(name='goldLock',lockType=2,key=goldKey)
  goldDoor=Door.door(name='goldDoor',status=2,lock=goldLock,room=goldRoom)
  goldRoom.addContents(princess)
  silverRoom.addContents(goldDoor)
  greyKey=Item.item(name='greyKey',takeable=1,status=0,itemType='key',attack=0,defense=0,inventory=None,hasInventory=0)
  greyRoom=Room.room(name='greyRoom',prev=tealRoom,dict=firstdict,keyvals=firstkeyvals)
  greyRoom.addContents(ironSword)
  greyLock=Lock.lock(name='grayLock',lockType=2,key=greyKey)
  greyDoor=Door.door(name='greyDoor',status=2,lock=greyLock,room=greyRoom)
  tealRoom.addContents(greyDoor)
  tealRoom.addContents(silverDoor)
  goblin=Character.Character(name='goblin',hideInventory=1,health=30,attack=20,description='Goblin',speech={'default': 'Oh, a yummy adventurer! I will eat you for breakfast!'},activity='sleeping',inventory=[greyKey])
  tealRoom.addContents(goblin)
  #greyRoom.addContents(purpleNote)
  woodenChest=Chest.chest(name='woodenChest')
  ironShield=Item.item(name='ironShield',takeable=1,status=0,itemType='shield',attack=0,defense=400,inventory=None,hasInventory=0)
  #woodenChest.addInventory(ironShield)
  #initialRoom.addContents(woodenChest)
  #initialRoom.addContents(silverKey)
  #maroonRoom.addContents(silverKey)
  #dict.extend(blueDoor.dict)
  initialRoom.addContents(blueDoor)
  #mergeDict(dict,blueDoor.dict)
  #keyvals['blueDoor.check']=blueDoor.check
  #keyvals['blueDoor.unlock']=blueDoor.unlock
  #keyvals['blueDoor.openDoor']=blueDoor.openDoor
  #keyvals['blueDoor.enterDoor']=blueDoor.enterDoor
  #keyvals['blueDoor.attack']=blueDoor.attack
  #initialRoom=1
  #currRoom=initialRoom
  # More keys
  brownKey=Item.item(name='brownKey',takeable=1,status=0,itemType='key',attack=0,defense=0,hasInventory=None)
  oliveKey=Item.item(name='oliveKey',takeable=1,status=0,itemType='key',attack=0,defense=0,hasInventory=None)
  pinkKey=Item.item(name='pinkKey',takeable=1,status=0,itemType='key',attack=0,defense=0,hasInventory=None)
  woodenKey=Item.item(name='woodenKey',takeable=1,status=0,itemType='key',attack=0,defense=0,hasInventory=None)
  # More locks
  salmonPuzzle=Puzzle.puzzle(name='salmonPuzzle',puzzleType=1,clue="What has it gots in its pocketses?",answer="ring")
  salmonLock=Lock.lock(name='salmonLock',lockType=3,puzzle=salmonPuzzle)
  platinumLock=Lock.lock(name='platinumLock',lockType=2,key=platinumKey)
  pinkLock=Lock.lock(name='pinkLock',lockType=2,key=pinkKey)
  oliveLock=Lock.lock(name='oliveLock',lockType=2,key=oliveKey)
  brownLock=Lock.lock(name='brownLock',lockType=2,key=brownKey)
  # More rooms
  brownRoom=Room.room(name='brownRoom',prev=redRoom,dict=firstdict,keyvals=firstkeyvals)
  oliveRoom=Room.room(name='oliveRoom',prev=brownRoom,dict=firstdict,keyvals=firstkeyvals)
  pinkRoom=Room.room(name='pinkRoom',prev=brownRoom,dict=firstdict,keyvals=firstkeyvals)
  cyanRoom=Room.room(name='cyanRoom',prev=pinkRoom,dict=firstdict,keyvals=firstkeyvals)
  salmonRoom=Room.room(name='salmonRoom',prev=pinkRoom,dict=firstdict,keyvals=firstkeyvals)
  maroonRoom=Room.room(name='maroonRoom',prev=greenRoom,dict=firstdict,keyvals=firstkeyvals)
  lavenderRoom=Room.room(name='lavenderRoom',prev=greenRoom,dict=firstdict,keyvals=firstkeyvals)
  whiteRoom=Room.room(name='whiteRoom',prev=orangeRoom,dict=firstdict,keyvals=firstkeyvals)
  platinumRoom=Room.room(name='platinumRoom',prev=whiteRoom,dict=firstdict,keyvals=firstkeyvals)
  # More doors
  salmonDoor=Door.door(name='salmonDoor',status=2,lock=salmonLock,room=salmonRoom)
  brownDoor=Door.door(name='brownDoor',status=2,lock=brownLock,room=brownRoom)
  oliveDoor=Door.door(name='oliveDoor',status=2,lock=oliveLock,room=oliveRoom)
  pinkDoor=Door.door(name='pinkDoor',status=2,lock=pinkLock,room=pinkRoom)
  cyanDoor=Door.door(name='cyanDoor',status=0,room=cyanRoom)
  maroonDoor=Door.door(name='maroonDoor',status=0,room=maroonRoom)
  lavenderDoor=Door.door(name='lavenderDoor',status=1,room=lavenderRoom)
  whiteDoor=Door.door(name='whiteDoor',status=0,room=whiteRoom)
  platinumDoor=Door.door(name='platinumDoor',status=2,lock=platinumLock,room=platinumRoom)
  # More items 
  ironHelmet=Item.item(name='ironHelmet',takeable=1,status=0,itemType='helmet',attack=0,defense=100,inventory=None,hasInventory=0)
  ironArmor=Item.item(name='ironArmor',takeable=1,status=0,itemType='armor',attack=0,defense=100,inventory=None,hasInventory=0)
  longSword=Item.item(name='longSword',takeable=1,status=0,itemType='sword',attack=100,defense=0,inventory=None,hasInventory=0)
  broadSword=Item.item(name='broadSword',takeable=1,status=0,itemType='sword',attack=200,defense=0,inventory=None,hasInventory=0)
  greenPotion=Potion.potion(name='greenPotion')
  redPotion=Potion.potion(name='redPotion',attack=20)
  purplePotion=Potion.potion(name='purplePotion')
  bluePotion=Potion.potion(name='bluePotion')
  # More characters
  ogre=Character.Character(name='ogre',hideInventory=1,health=230,attack=60,description='Ogre',inventory=[pinkKey,ironShield])
  orc=Character.Character(name='orc',hideInventory=1,health=130,attack=30,description='Orc',activity='sleeping',inventory=[longSword,bluePotion])
  # Fill in details and connections
  #orangeRoom.addContents(oliveKey)
  woodenChest.addInventory(ironHelmet)
  woodenChest.addInventory(ironArmor)
  pinkRoom.addContents(broadSword)
  cyanRoom.addContents(thief)
  salmonRoom.addContents(redPotion)
  brownRoom.addContents(ogre)
  oliveRoom.addContents(purplePotion)
  #pinkRoom.addContents(broadSword)
  maroonRoom.addContents(silverKey)
  maroonRoom.addContents(woodenChest)
  lavenderRoom.addContents(orc)
  lavenderRoom.addContents(oliveKey)
  whiteRoom.addContents(greenPotion)
  whiteRoom.addContents(woodenKey)
  platinumRoom.addContents(purpleNote)
  redRoom.addContents(brownKey)
  redRoom.addContents(brownDoor)
  brownRoom.addContents(oliveDoor)
  brownRoom.addContents(pinkDoor)
  pinkRoom.addContents(cyanDoor)
  pinkRoom.addContents(salmonDoor)
  greenRoom.addContents(maroonDoor)
  greenRoom.addContents(lavenderDoor)
  orangeRoom.addContents(whiteDoor)
  whiteRoom.addContents(platinumDoor)
  # Now play the game!
  currRoom,dict,keyvals=initialRoom.enterRoom()
  currRoom.seeRoom()
  while initialRoom:
  	#print("You see two doors: a red door and a blue door.")
  	#currRoom=initialRoom
  	#dict,keyvals=initialRoom.enterRoom()
  	# Now call a function which parses the inpit and does the appropriate action.
  	#print(dict)
  	inputAccepted=0
  	while not inputAccepted:
  	  inputAccepted,object,command,adjective,attribute,argument=parse(input("> "),dict,keyvals,currRoom)
    	#print("Do: ",' '.join([adjective,object,command,argument]))
  	  if debug: print("inputAccepted:",inputAccepted)
  	  if debug: print("Do: ",adjective,attribute,object,command,argument)
  	  if debug: print(currRoom,dict)
  	  if inputAccepted:
  	  	try:
    			#(object).(command)(argument) #invalid syntax
    			#pass
    			#print("Do: ",' '.join([adjective,object,command,argument]))
    			func,argument=sanitize(adventurer,currRoom,dict,keyvals,adjective,attribute,object,command,argument)
    			if debug: print(func,argument)
    			#if object=='door':
    				#object=adjective+'Door'
    				#print(object,exec('%s'%(object)),type(exec('%s'%(object))))
    			#func=getattr(exec(object),command,None)
    			#print("func=%s.%s"%(object,command))
    			#exec("func=%s.%s"%(object,command))
    			#print(func)
    			#func(arguments)
    			#func='.'.join([object,command])
    			if debug: print(func)
    			if func not in keyvals:
    				#res=re.findall('[a-zA-Z][^A-Z]*',func.split('.')[0])
    				#if len(res)>1:
    					#res=' '.join(res)
    				print("There is no {} here...".format(' '.join(re.findall('[a-zA-Z][^A-Z]*',func.split('.')[0])).lower()))
    			elif func and argument != None:
    				#print("Has arg.")
    				#print(func.split('.'))
    				if func.split('.')[1] in ['enterRoom']:
    					currRoom,dict,keyvals=keyvals[func](argument)
    					#print("Room:",currRoom.name,"Contents:",currRoom.contents)
    				elif func.split('.')[1] in ['open'] and len(re.findall('[a-zA-Z][^A-Z]*',func.split('.')[0]))>1 and re.findall('[a-zA-Z][^A-Z]*',func.split('.')[0])[1].lower() in ['chest']:
    					dict,keyvals=keyvals[func](argument)
    				else:
    					if debug: print("Got here.")
    					keyvals[func](argument)
    					if debug: print(func,argument)
    					if func.split('.')[0]=='dragon' and func.split('.')[1]=='talk' and argument=='purple':
    						argument=[dragonsNote,currRoom]
    						dragon.drop(argument)
    					elif func.split('.')[0]=='guard' and func.split('.')[1]=='talk' and amulet in adventurer.inventory:
    						guard.talk('foundamulet')
    						argument=[goldKey,currRoom]
    						guard.drop(argument)
    					#elif func.split('.')[0]=='princess' and func.split('.')[1]=='talk' and amulet in adventurer.inventory:
    					#	argument=[amulet,princess]
    					#	adventurer.give(argument)
    					#	princess.talk('amuletthanks')
    						#princess.speech('amulet')=princess.speech('amuletthanks')
    					#	argument=[obliteratorSword,currRoom]
    					#	princess.drop(argument)
    					elif func.split('.')[1]=='give' and argument[0]==amulet and argument[1]==princess:
    						if debug: print("In here.")
    						princess.talk('amuletthanks')
    						princess.speech['amulet']=princess.speech['amuletthanks']
    						argument=[obliteratorSword,currRoom]
    						princess.drop(argument)
    			elif func:
    				#print(func.split('.'))
    				#print(func.split('.')[1])
    				#print(func.split('.')[1] in ['enterDoor','enterRoom','exitRoom'])
    				if func.split('.')[1] in ['enterDoor','enterRoom','exitRoom']:
    					#print("Changing room...")
    					#print(keyvals)
    					currRoom,dict,keyvals=keyvals[func](currRoom)
    					for that in adventurer.inventory:
    						dict[0].extend(that.dict[0])
    						dict[1].extend(that.dict[1])
    						dict[2].extend(that.dict[2])
    						dict[5].extend(that.dict[5])
    						keyvals.update(that.keyvals)
    					#print("Room:",currRoom.name,"Contents:",currRoom.contents)
    					if 'outside' in dict[1]:
    						youWin()
    				elif func.split('.')[1] in ['attack']:
    					keyvals[func](adventurer.attackPower)
    					obj=func.split('.')[0]
    					res=re.findall('[a-zA-Z][^A-Z]*',func.split('.')[0])
    					if debug: 
    						if len(res)>1: 
    							print(res[1])
    					if (len(res)==1 or (len(res)>1 and res[1].lower() not in ['door'])) and keyvals[obj].health<=0:
    						print("You defeated the {}!".format(keyvals[obj].description))
    						#here its inventory should no longer be hidden, so adventurer can check it and take items
    						#keyvals[obj].hideInventory=0
    						#keyvals[obj].action='incapacitated'
    						dict,keyvals=keyvals[obj].defeated(dict,keyvals)
    					else:
    						if res[0] not in ['adventurer']:
    							if len(res)==1 or (len(res)>1 and res[1].lower() not in ['door']):
    								if keyvals[obj].action in ['sleeping']:
    									keyvals[obj].wake()
    								print(keyvals[obj].description,"attacks you back!")
    								adventurer.attack(keyvals[obj].attackPower)
    					if adventurer.health<=0:
    						print("You have run out of health.")
    						gameOver()
    				else:
    					keyvals[func]()
    			# gotta get changing rooms to work... maybe always return currRoom, as well as dict and keyvals? Or just handle those enterDoor functions differently andreturn those there?
    		except Exception as e:
    			print("Something is wrong with the parsed input:")
    			print(e)
    			print("Please try again.")
    			inputAccepted=0
  	currRoom.seeRoom()
  #
  print("This is all that has been written thus far.")
  gameOver()

if __name__ == '__main__':
	main(debug)
