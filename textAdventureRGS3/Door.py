import re
class door():
	#import re
	def __init__(self,name='blueDoor',status=1,lock=None,room=None):
		self.name=name
		self.description=' '.join(re.findall('[a-zA-Z][^A-Z]*',name)).lower()
		self.status=status#0=open,1=closed,2=locked
		self.lock=lock
		self.room=room
		self.takeable=0
		#self.dict=[['unlock','open','enter','go','attack'],['door'],[name],['status','lock'],['to','through','into']]
		#self.dict=[['unlock','open','enter','go','attack'],['door'],[re.findall('[a-zA-Z][^A-Z]*',name)[0]],['status','lock'],['to','through','into']]
		self.dict=[['unlock','open','enter','go','attack'],['door'],[re.findall('[a-zA-Z][^A-Z]*',name)[0]],['status'],['to','through','into'],[]]
		self.keyvals={}
		self.keyvals[self.name]=self
		self.keyvals[name+'.check']=self.check
		self.keyvals[name+'.unlock']=self.unlock
		self.keyvals[name+'.openDoor']=self.openDoor
		self.keyvals[name+'.enterDoor']=self.enterDoor
		self.keyvals[name+'.attack']=self.attack
		if lock:
			if self.lock.dict:
				self.dict=self.mergeDict(self.dict,self.lock.dict)
			if self.lock.keyvals:
				self.keyvals.update(self.lock.keyvals)
	def mergeDict(self,dict1,dict2):
		for ii in range(0,len(dict1)):
			dict1[ii].extend(dict2[ii])
		return dict1
	def unlock(self,adventurer):
		#pass
		if self.status<2:
			print("The door is not locked.")
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
				print("The door is now unlocked.")
			else:
				print("Unlock unsuccessful.")
			return
	def openDoor(self):
		if self.status==2:
			print("The door is locked.")
			return 
		elif self.status==1:
			self.status=0
			print("The door is now open!")
			return
		else:
			print("The door is already open!")
			return
	def check(self,*args):
		if self.status==0:
			print("The door is open.")
			return
		elif self.status==1:
			print("The door is closed.")
			return
		else:
			print("The door is locked.")
			# Show the description of the lock from the lock function
			self.lock.check()
			return
	def enterDoor(self,*room):
		if self.status==0:
			print("Entering door!")
			if self.room:
				return self.room.enterRoom()
			else:
				print("Behind the door is... just a rock wall?")
				print("It appears as if the ceiling caved in and this tunnel collapsed.")
				print("Can't go through that...")
				print("You return to the previous room.")
			return room[0],room[0].dict,room[0].keyvals
		else:
			print("The door is closed.")
			return room[0],room[0].dict,room[0].keyvals
	def attack(self,*args):
		print("The door is too solid; attacking it had no effect.")
		return