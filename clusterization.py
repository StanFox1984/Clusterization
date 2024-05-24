class NamedObject:
	def __init__(self, name):
		self.name = name

	def getName(self):
		return self.name

class Metric(NamedObject):
	def __init__(self, name, value):
		super().__init__(name)
		self.value = value

	def getValue(self):
		return self.value

class MeteredObject(NamedObject):
	def __init__(self, name):
		super().__init__(name)
		self.metrics = { }

	def getMetrics(self):
		return self.metrics

	def addMetric(self, m):
		self.metrics[m.getName()] = m

	def __repr__(self):
		s = self.getName()
		for metric in self.metrics:
			s += " "+ metric + ":" + str(self.metrics[metric].getValue())
		return s


class MeteredObjectSet(NamedObject):
	def __init__(self, name, objects = None):
		super().__init__(name)
		self.objects = objects
		self.metric_names = { }
		self.clusters = { }

	def addObject(self, o):
		self.objects.append(o)

	def getMetricNames(self):
		for o in self.objects:
			metrics = o.getMetrics()
			for m in metrics:
				if not m in self.metric_names:
					self.metric_names[m] = True

	def getAverageDeltaForMetric(self, metric_name, objs):
		total_delta = 0
		prev_value = None
		total_objects_with_metric = 0
		for o in objs:
			metrics = o.getMetrics()
			if metric_name in metrics:
				total_objects_with_metric += 1
				value = metrics[metric_name].getValue()
				if prev_value != None:
					total_delta += abs(prev_value - value)
				prev_value = value

		return total_delta / total_objects_with_metric

	def createMetricClusters(self, metric_name):
		if metric_name in self.clusters:
			clusters = self.clusters[metric_name][0]
		else:
			clusters = [ ]

		objects_clustered = 0

		objs = [ o for o in self.objects if metric_name in o.getMetrics() ]
		objs.sort(key = lambda o: o.getMetrics()[metric_name].getValue())

		average_delta = self.getAverageDeltaForMetric(metric_name, objs)

		for o in objs:
			metrics = o.getMetrics()
			if metric_name in metrics:
				value = metrics[metric_name].getValue()
				found = False
				for cluster in clusters:
					for cluster_object in cluster:
						cluster_object_value = cluster_object.getMetrics()[metric_name].getValue()
						if abs(value - cluster_object_value) <= average_delta:
							found = True
							break
					if found == True:
						if not o in cluster:
							cluster.append(o)
						break

				if found == False:
					cluster = [ ]
					cluster.append(o)
					clusters.append(cluster)

				objects_clustered += 1

		return (clusters, objects_clustered)


	def clusterize(self):
		self.getMetricNames()
		for metric_name in self.metric_names:
			clusters = self.createMetricClusters(metric_name)
			# use average amount of objects per cluster as a criteria of how valuable that metric is
			# less objects per cluster, means data are not very dense according to this metric
			# meaning values are lying pretty far from each other and information value of being
			# in particular cluster isn't very high.
			self.clusters[metric_name] = ( clusters[0], clusters[1]/len(clusters[0]))

	def add_object(self, o):
		for metric_name in self.metric_names:
			
			average_delta = self.getAverageDeltaForMetric(metric_name)
			for cluster in self.clusters[metric_name][0]:
				for cluster_object in cluster:
					value = o.getMetrics()[metric_name].getValue()
					cluster_object_value = cluster_object.getMetrics()[metric_name].getValue()
					if abs(value - cluster_object_value) <= average_delta:
						if not o in cluster:
							cluster.append(o)


	def get_clusters_sorted(self):
		return sorted([ self.clusters[metric_name] for metric_name in self.clusters ],
			      key = lambda cluster: cluster[1], reverse = True)


human1 = MeteredObject("human1")
human2 = MeteredObject("human2")
human3 = MeteredObject("human3")
human4 = MeteredObject("human4")

human1.addMetric(Metric("color", 1))
human2.addMetric(Metric("color", 2))
human3.addMetric(Metric("color", 4))
human4.addMetric(Metric("color", 5))

human1.addMetric(Metric("age", 1))
human2.addMetric(Metric("age", 20))
human3.addMetric(Metric("age", 400))
human4.addMetric(Metric("age", 700))


s = MeteredObjectSet("set", [ human1, human2, human3, human4 ])

s.clusterize()

human5 = MeteredObject("human5")
human5.addMetric(Metric("age", 70000))
s.addObject(human5)

s.clusterize()

print (s.clusters)
print (s.get_clusters_sorted())
