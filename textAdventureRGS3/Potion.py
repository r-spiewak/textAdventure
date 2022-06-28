from . import Item
class potion(Item.item):
	def __init__(self,name='redPotion',takeable=1,status=0,itemType='potion',attack=0,defense=100,inventory=None,hideInventory=0,hasInventory=0,description=None,message=None):
		Item.item.__init__(self,name,takeable,status,itemType,attack,defense,inventory,hideInventory,hasInventory,description,message)
		self.keyvals[self.name+'.drink']=self.drink
		self.dict[0].append('drink')
	def drink(self,adventurer):
		if not self in adventurer.inventory:
			print("{} do not have a {}...".format(adventurer.description,self.description))
			return
		adventurer.health+=self.defense
		adventurer.removeInventory(self)
		print("{} drank the {}!".format(adventurer.description,self.description))
