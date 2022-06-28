import re
class item:
	def __init__(self,name='rustySword',takeable=1,status=0,itemType='sword',attack=5,defense=0,inventory=None,hideInventory=0,hasInventory=0,description=None,message=None):
		self.name=name
		if description:
			self.description=description
		else:
			self.description=' '.join(re.findall('[a-zA-Z][^A-Z]*',name)).lower()
		self.message=message
		self.takeable=takeable
		self.status=status
		self.itemType=itemType
		self.attackPower=attack
		self.defense=defense
		self.hideInventory=hideInventory
		self.hasInventory=hasInventory
		if hasInventory and not inventory:
			self.inventory=[]
		else:
			self.inventory=inventory
		if len(re.findall('[a-zA-Z][^A-Z]*',name))>1:
			self.dict=[['check'],[re.findall('[a-zA-Z][^A-Z]*',name)[1].lower()],[re.findall('[a-zA-Z][^A-Z]*',name)[0]],['status','attack power','defense'],[],[self.description,self.name,re.findall('[a-zA-Z][^A-Z]*',name)[0],re.findall('[a-zA-Z][^A-Z]*',name)[1].lower()]]
		else:
			self.dict=[['check'],[name.lower()],[],['status','attack power','defense'],[],[self.description,self.name.lower()]]
		self.keyvals={}
		self.keyvals[self.name]=self
		self.keyvals[self.name+'.check']=self.check
	def check(self,element):
		#print("Element:",element)
		if len(element[0])>1:
			thisList=element
			room=element[0][1]
			element=element[0][0]
		if element!=self.name:
			element=element.lower()
		#print("Element:",element)
		if element==self.name:
			if self.message:
				print(self.message)
			else:
				print("It's a {}!".format(self.description))
		elif element in ['health','hp','defense']:
			print(self.defense)
			return self.defense
		elif element in ['inventory','items','equipment']:
			if not self.hideInventory:
				#print(self.inventory)
				print('['+', '.join([item.description for item in self.inventory])+']')
				return self.inventory
			else:
				print('The {} is closed.'.format(self.description))
				return 'The {} is closed.'.format(self.description)
		elif element in ['attack power','ap']:
			print(self.attackPower)
			return self.attackPower
		else:
			print('Unknown element.')
			return 'Unknown element.'
		