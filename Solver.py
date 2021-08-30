from MineEnv import *
import random
import time
class Solver(object):
	won=False
	def __init__(self,env):
		self.env=env
		self.actions=[(i,j) for i in range(self.env.cellmax) for j in range(self.env.cellmax)]
	##### Returns list of [(y,x)]
	def get_neighbours(self,point):
		x=point[1]
		y=point[0]
		cellmax=self.env.cellmax
		alllist=[]
		toplist=[(y-1,i) for i in range(x-1,x+2) if i>=0 and i<=cellmax-1 and y-1>=0]
		bottomlist=[(y+1,i) for i in range(x-1,x+2) if i>=0 and i<=cellmax-1 and y+1<cellmax-1]
		middlelist=[(y,i) for i in range(x-1,x+2,2) if i>=0 and i<=cellmax-1]
		alllist.extend(toplist)
		alllist.extend(bottomlist)
		alllist.extend(middlelist)
		return alllist

	def unsolved_point(self,point):
		return [i for i in self.get_neighbours(point) if self.env.state[i[0]][i[1]]==9]

	def unsolved_all(self):
		return [i for i in self.actions if self.env.state[i[0]][i[1]]==9] 
	def solved_all(self):
		return [i for i in self.actions if self.env.state[i[0]][i[1]]!=9] 
	def marked_point(self,point):
		return [i for i in self.get_neighbours(point) if self.env.state[i[0]][i[1]]==10]
	def marked_all(self):
		return [i for i in self.actions if self.env.state[i[0]][i[1]]==10]
	def check_mistake(self):
		for i in self.solved_all():
			if(self.env.state[i[0]][i[1]]==10 and self.env.grid[i[0]][i[1]]!=-1):
				return i
		return False
	def check_win(self):
		# print(len(self.marked_all()))
		# self.env.draw_state()
		# print([i for i in self.actions if self.env.state[i[0]][i[1]]==9] )
		# print(len(self.unsolved_all()))
		return len(self.marked_all())+len(self.unsolved_all())==self.env.bombnumber
	"""actions are in y,x format"""
	def choose_action(self):
		if (all(j==9 for i in solver.env.state for j in i)): return ("step",[random.choice(self.actions)]) # check if the board is still all unsolved
			
		solved=self.solved_all()
		for i in solved:
			# if( i == (2,5)):
				
			# 	print(self.get_neighbours(i))
			# 	print(self.unsolved_point(i))
			# 	print(len(self.unsolved_point(i)))
			# 	print(len(self.marked_point(i)))
			# 	print(self.env.state[i[0]][i[1]])
			# 	print("//")
			# 	if(len(self.unsolved_point(i))-len(self.marked_point(i))==self.env.state[i[0]][i[1]]): print("infirst")
			"""Rule 1 : Mark unsolved positions that are near point when :
			---value of points not equal zero
			---number of unsolved points (near that point) different that zero
			---number of unsolved points (near that point) plus number of marked points(near that point) is equal to the value of that point"""
			if( self.env.state[i[0]][i[1]]!=0 
				and len(self.unsolved_point(i))!=0
				and len(self.unsolved_point(i))+len(self.marked_point(i))==self.env.state[i[0]][i[1]]):
				return ("mark",self.unsolved_point(i))
			"""Rule 2 : When marked points (near that point) is equal to the value of that point, check if the value is different than zero, 
			and that there exists an unsolved point(s) as well, then step on those point(s)"""
			if(len(self.marked_point(i))==self.env.state[i[0]][i[1]] 
				and self.env.state[i[0]][i[1]]!=0 
				and not (len(self.unsolved_point(i))==0)):
					return ("step",self.unsolved_point(i))

		return ("step",[random.choice(self.unsolved_all())])


env= MinesweeperEnv()
solver=Solver(env)


over=True

# # solver.env.draw_state()
# print(solver.env.state[0][3])
# print(solver.env.grid[0][3])


# print(solver.get_neighbours((2,5)))
# print(solver.get_neighbours((6,3)))

while(over):
	action=solver.choose_action()
	# print(action)
	time.sleep(0.25)
	# print(action)
	if(action[0]=="step"):
		for i in action[1]:
			solver.env.step(i)
	elif action[0]=="mark":
		for i in action[1]:
			solver.env.mark(i)
	else:
		print("No Solution Stop")
		over=False

	solver.env.visualize_state()
	if(solver.check_win()):
		print("Win stop")
		over=False
	if(solver.check_mistake()):
		print(solver.check_mistake())
		print("Mistake Stop")
		over=False
while True:
	solver.env.visualize_state()
