A* Search
Assignment 3

Run Options:

./aStar.py "World number" "Heuristic type"

"World numvber": either 1 or 2
"Heuristic type": either manhattan or diagonal

Diagonal Heuristic:
Equation:
function heuristic(node) =
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
As found in: http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

Motivation:
	The Manhattan distance is usually used to estimate the distance between two blocks when only
	non-diagnal moves are allowed,
	In our case, we are dealing with a grid were diagonal moves are allowed, yet costs more, and thus,
	using an estimation that includes diagonal should be better.
	When we are dealing with diagonal moves, using a Diagonal approximation provide us with an estimation that
	doesn't vary much between adjacent blocks as much as manhattan distance.
	
Results:
Manhattan:
	World1:
			Locations Visited: 62
			Path: (0,7)-(1,6)-(1,5)-(1,4)-(1,3)-(2,2)-(3,2)-(4,1)-(5,0)-(6,0)-(7,0)-(8,0)-(9,0)
			Cost of path: 156
	World2:
			Locations Visited: 58
			Path: (0,7)-(0,6)-(0,5)-(1,4)-(2,4)-(3,4)-(4,3)-(4,2)-(4,1)-(5,0)-(6,0)-(7,0)-(8,0)-(9,0)
			Cost of path: 142
Diagonal:
	World1:
			Locations Visited: 62
			Path: (0,7)-(1,7)-(2,7)-(3,6)-(4,5)-(4,4)-(5,3)-(6,3)-(7,3)-(8,2)-(9,1)-(9,0)
			Cost of path: 130
	World2:
			Locations Visited: 58
			Path: (0,7)-(1,7)-(2,7)-(3,6)-(3,5)-(4,4)-(5,3)-(4,2)-(4,1)-(5,0)-(6,0)-(7,0)-(8,0)-(9,0)
			Cost of path: 150
			
Preformance and Analysis:

As we can see, in the first world the Diagonal Heuristic gives a better estimation for A* search
this is due to the fact that we used many diagonal moves in that trace,

However, when looking at the second map, the diagonal did a bit worse than the Manhattan,
When comparing the results, we can see that in the second map, the use of diagonal moves is not very efficient
thus, it makes sense to have less accurate estimation when not using very much diagonal moves.

	
	


	



