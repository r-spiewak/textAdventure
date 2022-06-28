from . import Chest
class Character:
	def __init__(self,name='adventurer',health=100,inventory=None,hideInventory=0,attack=10,activity=None,description=None,speech=None):
		self.name=name
		self.health=health
		if not inventory:
			self.inventory=[]
		else:
			self.inventory=inventory
		self.hideInventory=hideInventory
		self.takeable=0
		self.attackPower=attack
		self.action=activity
		self.speech=speech
		if not description:
			self.description='You'
		else:
			self.description=description
		self.dict=[['attack','slay','kill','fight','talk','speak','ask','say','wake','give','drop'],[self.name],[],['health','hp','defense','items','inventory','equipment','attack power','ap','activity','action'],[],[]]
		if speech:
			for key in speech.keys():
				self.dict[2].append(key)
		self.keyvals={}
		self.keyvals[self.name]=self
		self.keyvals[self.name+'.check']=self.check
		self.keyvals[self.name+'.attack']=self.attack
		self.keyvals[self.name+'.talk']=self.talk
		self.keyvals[self.name+'.wake']=self.wake
		self.keyvals[self.name+'.give']=self.give
		self.keyvals[self.name+'.drop']=self.drop
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
	def drop(self,*args):
		#print(args)
		item=args[0][0]
		room=args[0][1]
		if item not in self.inventory:
			print("The {} is not in {}'s inventory.".format(item.description,self.description))
			return
		#unequip item if necessary, remove item from inventory, and add item to room
		if item.status==1:
			self.unequip(item)
		self.removeInventory(item)
		room.addContents(item)
		print("{} dropped the {}.".format(self.description,item.description))
	def give(self,*args):
		#acrually, don't use this function. At least not yet. The main parsing scheme is not set up to handle two nouns. But this isbprobably something necessary, so the parsing scheme needs to be updated to handle it. Unless I just handle this as a special case, and change object to  adventurer and subject to whatever object was, and then create the list argument? But I will still need to deal with the two other nouns, namely the character and the item. 
		#Should I add a special dictiomary list for items? No, because then we cannot just check items... Or maybe have them in the regular place and also in a new place, to compare and treat the second noun differently?
		#Also, only adventurer should give. All other characters should just drop for adventurer to pick up.
		if len(args[0])<2:
			print("Didn't get enough args to give.")
			print(args)
			return
		item=args[0][0]
		if not item:
			print("Didn't get item to give.")
			return
		other=args[0][1]
		if not other:
			print("Didn't get other to give.")
			return
		if isinstance(other,Chest.chest) and other.status>0:
			print("The {} is closed.".format(other.description))
			return
		if item in self.inventory:
			if item.status==1:
				if self.description=='You':
					self.unequip(item)
			self.removeInventory(item)
			other.addInventory(item)
			print("{} gave {} to {}.".format(self.description,item.description,other.description))
		else:
			print("The {} is not in {}'s inventory.".format(item.description,self.description))
	def check(self,element):
		element=element.lower()
		if element==self.name:
			print("It's a {}!".format(self.description))
		elif element in ['health','hp']:
			print(self.health)
			return self.health
		elif element in ['inventory','items','equipment']:
			if not self.hideInventory:
				if self.description=='You' and element in ['equipment']:
					#print('['+', '.join([item.description for item in self.equipment])+']')
					#print(self.equipment)
					#print('{'+', '.join([key+': '+val for key,val in g.items()])+'}')
					#print('{'+', '.join([key+': '+val if val else key+': None' for key,val in g.items()])+'}')
					print('{'+', '.join([key+': '+item.description if item else key+': None' for key,item in self.equipment.items()])+'}')
					return self.equipment
				else:
					print('['+', '.join([item.description for item in self.inventory])+']')
					return self.inventory
			else:
				print( 'The {} prevents you from seeing its inventory.'.format(self.description))
				return 'The {} prevents you from seeing its inventory.'.format(self.description)
		#'''
		#elif element in ['equipment']:
		#	if not self.hideInventory:
		#		print(self.equipment)
		#		return self.equipment
		#	else:
		#		return 'The {} prevents you from seeing its equipment.'.format(self.description)
		#'''
		elif element in ['attack power','ap']:
			print(self.attackPower)
			return self.attackPower
		elif element in ['activity','action']:
			print("The {} is {}.".format(self.description,self.action))
			return self.action
		else:
			print('Unknown element.')
			return 'Unknown element.'
	def attack(self,damage):
		if self.action in ['incapacitated']:
			print("The {} has already been defeated.".format(self.description))
			return
		#add random chance of attack missing?
		if not isinstance(damage,int) and len(damage)>1:
			print("Cannot attack {}.".format(damage[0].description))
			return
		print(self.description,"took",damage,"damage.")
		self.health-=damage
	def talk(self,*prompt):
		if self.action in ['sleeping','incapacitated']:
			print("The {} is {}.".format(self.description,self.action))
		elif self.speech:
			print("The {} says:".format(self.description))
			print()
			if len(self.speech)==1:
				#print(self.speech)
				print(list(self.speech.values())[0])
				print()
			elif prompt[0] not in self.speech:
				print("I'm sorry. I don't know about a {}.".format(prompt[0]))
				print()
			else:
				print(self.speech[prompt[0]])
				print()
				#if self.name=='dragon' and prompt[0]=='purple':
				#	self.drop(dragonsNote)
		else:
			print("The {} just looks at you, uncomprehending.".format(self.description))
	def wake(self):
		if self.action in ['sleeping']:
			self.action=None
			print("You woke the {}.".format(self.description))
		else:
			print("The {} isn't sleeping".format(self.description))
	def defeated(self,dict,keyvals):
		self.hideInventory=0
		self.action='incapacitated'
		for that in self.inventory:
			dict[1].extend(that.dict[1])
			dict[2].extend(that.dict[2])
			dict[5].extend(that.dict[5])
			keyvals.update(that.keyvals)
		return dict,keyvals
