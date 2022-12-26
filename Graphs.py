
import pygame
from pygame.locals import *
import queue, math
import time
import pygame, os 


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
BackGround = Background('Back.png', [0,0])

os.environ['SDL_VIDEO_CENTERED'] = '1'
red   = (255, 0 ,0  )
grey  = (127,127,127)
blue  = (0  , 0 ,255)
white = (0,0,1)
green = (0  ,255,0  )
black = (0  ,0  ,0  )
yellow= (255,255,0  )
EdgeThickness = 3

class Edge():
	
	def __init__(self, color, node1, node2, weight):
		self.color     = color
		self.node1     = node1
		self.node2     = node2
		self.weight    = weight
	
	def Draw(self, window):
		pygame.draw.lines(window,self.color, True, [self.node1.center, self.node2.center], EdgeThickness)
		x1, y1 = self.node1.center
		x2, y2 = self.node2.center

		slope = float(y2 - y1)/((x2 - x1)+.00001)
		_slope = float(x2 - x1)/((y2 - y1)+.00001)
		sign_x = math.copysign(1, x1 - x2)
		sign_y = math.copysign(1, (y1 - y2)*slope)

		if slope > -10 and slope < 10 :
			x = x2 + sign_x * (20.0 / math.sqrt(1 + slope**2))
			y = y2 + sign_y * (slope * 20.0) / math.sqrt(1 + slope**2)
		else :
			x = x2 + sign_x * (_slope * 20.0) / math.sqrt(1 + _slope**2)
			y = y2 + sign_y * 20.0 / math.sqrt(1 + _slope**2)
		x = int(x)
		y = int(y)
		r = int(self.node2.radius/2)
		if self.node1.index == self.node2.index:
			pygame.draw.circle(window, (0,0,0), (x,y),r,0)
		else :
			pygame.draw.circle(window, blue, (x,y),r,0)
		myfont = pygame.font.SysFont('Comic Sans MS', 15)
		textsurface = myfont.render(str(self.weight), False, white)
		window.blit(textsurface,((self.node1.center[0]+self.node2.center[0])/2, (self.node1.center[1]+self.node2.center[1])/2))

	def SetColor(self, window, color):
		pygame.draw.lines(window, grey, True, [self.node1.center, self.node2.center], EdgeThickness)
		myfont = pygame.font.SysFont('Comic Sans MS', 15)
		textsurface = myfont.render(str(self.weight), False, white)
		window.blit(textsurface,((self.node1.center[0]+self.node2.center[0])/2, (self.node1.center[1]+self.node2.center[1])/2))

	def __lt__ (self, other):
		return self.weight < other.weight
	

class Node():
	def __init__(self, color, center, radius, thickness,index):
		self.color     = color
		self.center    = center 
		self.radius    = radius
		self.thickness = thickness
		self.edges     = []
		self.index = index

	def Draw(self, window):
		pygame.draw.circle(window, self.color, self.center,self.radius,0)
		myfont = pygame.font.SysFont('Comic Sans MS', 25)
		textsurface = myfont.render(str(self.index), False, black)
		window.blit(textsurface,(self.center[0]-10,self.center[1]-15))
		
	def SetColor(self, window, color):
		pygame.draw.circle(window, color, self.center,self.radius,0)
		myfont = pygame.font.SysFont('Comic Sans MS', 25)
		textsurface = myfont.render(str(self.index), False, white)
		window.blit(textsurface,(self.center[0]-10,self.center[1]-15))
	
	def AddEdge(self, node2, weight):
		self.edges.append(Edge(red,self, node2,weight)) 
	def GetColor(self):
		return self.color;
	
def Answer(window,color,ans):
	myfont = pygame.font.SysFont('Comic Sans MS', 100)
	textsurface = myfont.render(ans, False, color)
	window.blit(textsurface,(250,500))

class GraphVisualization():
	def __init__(self):
		pygame.init()
		pygame.font.init() 
		window = pygame.display.set_mode([1500,700])
		pygame.display.update()#
		self.myfont = pygame.font.SysFont('Comic Sans MS', 15)
		fname = 'input100.txt'
		#print(connection)
		f = open(fname,'r')
		x = f.seek(10)
		w = [int(x) for x in next(f).split()]
		w = w[0]
		print(w)
		inputnodes = []
		connection = []
		
		x = f.seek(14 + len(str(w)))

		for i in range(w):
	
			index, x,y  = [float(x) for x in next(f).split()]
			inputnodes.append([int(x*1300)+25,int(y*1000)+50])
		x = f.read(1)
		for i in range(w):
			
			vertex =  f.read(1)
			f.read(1)
			x = next(f).split('\t')
			
			for i in range (int(len(x)/4)):
				if x[i*4] == '':
					del x[i*4]
				arr = [int(vertex),int(x[i*4]),int(float(x[i*4+2])/1000000)]
			
				connection.append(arr)
	
		window.blit(BackGround.image, BackGround.rect)
		pygame.display.update()

		called = False
		while True:
			window.fill([255, 255, 255])
			nodes = []

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					quit()

    #(window,color,starting point(centre),radius,thickness)
			for index,node in enumerate(inputnodes):
				tempnode = Node(blue, node,20,1,index)
				nodes.append(tempnode)
				tempnode.Draw(window)

			for edge in connection:
				nodes[edge[0]].AddEdge(nodes[edge[1]],edge[2])
			
			for tempnode in nodes:
				for ed in tempnode.edges:
					ed.Draw(window)
			for tempnode in nodes:
				tempnode.Draw(window)
			if not called:
				#Dijkstra(nodes, 5, pygame.display.set_mode([1500,700]))
				#pygame.display.update()
				#Kruskal(nodes, pygame.display.set_mode([1500,700]))
				#pygame.display.update()
				#BellmanFord(nodes, 5, pygame.display.set_mode([1500,700]))
				#pygame.display.update()
				#FloydWarshall(nodes, pygame.display.set_mode([1500,700]))
				#pygame.display.update()
				Prims(nodes,5,pygame.display.set_mode([1500,700]))
				pygame.display.update()
				called = True


