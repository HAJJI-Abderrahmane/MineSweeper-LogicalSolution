from MineEnv import *
import random
class Solver(object):
	won=False
	def __init__(self,env):
		self.env=env
		self.actions=[(i,j) for i in range(self.env.cellmax) for j in range(self.env.cellmax)]

	def get_neighbours(self,point):
		x=point[0]
		y=point[1]
		cellmax=self.env.cellmax
		alllist=[]
		toplist=[(i,y-1) for i in range(x-1,x+2) if i>=0 and i<=cellmax-1 and y-1>=0]
		bottomlist=[(i,y+1) for i in range(x-1,x+2) if i>=0 and i<=cellmax-1 and y+1<cellmax-1]
		middlelist=[(i,y) for i in range(x-1,x+2,2) if i>=0 and i<=cellmax-1]
		alllist.extend(toplist)
		alllist.extend(bottomlist)
		alllist.extend(middlelist)
		return alllist

	def unsolved_point(self,point):
		return [i for i in self.get_neighbours(point) if self.env.state[i][0]==9]

	def unsolved_all(self):
		return [i for i in solver.actions if solver.env.state[i]==9] 
	def solved_all(self):
		return [i for i in solver.actions if solver.env.state[i]!=9] 
	def choose_action(self):
		if ((self.env.state==9).all()):
			return ("step",random.choice(self.actions))
		solved=self.solved_all()
		for i in solved:
			# print("i : "+str(i))
			# print("len(self.unsolved_point(i)) = "+str(len(self.unsolved_point(i))))
			# print("self.env.state[i] = "+str(self.env.state[i][0]))
			# print("//////////")
			if(len(self.unsolved_point(i))==self.env.state[i][0] and self.env.state[i][0]!=0 and len(self.unsolved_point(i))!=0):
				return ("mark",self.unsolved_point(i))
		return ("over")
env= MinesweeperEnv()
solver=Solver(env)


over=True
while(over):
	action=solver.choose_action()
	if(action[0]=="step"):
		solver.env.step(action[1])
	elif action[0]=="mark":
		for i in action[1]:
			solver.env.mark(i)
	else:
		over=False
	solver.env.visualize_state()
	print("//////////////")
# print("Its over")
# over=True
# while(over):
# 	solver.env.visualize_state()