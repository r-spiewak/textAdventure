class room():
	def __init__(self,name='initialRoom',contents=None,prev=None,dict=None,keyvals=None):
		if not contents:
			self.contents=[]
		else:
			self.contents=contents
		self.name=name
		self.takeable=0
		#the dicts and keyvals that I had before should be room specific probably, with the adventurer entries included in every room
		#gotta also keep track of which room we're in and from which room (in the room tree starting from the initial room) we came, so that we can get back. Thinking about it like a tree with nodes clarifues the data structure... 
		#gotta also keep track of all the rooms ' visitation statuses; initialize them if new, but save state if we've been there before. Maybe just don't remove them from memory?
		self.prev=prev
		#if not dict:
			#self.dict=[[],[],[],[],[]]
		#else:
			#self.dict=dict.copy()
		self.dict=[[],[],[],[],[],[]]
		if dict:
			self.dict=self.mergeDict(self.dict,dict)
		self.dict[0].extend(['exit','leave','run','flee','go'])
		self.dict[1].append('room')
		self.dict[4].append('back')
		if not keyvals:
			self.keyvals={}
		else:
			self.keyvals=keyvals.copy()
		self.keyvals[self.name]=self
		self.keyvals[self.name+'.exitRoom']=self.exitRoom
	def check(self):
		#if not self.contents:
			#print("This room is empty...")
		#else:
			#print(self.contents)
		self.seeRoom()
	def seeRoom(self):
		if not self.contents:
			print("This room is empty...")
		else:
			print("You see a"," and a ".join([thing.description for thing in self.contents])+".")
	def mergeDict(self,dict1,dict2):
		for ii in range(0,len(dict1)):
			dict1[ii].extend(dict2[ii])
		return dict1
	def addContents(self,thing):
		self.contents.append(thing)
		if thing.dict:
			self.dict=self.mergeDict(self.dict,thing.dict)
		if thing.keyvals:
			self.keyvals.update(thing.keyvals)
	def removeContents(self,thing):
		#pass
		self.contents.remove(thing)
		#remove it from self.contents, and try to remove exactly those entries amd exactly those numbers of repetitions from room dict, and same for keyvals
	def enterRoom(self):
		#self.seeRoom()
		return self,self.dict,self.keyvals
	def exitRoom(self,*args):
		if not self.prev:
			print("This is the first room...")
			return self,self.dict,self.keyvals
		else:
			#return self.prev.dict,self.prev.keyvals
			return self.prev.enterRoom()