def Dijkstra(graph, source, window):
	global blue
	visited = [False]*len(graph)
	weights = [math.inf]*len(graph)

	pq = queue.PriorityQueue()
	graph[source].SetColor(window,blue)
	pq.put((0, source))
	weights[source] = 0
	final_edges = [None]*len(graph)
	visited[source] = True

	while not pq.empty():

		temp = pq.get()
		w = temp[0]
		v = temp[1]
		visited[v] = True

		for e in graph[v].edges:
			u = e.node2.index
			if not visited[u] and weights[u] > w + e.weight:
				weights[u] = w + e.weight
				final_edges[u] = e
				pq.put((weights[u], u))

	for i in range(len(graph)):
		if i != source:
			final_edges[i].SetColor(window, blue)
	for tempnode in graph:	
		tempnode.Draw(window)

	print("Disjkstra: ", weights)
	weights = [i for i in weights if i != math.inf]
	print("total: ",sum(weights))
	Answer(window,white,"Dijkstra")
	return 


def find(parent, v):
	if parent[v] == -1:
		return v

	return find(parent, parent[v])

def union(parent, u, v):
	x = find(parent, u)
	y = find(parent, v)
	parent[x] = y

def Kruskal(graph, window):
	global blue
	window.fill([255, 255, 255])
	window.blit(BackGround.image, BackGround.rect)
	edges = []
	parent = [-1]*(len(graph))

	for v in graph:
		for e in v.edges:
			edges.append(e)

	edges.sort(key= lambda x : x.weight)
	
	total_cost = 0
	for e in edges:
		if find(parent, e.node1.index) != find(parent, e.node2.index):
			e.SetColor(window, blue)
			union(parent, e.node1.index, e.node2.index)
			total_cost += e.weight
	print("Kruskal")
	print("total_cost: ",total_cost)
	for tempnode in graph:	
		tempnode.Draw(window)
	ans = "Kruskal: MST Cost: " + str(total_cost)
	Answer(window,white,ans)

def Prims(graph, source, window):
	global blue
	window.fill([255, 255, 255])
	window.blit(BackGround.image, BackGround.rect)
	edges = []
	parent = [-1]*(len(graph))
	nodes = []
	nodes.append(graph[source])
	for e in graph[source].edges:
		edges.append(e)
	edges.sort(key= lambda x : x.weight)
	cost = 0
	while edges != []:
		e = edges[0]
		if find(parent, e.node1.index) != find(parent, e.node2.index):
			e.SetColor(window, green)
			cost = cost + e.weight
			union(parent, e.node1.index, e.node2.index)
			for e in e.node2.edges:
				edges.append(e)
			edges.sort(key= lambda x : x.weight)
		else:
			edges.remove(e)
	ans = "PRIMS : Mst cost : " + str(cost)
	for tempnode in graph:	
		tempnode.Draw(window)
	graph[source].SetColor(window,blue)
	Answer(window,white,ans)
	print(ans)
	pygame.display.update()
		
	


def BellmanFord(graph, source, window):
	global blue
	window.fill([255, 255, 255])
	window.blit(BackGround.image, BackGround.rect)
	Answer(window,white,"BellmanFord")
	V = len(graph)
	edges = []
	for v in graph:
		for e in v.edges:
			edges.append(e)

	weights = [math.inf] * V
	weights[source] = 0
	graph[source].SetColor(window,blue)
	final_edges = [None] * V

	for i in range(V-1):
		for edge in edges:
			x = edge.node1.index
			y = edge.node2.index
			if weights[y] > weights[x] + edge.weight:
				final_edges[y] = edge
				weights[y] = weights[x] + edge.weight

	for edge in edges:
		x = edge.node1.index
		y = edge.node2.index
		if weights[y] > weights[x] + edge.weight:
			print("IMPOSSIBLE")
			return

	print("BellmanFord: ", weights)
	weights = [i for i in weights if i != math.inf]
	print("Total: ", sum(weights))

	for i in range(V):
		if i != source:
			final_edges[i].SetColor(window, red)
	for tempnode in graph:	
		tempnode.Draw(window)

def FloydWarshall(graph, window):
	window.fill([255, 255, 255])
	window.blit(BackGround.image, BackGround.rect)

	V = len(graph)
	weight = [[math.inf for i in range(V)] for i in range(V)]
	Pi = [[None for i in range(V)] for i in range(V)]

	for v in graph:
		for e in v.edges:
			weight[e.node1.index][e.node2.index] = e.weight
	
	for i in range(V):
		weight[i][i] = 0

	for k in range(V):
		for i in range(V):
			for j in range(V):
				if weight[i][j] > weight[i][k] + weight[k][j]:
					weight[i][j] = weight[i][k] + weight[k][j]
					Pi[i][j] = k
	
	print("Weights")
	total_cost = 0
	for i in range(V):
		for j in range(V):
			if weight[i][j] != math.inf:
				total_cost += weight[i][j]

			#print(weight[i][j], end="\t")
		#print()
	print("Parents")
	#for i in range(V):
	#	for j in range(V):
	#		pass#print(Pi[i][j], end="\t")
	#	print()

	print("FloydWarshall COST: ", total_cost)
	Answer(window,white,str("FloydWarshall total cost : ")+str(total_cost))

if __name__ == "__main__":
    app = GraphVisualization()
