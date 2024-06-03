class Node:
	PrintDebugs = False

	def __init__(self, name, data = None):
		self.name = name
		self.data = data
		self.connections = [ ]
		self.connection_value_map = { }

	def connect(self, node, value = 1, connect_back = True):
		if not node in self.connections:
			self.connections.append(node)
		self.connection_value_map[node.name] = value
		if connect_back:
			node.connect(self, value, False)

	def get_connection_value(self, node):
		if not node.name in self.connection_value_map:
			return None

		return self.connection_value_map[node.name]

	def __repr__(self):
		return self.name

	def get_path_heuristic_value(path):
		value = 0
		prev_node = None
		for node in path:
			if prev_node != None:
				v =  prev_node.get_connection_value(node)
				if v == None:
					if Node.PrintDebugs:
						print ("None value between ", prev_node, node, "path ", path)
				else:
				   value += v
			prev_node = node

		if Node.PrintDebugs:
			print ("Heuristic value for path ", path, " is ", value)
		return value

	def get_shortest_paths(self, paths = { }, path = [ ]):
		if len(path) == 0:
			path.append(self)
		for node in self.connections:
			if node in path:
				continue
			new_path = list(path)
			new_path.append(node)
			if Node.PrintDebugs:
				print ("Added ", node, "to path", new_path)
			value = len(new_path) * Node.get_path_heuristic_value(new_path)
			if not node.name in paths:
				paths[node.name] = ([new_path], value)
			else:
				if value < paths[node.name][1]:
					paths[node.name] = ([new_path], value)
				if value == paths[node.name][1]:
					equal_paths = paths[node.name][0]
					if not new_path in equal_paths:
						equal_paths.append(new_path)
					paths[node.name] = (equal_paths, value)
			node.get_shortest_paths(paths, new_path)

	def get_spanning_tree(nodes, rev = False):
		path_maps = { }
		node_pairs = { }

		for node in nodes:
			if Node.PrintDebugs:
				print ("Getting shortest paths for node", node)
			paths = { }
			node.get_shortest_paths(paths, [ ])
			path_maps[node.name] = paths

		for node1 in nodes:
			for node2 in nodes:
				if not node2.name in path_maps[node1.name]:
					continue

				edge_name = "[ " + node1.name + " , " + node2.name + " ]"
				edge_name_rev = "[ " + node2.name + " , " + node1.name + " ]"
				if not edge_name in node_pairs and not edge_name_rev in node_pairs:
					if not rev:
						node_pairs[edge_name] = path_maps[node1.name][node2.name]
					else:
						node_pairs[edge_name_rev] = path_maps[node2.name][node1.name]


		return node_pairs



a = Node("A")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")


# if value was 1, best route to "e" from "A" would have been A, b, e
# now it should be a, c, b, e, despite more edges on the way, cost
# of the connection between a <-> b is too high..
a.connect(b, 200)
#a.connect(b, 1)
a.connect(c, 1)
b.connect(c, 1)
c.connect(d, 1)
e.connect(d, 1)
b.connect(e, 1)

paths = {}

#Node.PrintDebugs = True

#a.get_shortest_paths(paths)

#print (paths)

print (Node.get_spanning_tree([a,b,c,d,e]))

print (Node.get_spanning_tree([a,b,c,d,e], True))





