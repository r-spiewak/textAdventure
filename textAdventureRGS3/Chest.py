import Item
class chest(Item.item):
	def __init__(self,name='woodenChest',takeable=0,status=1,itemType='chest',attack=0,defense=0,inventory=None,hideInventory=1,hasInventory=1,description=None,message=None,lock=None):
		Item.item.__init__(self,name,takeable,status,itemType,attack,defense,inventory,hideInventory,hasInventory,description,message)
		self.keyvals[self.name+'.unlock']=self.unlock
		self.keyvals[self.name+'.open']=self.open
		self.keyvals[self.name+'.attack']=self.attack
		self.dict[0].extend(['unlock','open','attack'])
	def unlock(self,adventurer):
		#pass
		if self.status<2:
			print("The {} is not locked.".format(self.description))
			return
		else:
			#pass
			# Somehow run a function defined by self.lock which is a puzzle required to unlock the door. Unlock on success.
			if not self.lock:
				print("The lock is old and just crumbled when you touched it.")
				unlockSuccess=1
			else:
				unlockSuccess=self.lock.unlock(adventurer)
			if unlockSuccess:
				self.status=1
				print("The {} is now unlocked.".format(self.description))
			else:
				print("Unlock unsuccessful.")
			return
	def open(self,*args):
		#print(args)
		dict=args[0][0]
		keyvals=args[0][1]
		if self.status==2:
			print("The {} is locked.".format(self.description))
			return dict,keyvals
		elif self.status==1:
			self.status=0
			self.hideInventory=0
			for that in self.inventory:
				dict[0].extend(that.dict[0])
				dict[1].extend(that.dict[1])
				dict[2].extend(that.dict[2])
				dict[5].extend(that.dict[5])
				keyvals.update(that.keyvals)
			#return dict,keyvals
			print("The {} is now open!".format(self.description))
			return dict,keyvals
		else:
			print("The {} is already open!".format(self.description))
			return dict,keyvals
	def attack(self,*args):
		print("The {} is too solid; attacking it had no effect.".format(self.description))
		return
	def mergeDict(self,dict1,dict2):
		for ii in range(0,len(dict1)):
			dict1[ii].extend(dict2[ii])
		return dict1
	def addInventory(self,item):
		#pass
		self.inventory.append(item)
		if item.dict:
			self.dict=self.mergeDict(self.dict,item.dict)
		if item.keyvals:
			self.keyvals.update(item.keyvals)
	def removeInventory(self,item):
		#pass
		self.inventory.remove(item)