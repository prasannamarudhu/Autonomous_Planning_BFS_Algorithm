""" 
*****************  Name:  Prasanna Marudhu Balasubramanian   ********************
*****************  UID:   116197700                          ********************
*****************  Class: Robotics - 2019 Spring Semester    ********************
*****************  Course: ENPM661-Planning for Autonomous Robots    ********************
###
 
* This Python program is developed to find all the possible states of the 8-Puzzle starting from the given initial state. 
* The states are unique without repetitions.
* The brute force search algorithm (BFS) is used to find the path to reach the goal state using the possible states of 8-puzzle.
* From the initial state of the puzzle, different moves in all the directions is made to generate new states.

File Generation:

The below mentioned files are generated when the output is executed which can be used to visualize the blank tile position changes.
 
1.NodesInfo.txt - matrix which gives the information about the node number, parent node number, and the cost-to-come
2.Nodes.txt - holds the all explored nodes during the execution
3.NodePath.txt - holds the nodes value in the path of reaching final goal node from the initial node

"""

### Modules
import numpy as np
#import importlib
import collections
#import itertools
import sys
import math
import copy
import string
import time
#import keyword

### puzzle_main() is the function which call the other functions in the class PUZZLE8
def puzzle_main():

	NODE = PUZZLE8()          #Initializing class as 'NODE'
	NODE.puzzle_solve_bfs()   #calling the 'puzzle_solve_bfs' function

