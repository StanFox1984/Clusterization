


class AssociationObject:
	full_set = { }
	def __init__(self, name, class_id):
		self.name = name
		self.class_id = class_id
		self.associations = { }
		if not class_id in AssociationObject.full_set:
			AssociationObject.full_set[class_id] = [ ]
		AssociationObject.full_set[class_id].append(self)

	def associate(self, obj, associate_back = True):
		if not obj.class_id in self.associations:
			self.associations[obj.class_id] = [ ]

		self.associations[obj.class_id].append(obj)

		if associate_back:
			obj.associate(self, False)

	def get_unassociated_with_class_id_by_class_id(with_class_id, by_class_id):
		a = [ ]
		if not with_class_id in AssociationObject.full_set:
			return None

		for o in AssociationObject.full_set[with_class_id]:
			res = o.get_association_by_class_id(by_class_id)

			if res == None:
				a.append(o)

		if len(a) > 0:
			return a

		return None

	def get_association_by_class_id(self, class_id, prev_objs = [ ]):
		a = [ ]

		if class_id in self.associations:
			for o in self.associations[class_id]:
				a.append(o)

		for association_class_id in self.associations:
			for o in self.associations[association_class_id]:
				if o in prev_objs:
					continue

				new_prev_objs = list(prev_objs)
				new_prev_objs.append(self)

				res = o.get_association_by_class_id(class_id, new_prev_objs)
				if res != None:
					a.extend(res)

		if len(a) > 0:
			return a

		return None



human1 = AssociationObject("human1", "humans")
human2 = AssociationObject("human2", "humans")
human3 = AssociationObject("human3", "humans")

redshirt = AssociationObject("redshirt", "shirts")
blueshirt = AssociationObject("blueshirt", "shirts")
whiteshirt = AssociationObject("wteshirt", "shirts")

honda = AssociationObject("honda", "cars")
toyota = AssociationObject("toyota", "cars")
bmw = AssociationObject("bmw", "cars")
mazda = AssociationObject("mazda", "cars")

human1.associate(redshirt)
human2.associate(blueshirt)

whiteshirt.associate(bmw)
human3.associate(bmw)

human1.associate(honda)
blueshirt.associate(toyota)

#mazda.associate(human3)



print (human3.get_association_by_class_id("shirts")[0].name)
print (redshirt.get_association_by_class_id("cars")[0].name)
print (AssociationObject.get_unassociated_with_class_id_by_class_id("cars", "shirts")[0].name)

