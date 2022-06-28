import random
import operator
class puzzle:
	def __init__(self,name='orangePuzzle',puzzleType=0,iters=3,clue=None,answer=None):
		self.name=name
		self.puzzleType=puzzleType
		self.iters=iters
		self.clue=clue
		self.answer=answer
	def solve(self,adventurer):
		if self.puzzleType==0:
			print("Math quiz!")
			operators=['+','-','*']
			operatorsDict={'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
			for ii in range(0,self.iters):
				one=random.SystemRandom().randint(0,10)
				two=random.SystemRandom().randint(0,10)
				oper=random.SystemRandom().choice(operators)
				print("What is",one,oper,two,"?")
				#print(operatorsDict[oper](one,two))
				if not input("> ")==str(operatorsDict[oper](one,two)):
					return 0
		elif self.puzzleType==1:
			#riddle?
			if not self.clue:
				print("Error! No clue given for {}!".format(self.description))
				return 1
			if not self.answer:
				print("Error! No answer given for {}!".format(self.description))
				return 1
			print(self.clue)
			return self.answer in input("> ").lower().split(' ')
		elif self.puzzleType==2:
			#wear the correct equipment
			if not self.clue:
				print("Error! No clue given for {}!".format(self.description))
				return 1
			if not self.answer:
				print("Error! No answer given for {}!".format(self.description))
				return 1
			print(self.clue)
			for item in adventurer.equipment.values():
				if not item:
					return 0
				#print("{}:".format(item.description.split(' ')[1]),item.description.split(' ')[0], self.answer)
				if item.description.split(' ')[0] != self.answer:
					return 0
		return 1