class PUZZLE8:

	###The '__init__' function initializes the variables with initial values 
	def __init__(self, initial_val=None, node_id=None, parent_id=None, cost2come=None):
		self.par_id = parent_id
		self.c2c = cost2come
		self.values = initial_val
		self.id = node_id

	### The 'puzzle_solve_bfs' function executes the brute force search algorithm to generate the child nodes and check for the goal node

	def puzzle_solve_bfs(self):

		#Global declaration of the variables
		global Iden_Numb      
		global cost_val
		global Nodes

		#Initialising the flags
		FLAG = 0               #Initialising the general flag which is used later
		lim_time_FLAG = 0      #Initialising the flag which indicates the time limit status

		start_val = np.array([[int(j) for j in input().split()] for i in range(3)])   	#obtaining the input from the user-the initial node from which the function should start is obtained
		init_node = PUZZLE8(start_val, Iden_Numb, 0, cost_val)                        	#storing the values 'starting node, ID_Number, parent id and cost2come inside init_node matrix
		Time_start = time.time()              					        #obtaining the start time through 'time' function
		NODE_Collec_Stack = collections.deque() 				      	#Initializing the 'NODE_Collec_Stack'as a deque which accepts the values and stores in a stack		
		NODE_Collec_Stack.append(init_node)     				      	#storing the datas in 'init_node' inside the 'NODE_Collec_Stack'

		### Through this while loop the children nodes are generated and stacked inside the 'NODE_Collec_Stack' 		
		while NODE_Collec_Stack: 						        #while loop executes for the length of the stack
                        
			Time_recent = time.time()                 		 		#The current time data is obtained through the 'time' function and stored in the 'Time_recent'
			current_node = NODE_Collec_Stack.popleft() 				# The current node is obtained from the stack 'NODE_Collec_Stack' through the popleft function so that the
                                                                                                # -value which was stored first is obtained.
			Nodes.append(current_node.values)                    		 	# The current node value is added to the list nodes  
			Str_Node_set.add(self.arr2str(current_node.values))   			# The node is converted into a string for the faster computation and analyzing process
			Inf_Nodes.append([current_node.id, current_node.par_id, current_node.c2c])   # The current nodes information are added to the 'Inf_Nodes' array

			###The current node is compared with the goal node to check whether it is matching through the 'Check_GoalNode' function	
			FLAG = self.Check_GoalNode(current_node)  				#calling the 'Check_GoalNode' function and if both goal node and current node matches we return the flag as 1
			if FLAG == 1:     							# If the flag is 1 then we print the following data in the output console
				print("\n'Success' - The Expected Goal Node is reached")
				print("\nNumber of the total nodes explored is : "+str(len(Nodes)))       		#printing number of nodes
				print("\nLength of the Info Nodes matrix is :  "+str(len(Inf_Nodes)))     		#printing node_info length 
				print("\nText files generated holds the 'Nodes' , 'Node Path' and 'Node Info' data.\nPlease use them to visualize the output. ")
				print("\nThe Time taken to reach the goal node is : "+str(Time_recent-Time_start))  	#printing the execution time
				break
			### The children nodes are generated through the 'BlankTileMovement' function by moving the blank tile in different direction
			Gen_New_Nodes = self.BlankTileMovement(current_node, Str_Node_set)  				#calling the BlankTileMovement function by passing the arguments 'current_node' and 'Str_Node_set' and the new 
                                                                                            				#node will be stored as 'Gen_New_Nodes'
			NODE_Collec_Stack.extend(Gen_New_Nodes)   							# The generated new node will be qeued into the collection stack 'NODE_Collec_Stack'

			### The accumulated time of this ongoing program execution is checked and if it is found running for more than 20minutes then the execution is aborted saying 'No Solution' 
			if Time_recent-Time_start > 1200:  			#if the execution time is more than 20 minutes or 1200 seconds then
				lim_time_FLAG = 1          			#time limit flag is set and loop is broken to exit
				break

			### If the goal node cannot be reached from the input node, then the flag is set to remain false and when this happens then the following information is printed saying 'No Solution' possible
		if (FLAG == 0):			
			print("\n'No Solution', since the Goal node cannot be reached.")
			print("\nNumber of Nodes explored is : "+str(len(Nodes)))         	#printing number of nodes
			print("\nThe Time taken is : "+str(Time_recent-Time_start))       	#printing the execution time 

                ### The accumulated time of this ongoing program execution is checked and if it is found running for more than 20minutes then the execution is aborted saying 'No Solution'
		if lim_time_FLAG == 1:
			print("\n'No solution', since the search occured beyond the expected execution time of 20minutes.")
			print("\nThe Time taken is : "+str(Time_recent-Time_start))		#printing the execution time 

	
	### This 'BlankTileMovement' function generates new child from the parent nodes by moving the blanktile left,up,down and right

	def BlankTileMovement(self, parent_node, explored_nodes):

		### Initiating Generated_Child_Nodes as a blank node
		Generated_Child_Nodes = []  

		### Global declaration of variables
		global Iden_Numb
		global Inf_Nodes
		x, y = 0, 0				#Initializing x and y values

		### Determining the location of the blank tile 
		for i in range(0, 3):
			for j in range(0, 3):
		###When the location is balnk tile is found then the position values are assigned to x and y as corresponding row and column position respectively
				if parent_node.values[i][j] == 0:
					x = i  		#row position of blank tile
					y = j  		#column position of blank tile


		### The blank tile is moved "LEFT" when the blank tile is not in the 0'th column('y' position is not 0)
		if y is not 0:
			### The node values are stored in the child node where the parent node values are deep copied instaed of shallow copy to make it unaffected by the future changes in parent_node.values
			Child_Node = PUZZLE8(copy.deepcopy(parent_node.values), None, parent_node.id, parent_node.c2c+1)
			### The value in the left of the blank tile is moved to the current blank tile position and the blank is moved to the left, basically the positions are swapped
			k = Child_Node.values[x][y - 1]  				#'k' is a temporary variable which helps in swapping data
			Child_Node.values[x][y - 1] = Child_Node.values[x][y]
			Child_Node.values[x][y] = k

			### Checking for the earlier existence of newly generated child node to prevent redundancy to have all the nodes unique 
			if self.arr2str(Child_Node.values) not in explored_nodes:
				###If the child node is unique then the variables are updated as below
				Iden_Numb += 1  					#Identity number is incremented
				Child_Node.id = Iden_Numb 				#Identity number is incremented and stored as current child node id
				Generated_Child_Nodes.append(Child_Node) 		#The new child node is added to the 'Generated_Child_Nodes'

		###The blank tile is moved "UP" when the blank tile is not in the 0'th row('x' position is not 0)
		if x is not 0:
			###The node values are stored in the child node where the parent node values are deep copied instaed of shallow copy to make it unaffected by the future changes in parent_node.values
			Child_Node = PUZZLE8(copy.deepcopy(parent_node.values), None, parent_node.id, parent_node.c2c+1)
			
			### The value in the left of the blank tile is moved to the current blank tile position and the blank is moved to the left, basically the positions are swapped
			k = Child_Node.values[x - 1][y] 				#'k' is a temporary variable which helps in swapping data
			Child_Node.values[x - 1][y] = Child_Node.values[x][y]
			Child_Node.values[x][y] = k

			### Checking for the earlier existence of newly generated child node to prevent redundancy to have all the nodes unique 
			if self.arr2str(Child_Node.values) not in explored_nodes:
				### If the child node is unique then the variables are updated as below
				Iden_Numb += 1 						#Identity number is incremented
				Child_Node.id = Iden_Numb 				#Identity number is incremented and stored as current child node id
				Generated_Child_Nodes.append(Child_Node) 		#The new child node is added to the 'Generated_Child_Nodes'

		### The blank tile is moved "DOWN" when the blank tile is not in the 2'nd row('x' position is not 2)
		if x is not 2:  
			### The node values are stored in the child node where the parent node values are deep copied instaed of shallow copy to make it unaffected by the future changes in parent_node.values
			Child_Node = PUZZLE8(copy.deepcopy(parent_node.values), None, parent_node.id, parent_node.c2c+1)
			### The value in the left of the blank tile is moved to the current blank tile position and the blank is moved to the left, basically the positions are swapped
			k = Child_Node.values[x + 1][y] 				#'k' is a temporary variable which helps in swapping data
			Child_Node.values[x + 1][y] = Child_Node.values[x][y]
			Child_Node.values[x][y] = k

			### Checking for the earlier existence of newly generated child node to prevent redundancy to have all the nodes unique 
			if self.arr2str(Child_Node.values) not in explored_nodes:
				### If the child node is unique then the variables are updated as below
				Iden_Numb += 1 						#Identity number is incremented
				Child_Node.id = Iden_Numb 				#Identity number is incremented and stored as current child node id
				Generated_Child_Nodes.append(Child_Node) 		#The new child node is added to the 'Generated_Child_Nodes'


		### The blank tile is moved "RIGHT" when the blank tile is not in the 2'nd column('y' position is not 2)
		if y is not 2:
			### The node values are stored in the child node where the parent node values are deep copied instaed of shallow copy to make it unaffected by the future changes in parent_node.values
			Child_Node = PUZZLE8(copy.deepcopy(parent_node.values), None, parent_node.id, parent_node.c2c+1)
			### The value in the left of the blank tile is moved to the current blank tile position and the blank is moved to the left, basically the positions are swapped
			k = Child_Node.values[x][y + 1]  				#'k' is a temporary variable which helps in swapping data
			Child_Node.values[x][y + 1] = Child_Node.values[x][y]
			Child_Node.values[x][y] = k

			### Checking for the earlier existence of newly generated child node to prevent redundancy to have all the nodes unique 
			if self.arr2str(Child_Node.values) not in explored_nodes:
				### If the child node is unique then the variables are updated as below
				Iden_Numb += 1 						#Identity number is incremented
				Child_Node.id = Iden_Numb 				#Identity number is incremented and stored as current child node id
				Generated_Child_Nodes.append(Child_Node) 		#The new child node is added to the 'Generated_Child_Nodes'

		return Generated_Child_Nodes 						# The generated child node is returned as output from this 'BlankTileMovement' function

	### The function 'nod2str' converts the node in the string form to be stored in the txt file that will be generated when the program is executed
	def nod2str(self, conv_node): 							#The argument 'conv_node' is passed into the function to convert node to string in the form of list
		data = ''
		for i in conv_node:
			for j in i:
				data += str(j) + " " 					#adding space between the each data stored in the list
		return data

	### The function 'Check_GoalNode' is used to determine whether the current node in process is equal to the goal node
	def Check_GoalNode(self, current_node):
		Node_ReachPath = []  							# Initiating 'Node_ReachPath' array
		
		### Comparing the nodes in below of condition
		if self.arr2str(current_node.values) == self.arr2str(Goal_State_Node):
			### when both current node and the goal node are same then variables are assigned as follows
			CurrNode_id = current_node.id
			ParNode_id = current_node.par_id
			Node_ReachPath.append(Nodes[CurrNode_id - 1]) 			#storing the current node inside the 'Node_ReachPath' 
			Node_ReachPath.append(Nodes[ParNode_id - 1])  			#storing the parent node of current node inside the 'Node_ReachPath'
		
		### All the nodes in the path from initial node to goal node is obtained thorugh the following while loop and appended to the 'Node_ReachPath' to derive the node path matrix
			while ParNode_id != 1: 						#until the initial(start) node is reached, the loop is executed
				### current node id and parent node id are obtained through the following statements
				CurrNode_id = [x for x in Inf_Nodes if ParNode_id in x][0][0]  #[0][0] indicates the current node id position in 'Inf_Nodes' matrix
				ParNode_id = [x for x in Inf_Nodes if ParNode_id in x][0][1]   #[0][1] indicates the parent node id position in 'Inf_Nodes' matrix
                                ###when the id are obtained then the corresponding node related to that id is derived from the Node matrix and added to the 'Node_ReachPath' matrix
				Node_ReachPath.append(Nodes[CurrNode_id - 1])  		#storing the current node inside the 'Node_ReachPath' 
				Node_ReachPath.append(Nodes[ParNode_id - 1])   		#storing the parent node of current node inside the 'Node_ReachPath'
			
			### The matrix data is reversed and written to the files generated
			Node_ReachPath.reverse()
			self.File_Generation_txt(Inf_Nodes, 1) 				#NodesInfo.txt file data is written
			self.File_Generation_txt(Nodes, 2)     				#Nodes.txt file data is written
			self.File_Generation_txt(Node_ReachPath, 3)			#NodePath.txt file data is written
			
			### Node path is printed in the output console
			print("Node Path is:\n")
			print(Node_ReachPath)	
	
			### Flag set as True and returned to while loop inside 'puzzle_solve_bfs' function
			FLAG = 1
			return FLAG

		### when both current node and the goal node are not same then the Flag is set as False	
		else:
			FLAG = 0
			return FLAG

	###The obtained Node, Node path and Node info matrix data are written in the generated files in the 'File_Generation_txt' function
	def File_Generation_txt(self, explored_nodes, File_Numb): 			#The explored node and file number is passed as the arguments

		if File_Numb == 1:  
			### when the file number is 1 then the 'NodesInfo.txt' data is written
			fileopen = open('NodesInfo.txt', 'w') 				#opening the file
			for i in range(0, len(explored_nodes)): 			#loop executed for the length of nodes in 'explored_nodes'
				for j in range(0, 3):
					string_val = explored_nodes[i][j] 		#data written as string
					fileopen.write("%s " % string_val)
				fileopen.write("\n") 					#writing in new line
			fileopen.close()             					#closing the file


		if File_Numb == 2:
		### when the file number is 2 then the 'Nodes.txt' data is written
			fileopen = open('Nodes.txt', 'w') 				#opening the file
			for i in range(0, len(explored_nodes)):  			#loop executed for the length of nodes in 'explored_nodes'
				transposed_nodes = explored_nodes[i].transpose() 	#transposed to write the data in expected format
				string_val = self.nod2str(transposed_nodes) 		#data written as string
				fileopen.write("%s \n" % string_val) 			#writing in new line
			fileopen.close() 						#closing the file

		if File_Numb == 3:
		### when the file number is 1 then the 'NodesInfo.txt' data is written
			fileopen = open('nodePath.txt', 'w') 				#opening the file
			for i in range(0, len(explored_nodes)): 			#loop executed for the length of nodes in 'explored_nodes'
				transposed_nodes = explored_nodes[i].transpose()  	#transposed to write the data in expected format
				string_val = self.nod2str(transposed_nodes) 		#data written as string
				fileopen.write("%s \n" % string_val) 			#writing in new line
			fileopen.close() 						#closing the file
	### This function converts the array to a string list which helps in faster computation
	def arr2str(self, conv_node): 							#The argument 'conv_node' is passed into the function to convert node to string in the form of list
		data = ''
		for i in conv_node:
			for j in i:
				data += str(j) 						#storing the data in the string form
		return data  								#The data is written to respective calling function

### Initializing the variables with initial values below
Nodes = []
Iden_Numb = 1
cost_val = 0
Inf_Nodes = []
Str_Node_set = set()
Goal_State_Node = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])				#Goal node initialization

###The Main function for the 8-puzzle problem
puzzle_main()

