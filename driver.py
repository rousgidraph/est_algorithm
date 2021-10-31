from solution import *


"""main entry """

if __name__ == '__main__':
#An implementation of the main method allowing the rest of the code to exist in methods  
    #read the file and load the values 
    read_env_file(filename,obstacles,BOUNDS)
    start_node = Node(1,0) 
    goal_node = Node(2,0)
    est_implementation(start_node,goal_node)
