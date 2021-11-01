import math  #this is not an external library 
import random 
from queue import PriorityQueue
from typing import OrderedDict


"""constants""" 

#env file 
filename = "001.env"
#obstacle array
BOUNDS =[]# X_low,X_high,y_low,y_high the limit of the word area
obstacle_count = 0
obstacles = []
tree = [] #an empty list that will store the nodes 
edges = [] # after the taget is found the edges can be fed in
step = 2.0 #when generating new nodes how far from the current node 
end_reached = False #calls the program to end 

"""Method declarations"""

"""data loading and writing methods """
#this method loads up the variable provided regarding the environment as a ".env"
#the format of the input expected 
#Boundary: xlow : xhigh; ylow : yhigh
#n :Number of obstacles
#x1 y1 radius1
#...
#xn yn radiusn
def read_env_file(filename,_obstacles,_bounds):
    f = open(filename,"r")
    content = f.read()
    content_list = content.splitlines()
    for i in range(0,len(content_list)):
        line = content_list[i]
        #print(line)
        if(i == 0):
            # it the first line with the boundary
            line = line.replace(";",":")
            things = line.split(":")
            #print(things)
            #_bounds = int(things[1]),int(things[2]),int(things[3]),int(things[4])
            for x in range(1,5):
                _bounds.append(int(things[x]))
            #print(BOUNDS)
            continue
        if(i == 1):
            # its the second line with the number of obstacles 
            obstacle_count = int(line)
            continue  
        line = line.split(" ")
        #print(line)
        temp = Obstacle(line[0],line[1],line[2])
        #print(temp.__str__())
        _obstacles.append(temp)
        
    
    #print(len(_obstacles))
    #print(len(content_list)) 
    #print(obstacle_count)
    pass

# this method will out put the generated tree to a .map file 
# if file exists delete and save new  
def write_result(edges_count,nodes_count,path):
    sol = open("001.map","w")
    sol.write("Number of nodes({0}) Number of edges({1})\n".format(nodes_count,edges_count))
    sol.write(path)
    pass

"""Node manipulation methods """

def dist_to_node(n1, n2):
    return dist(n1.get_coords(), n2.get_coords())


def dist_to_point(n, p):
    return dist(n.get_coords(), p)


def dist(p1, p2):
    x, y = p1[0], p1[1]
    xx, yy = p2[0], p2[1]
    return math.hypot(x - xx, y - yy)


def add_edge(n1, n2):
    n1.add_neighbour(n2)
    n2.add_neighbour(n1)


def remove_edge(n1, n2):
    del n1.adj[n2]
    del n1.edge[n2]
    del n2.adj[n1]
    del n2.edge[n1]


#generates proints from the given node in random directions
def generate_node(current_node):
    _y = current_node.get_y()
    _x = current_node.get_x()
    new_y = random.randint(-step,step+1)
    new_x = random.randint(-step,step+1)
    temp_node = Node(_x+new_x,_y+new_y)
    return temp_node

# this method will pick an new node and check for collions in the obstacle set
def check_collision(new_node):
    # check for collisons with the bounds as well 
    #BOUNDS =[]# X_low,X_high,y_low,y_high the limit of the word area
    
    node_point = new_node.get_coords()# (x,y)
    if(node_point[0] <= BOUNDS[0] or node_point[0] >= BOUNDS[1] or node_point[1] <= BOUNDS[2] or node_point[1] >= BOUNDS[3] ):
        #print("out of bound, (",node_point,")")
        return True

    for obst in obstacles:# loops through the obstacles looking for collisons 
        point = obst.get_coords()
        #node_point = new_node.get_coords()
        #print(point,node_point)
        distance = dist(node_point,point)
        #print(distance)
        if distance < obst.get_rad():
            #print("There was a collision, ",node_point)
            return True
        
    return False

def goal_reached(current_node,goal):
    radius = 1.0 # how close a node should be to register the goal as reached 
    point = current_node.get_coords()
    goal_point =  goal.get_coords()
    distance = int(dist(point,goal_point)) #converting this to int this rounds off the actual distance to the goal but in turn increases the speed of the check
    #print(distance)
    if distance <= radius:
        print("Goal reached",distance,"current position", point)
        return True
    #print("missed dist to goal ",distance,"currently at ", point)    
    return False    



def get_the_path(visited,current,came_from):
    path = "\n"
    print(len(came_from))
    print("total edges added ",len(edges))
    print("Total nodes visited",len(visited))
    #print(current in came_from)
    while current in came_from:
        
        previous_step = came_from[current]
        #print(current," came from ",previous_step)
        path = "({0}) \t ({1}) \n".format(str(previous_step),str(current)) + path
        current = previous_step
    
    write_result(len(edges),len(visited),path)
    #print(path)
