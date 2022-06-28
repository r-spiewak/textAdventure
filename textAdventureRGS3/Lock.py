import re
class lock():
	def __init__(self,name='blueLock',lockType=0,code=None,key=None,puzzle=None):
		self.lockType=lockType
		self.code=code
		self.key=key
		self.puzzle=puzzle
		self.name=name
		self.dict=[['unlock','open'],['lock'],[re.findall('[a-zA-Z][^A-Z]*',name)[0]],['status'],[],[]]
		self.keyvals={}
		self.keyvals[self.name]=self
		self.keyvals[name+'.check']=self.check
		self.keyvals[name+'.unlock']=self.unlock
	def mergeDict(self,dict1,dict2):
		for ii in range(0,len(dict1)):
			dict1[ii].extend(dict2[ii])
		return dict1
	def unlock(self,adventurer):
		if self.lockType==0:
			print("The lock is old and just crumbled when you touched it.")
			return 1
		elif self.lockType==1:
			#Need to enter the correct passcode
			print("The lock requires a code to unlock.")
			return input("What is the code?\n> ")==self.code
		elif self.lockType==2:
			#lock requires a key to open
			print("The lock requires the correct key to open.")
			if self.key==None:
				print("Error! No key assigned to lock {}!".format(self.description))
			if self.key in adventurer.inventory:
				print("{} used the {} to unlock the door.".format(adventurer.description,self.key.description))
				return 1
			else:
				print("The correct key is not currently in the inventory of {}.".format(adventurer.description))
				return 0
		elif self.lockType==3:
			#lock requires solving a puzzle to open
			if self.puzzle==None:
				print("Error! No puzzle assigned to lock {}!".format(self.description))
			print("The lock requires solving this puzzle to unlock:")
			return self.puzzle.solve(adventurer)
		else:
			#presumably somwthing is wrong...
			return 0
	def check(self,*args):
		if self.lockType==0:
			print("The lock is too old to visibly discern anything about it.")
		elif self.lockType==1:
			print("The lock requires a code to unlock.")
		elif self.lockType==2:
			print("The lock requires a key to unlock")
		elif self.lockType==3:
			print("The lock seems to require solving a puzzle to unlock.")
		else:
			print("The lock is too confusing to check.")