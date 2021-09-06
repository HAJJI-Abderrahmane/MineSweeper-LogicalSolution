## I managed to create ai that solves most minesweeper games using simple logic rules

you can run ```python Solver.py ``` which will create a new 16 by 16 minesweeper game with 40 bombs, you can change these parameters in ```python MineEnv.py ```, then it might get solved automatically using 2 main rules which are :
- Mark unsolved positions that are near point when :
	- value of points not equal zero
	- number of unsolved points (near that point) different that zero
	- number of unsolved points (near that point) plus number of marked points(near that point) is equal to the value of that point
- When marked points (near that point) is equal to the value of that point, check if the value is different than zero, 
	- and that there exists an unsolved point(s) as well, then step on those point(s).
And the rest is based on luck.
this project has been inspired by Code-Bullet's version of minesweeper AI : [minesweeper-AI](https://github.com/Code-Bullet/minesweeper-AI)