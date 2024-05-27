class Node:
	def __init__(self, name, value = None):
		self.name = name
		self.value = value
		self.connections = [ ]

	def connect(self, node, connect_back = True):
		self.connections.append((node, node))
		if connect_back:
			node.connect(self, False)

	def __repr__(self):
		return self.name

	def get_shortest_paths(self, paths = { }, path = [ ]):
		if len(path) == 0:
			path.append(self)
		for connection in self.connections:
			if connection[0] in path:
				continue
			new_path = list(path)
			new_path.append(connection[0])
			if not connection[0].name in paths:
				paths[connection[0].name] = (new_path, len(new_path))
			else:
				if len(new_path) < paths[connection[0].name][1]:
					paths[connection[0].name] = (new_path, len(new_path))
			connection[0].get_shortest_paths(paths, new_path)





a = Node("A")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")


a.connect(b)
a.connect(c)
b.connect(c)
c.connect(d)
e.connect(d)
b.connect(e)

paths = {}
a.get_shortest_paths(paths)

print (paths)





