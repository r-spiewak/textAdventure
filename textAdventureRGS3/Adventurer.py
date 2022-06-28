from . import Character
from . import Chest
class Adventurer(Character.Character):
	def __init__(self,name='adventurer',health=100,inventory=None,hideInventory=0,attack=10,activity=None,description=None,speech=None):
		#pass
		Character.Character.__init__(self,name,health,inventory,hideInventory,attack,activity,description,speech)
		self.takeable=0
		self.dict[0].extend(['take','get','drop','give','equip','wear','unequip','pick','put'])
		self.dict[4].extend(['up','down','on','out'])
		self.keyvals[self.name+'.equip']=self.equip
		self.keyvals[self.name+'.unequip']=self.unequip
		self.keyvals[self.name+'.take']=self.take
		self.keyvals[self.name+'.drop']=self.drop
		#add dict entries for items/equipment and their methods
		self.equipment={'sword': None, 'shield': None, 'armor': None, 'helmet': None}
	def take(self,*args):
		if len(args[0])<2:
			print("Didn't get enough args to take.")
			print(args)
			return
		item=args[0][0]
		if not item:
			print("Didn't get item to take.")
			return
		room=args[0][1]
		if not room:
			print("Didn't get room to take.")
			return
		#pass
		#add item to inventory and remove it from room
		if item.takeable==0:
			print("The {} cannot be taken.".format(item.description))
			return
		if item in self.inventory:
			print("The {} is already in {}r inventory.".format(item.description,self.description))
			return
		if isinstance(room,Character.Character):
			if room.hideInventory:
				print("The {} prevents you from seeing its inventory.".format(room.description))
				return
			if item not in room.inventory:
				print("{} does not have a {}...".format(room.description,item.description))
				return
			room.removeInventory(item)
		elif isinstance(room,Chest.chest):
			if room.hideInventory:
				print("The {} is closed.".format(room.description))
				return
			if item not in room.inventory:
				print("{} does not have a {}...".format(room.description,item.description))
				return
			room.removeInventory(item)
		else:
			if item not in room.contents:
				print("There is no {} here...".format(item.description))
				return
			room.removeContents(item)
		self.addInventory(item)
		print("{} took the {}.".format(self.description,item.description))
	def drop(self,*args):
		if len(args[0])<2:
			print("Didn't get enough args to drop.")
			print(args)
			return
		item=args[0][0]
		if not item:
			print("Didn't get item to drop.")
			return
		room=args[0][1]
		if not room:
			print("Didn't get room to drop.")
			return
		#unequip item if necessary, remove item from inventory, and add item to room
		if item.status==1:
			self.unequip(item)
		self.removeInventory(item)
		room.addContents(item)
		print("{} dropped the {}.".format(self.description,item.description))
	def equip(self,item):
		#pass
		if item not in self.inventory:
			print("{} do not have a {}...".format(self.description,item.description))
			return
		if item.itemType not in ['sword','shield','armor','helmet']:
			print("Cannot equip {} items.".format(item.itemType))
			return
		#check if item type is already equipped. If it is, unequip that one first
		if self.equipment[item.itemType]:
			self.unequip(self.equipment[item.itemType])
		#attach attributes of item 
		self.health+=item.defense
		self.attackPower+=item.attackPower
		#set it to equipped status and add it to list of equipped items
		item.status=1
		self.equipment[item.itemType]=item
		print("{} equipped the {}.".format(self.description,item.description))
	def unequip(self,item):
		#pass
		#remove attributes of item
		self.health-=item.defense
		self.attackPower-=item.attackPower
		#set it to unequipped status and remove it from lost of equiped items (a keyvals with all the item typee, empty if there is none equipped)
		item.status=0
		self.equipment[item.itemType]=None
		print("{} unequipped the {}.".format(self.description,item.description))
