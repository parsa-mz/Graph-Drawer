import Main
import pygame

INF = 101010101

class GraphMatrix(): 
	def __init__(self, vertices, edges, weights): 
		self.V = len(vertices)
		self.vertexes = vertices
		self.edges = edges
		self.weights = weights
		self.parent = [-1 for v in range(self.V)] 
		self.graph = self.init_graph(self.edges, self.weights)
		#[[0 for column in range(self.V)] 
					#for row in range(self.V)] 

	def init_graph(self, edges, weights):
		g = [[INF for column in range(self.V)] 
					for row in range(self.V)]
		for i in range(len(edges)):			
			g[edges[i][0]][edges[i][1]] = g[edges[i][1]][edges[i][0]] = int(weights[i].get_text())
		return g

	def printMST(self, adding_order):
		print ("Prim:") 
		print ("Edge \tWeight")
		for i in range(1, len(adding_order)):
			u = int(adding_order[i])
			print(self.parent[u], "-", u, "\t", self.graph[u][ self.parent[u] ])
			

	def primMST(self, start):
		visited, key= [], []

		# initialize 
		for i in range(self.V):
			visited.append(False)
			key.append(INF)
		
		# relaxing start node
		key[start] = 0
		
		adding_order = []

		for c in range(self.V):
			# u: nearest node not in current mst
			# minn: nearest node weight not in current mst 
			u, minn = -1, INF
			# find nearest node
			for i in range(self.V):
				if visited[i] == False and key[i] < minn:
					minn = key[i]
					u = i
			# if we have not connected return false
			if minn == INF:
				self.draw_text("Graph doesn't have MST !", 'red')
				print("Graph doesn't have MST !")
				return

			# else visit node and add to mst
			visited[u] = True
			adding_order.append(u)
			if self.parent[u] != -1:
				self.draw_edge(u, self.parent[u], 'blue')

			# relax nodes adjacent weights
			for v in range(self.V):
				if self.graph[u][v] != INF and visited[v] == False and self.graph[u][v] < key[v]:
					key[v] = self.graph[u][v]
					self.parent[v] = u
		
		self.draw_text("Graph's MST: ", 'white')
		self.printMST(adding_order)

	# draw edge
	def draw_edge(self, i, j, color):
		pygame.draw.line(Main.screen, pygame.Color(color), self.vertexes[i], self.vertexes[j], 2)
		Main.screen_update() 
		pygame.time.wait(1000)

	# draw text
	def draw_text(self, message, color):
		font = pygame.font.SysFont("lucida sans", 18, bold=True)
		word = Main.font.render(message, 0, pygame.Color(color))
		Main.screen.blit(word, (20,20))
		Main.screen_update() 


class GraphK: 
	def __init__(self,vertices, edges, weights): 
		self.V= len(vertices)
		self.vertexes = vertices
		self.edges = edges
		self.weights = weights
		self.result = []
		self.graph = self.init_graph(self.edges, self.weights)

	def init_graph(self, edges, weights):
		g = []
		for i in range(len(edges)):
			g.append( [edges[i][0], edges[i][1], int(weights[i].get_text())] )
		return g

	# add edge to graph 
	def add_edge(self,u,v,w): 
		self.graph.append([u,v,w]) 

	# A utility function to find set of an element i 
	def find(self, parent, i): 
		if parent[i] == i: 
			return i 
		return self.find(parent, parent[i]) 

	# A function that does union of two sets of x and y 
	def union(self, parent, rank, x, y): 
		xroot = self.find(parent, x) 
		yroot = self.find(parent, y) 

		# Attach smaller rank tree under root of high rank tree 
		if rank[xroot] < rank[yroot]: 
			parent[xroot] = yroot 
		elif rank[xroot] > rank[yroot]: 
			parent[yroot] = xroot 

		# If ranks are same, then make one as root  
		else : 
			parent[yroot] = xroot 
			rank[xroot] += 1

	# draw edge
	def draw_edge(self, i, j, color):
		pygame.draw.line(Main.screen, pygame.Color(color), self.vertexes[i], self.vertexes[j], 2)
		Main.screen_update() 
		pygame.time.wait(1000)
	
	# draw text
	def draw_text(self, message, color):
		font = pygame.font.SysFont("lucida sans", 18, bold=True)
		word = Main.font.render(message, 0, pygame.Color(color))
		Main.screen.blit(word, (20,20))
		Main.screen_update() 


	def KruskalMST(self): 
		i = 0 # index for sorted edges 
		e = 0 # index for result[] 

		# sort all edge from low to high
		self.graph = sorted(self.graph,key=lambda item: item[2]) 

		parent, rank = [], [] 

		# create V subsets with single elements 
		for node in range(self.V): 
			parent.append(node) 
			rank.append(0) 
	
		while i < len(self.graph) : 
			# pick the smallest edge in inventory
			u,v,w = self.graph[i] 
			i = i + 1
			x = self.find(parent, u) 
			y = self.find(parent ,v) 

			# if edge doesn't make cycle add it to result 
			if x != y: 
				e = e + 1	
				self.result.append([u,v,w])
				self.draw_edge(u, v, 'blue') 
				self.union(parent, rank, x, y)			 
		
		if e < self.V - 1:
			self.draw_text("Graph doesn't have MST !", 'red')
			return 

		self.draw_text("Graph's MST:", 'white')
		self.printMST()

	def printMST(self)	:
		print ("Kruskal:")
		print ("Edge \tWeight")
		for u,v,weight in self.result: 
			print ("%d - %d\t %d" % (u,v,weight)) 



if __name__ == "__main__":
	g = GraphMatrix(6) 
	g.add_edge(0, 1, 10) 
	g.add_edge(0, 2, 6) 
	g.add_edge(0, 3, 5) 
	g.add_edge(1, 3, 15) 
	g.add_edge(2, 3, 4)
	g.add_edge(4, 5, 1)  

	g.primMST()
	
	'''
	g = GraphK(6) 
	g.KruskalMST() 
	'''

