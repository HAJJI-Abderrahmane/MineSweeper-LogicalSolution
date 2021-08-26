from MineEnv import *
import random
import time
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
	def marked_point(self,point):
		return [i for i in self.get_neighbours(point) if self.env.state[i][0]==10]
	def check_mistake(self):
		for i in self.solved_all():
			if(self.env.state[i]==10 and self.env.grid[i[0]][i[1]]!=-1):
				return i
		return False
	def choose_action(self):
		if ((self.env.state==9).all()):
			return ("step",[random.choice(self.actions)])
		solved=self.solved_all()
		for i in solved:
			if(len(self.unsolved_point(i))-len(self.marked_point(i))==self.env.state[i][0] and self.env.state[i][0]!=0 and len(self.unsolved_point(i))!=0 and len(self.unsolved_point(i))+len(self.marked_point(i))==self.env.state[i][0]):
				print(len(self.unsolved_point(i)))
				print(len(self.marked_point(i)))
				return ("mark",self.unsolved_point(i))
			if(len(self.marked_point(i))==self.env.state[i][0] and self.env.state[i][0]!=0):
				if(len(self.unsolved_point(i))==0):
					continue
				else:
					# print(i)
					return ("step",self.unsolved_point(i))

		return (["over"])


env= MinesweeperEnv()
solver=Solver(env)


over=True
solver.env.draw_grid()
while(over):
	if(solver.check_mistake()):
		print("Mistake Stop")
		over=False
	action=solver.choose_action()

	# print(action)
	# solver.env.draw_state()
	if(action[0]=="step"):
		for i in action[1]:
			solver.env.step(i)
	elif action[0]=="mark":
		for i in action[1]:
			if action==('mark', [(1, 7), (2, 7), (1, 6)]):

				over=False
			solver.env.mark(i)
	else:
		print("No Solution Stop")
		over=False
	# solver.env.draw_state()
	# print("aaa")
	solver.env.visualize_state()
	# time.sleep(1)
# solver.env.draw_state()
while True:
	solver.env.visualize_state()
# print(solver.check_mistake())
	# print("//////////////")
# print("Its over")
# over=True
# while(over):
# 	solver.env.visualize_state()

##### ADD SUBLIME MERGE AND PLUGIN FOR TODOS
#####TODO : fix more empty rolls