def est_implementation(start,end):
    count = 0
    neighbor_count = 4 # how many neighbors per addition 
    checked = []
    # the layout    f_score , index , node  
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}    
    visited = []
    g_score = { start : 0}    
    f_score = { start : dist_to_node(start,end)}

    
    open_set_hash = {start}
   

    while not open_set.empty():
        current = open_set.get()[2]
        #print(current)
        open_set_hash.remove(current)
        if not current in g_score:
            #print("didnt happen",current)
            g_score[current] = float("inf")
        if goal_reached(current,end) :
            visited.append(current)
            came_from[end] = current
            get_the_path(visited,end,came_from)            
            pass
            return True
        
        # you could generate neighbors here 
        for i in range(0 , neighbor_count +1 ):
            new_node = generate_node(current) # generate new node 
            
            while(check_collision(new_node)): # generate new nodes until they dont collide with anything
                """if(not check_collision(new_node)):
                    current.add_neighbour(new_node)
                    if not new_node in g_score:
                        g_score[new_node] = float("inf")
                else:"""
                #print("node requested ",new_node)
                new_node = generate_node(current)

            
            current.add_neighbour(new_node,edges)
            came_from[new_node] = current
            if not new_node in g_score:
                g_score[new_node] = float("inf")

        for neighbor in current.adj :
            temp_g_score  = g_score[current] + 1 
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + dist_to_node(neighbor,end)
                if(neighbor not in open_set_hash):
                    count = count + 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

                    if( neighbor in visited):
                        visited.remove(neighbor)

        if(current != start):
            visited.append(current)


        #print("so far so good ")
    return False    
    
    """
    # the loop entry might be here 
    while count < 3:
        count = count + 1
        new_node = generate_node(current)
        #print(new_node)
        if(not check_collision(new_node)):
            
            end_reached = goal_reached(new_node,end)
            current.add_neighbour(new_node) # if the new node is valid add it to the nodes neighbors
            print(len(current.get_connections()))
            #print(edges[0])
    """



    


"""Class declararions"""

class Node:
    #def __init__(self,_x,_y,_id):
    
    def __init__(self,_x,_y):
        self.x = float(_x) #x position
        self.y = float(_y) #y position
        #self.id =  "'_x':_y" # identifier 
        self.adj = {} #neighbors 
        self.edge = {} # edges 
        pass

    def get_x(self):
        return float(self.x)

    
    def get_y(self):
        return float(self.y)   

    def get_coords(self): # gets teh coordinates of the node 
        return self.x, self.y

    def add_neighbour(self, neighbour,_edges):
        self.adj[neighbour] = self.__euclidean_dist(neighbour)
        self.edge[neighbour] = NodeEdge(self, neighbour)
        #edges.append(NodeEdge(self, neighbour))
        _edges.append(NodeEdge(self, neighbour))
        

    def __euclidean_dist(self, neighbour): # the distance between this node and another 
        return math.hypot((self.x - neighbour.x), (self.y - neighbour.y))

    def get_connections(self): # all the neighbors you can travel to 
        return self.adj.keys()

    def get_weight(self, neighbour):# the weight of travelling to that neighbor 
        return self.adj[neighbour]

    def __str__(self): # express the node as a string 
        return f"{self.x}, {self.y}"

     


class Obstacle:
    def __init__(self,x,y,radius):
        self.x = float(x)
        self.y = float(y)
        self.rad = float(radius)  
        pass

    def get_coords(self): # gets teh coordinates of the node 
        return self.x, self.y

    def get_x(self):
        return self.x

    
    def get_y(self):
        return self.y   

    def get_rad(self):
        return self.rad             

    def __str__(self):
        return f"{self.x}, {self.y}, {self.rad}"

#describes an edge
class NodeEdge:
    def __init__(self, node_from: Node, node_to: Node):
        self.nfrom = node_from
        self.nto = node_to

    def __str__(self) -> str:
        return "There is an edge from ",self.nfrom.get_coords()," to ",self.nto.get_coords()
       


"""main entry """

if __name__ == '__main__':
#An implementation of the main method allowing the rest of the code to exist in methods  
    #read the file and load the values 
    read_env_file(filename,obstacles,BOUNDS)
    #print(len(obstacles))
    start_node = Node(-50,-100) # these can be randomised 
    goal_node = Node(100,100)
    #ensure the goal is in the bounds for optimisation.
    node_point = goal_node.get_coords()
    if(node_point[0] < BOUNDS[0] or node_point[0] > BOUNDS[1] or node_point[1] < BOUNDS[2] or node_point[1] > BOUNDS[3] ):
        print("out of bound, (",node_point,")")
        exit()
        
    est_implementation(start_node,goal_node)

   # n2 = Node(5,9)
    #n3 = Node(8,12)
    #obst_1 = Obstacle(10,10,5)
    #print(dist_to_node(n3,n2))