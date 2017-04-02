# this .py file is used to eliminate the duplicated vertices in the original .obj file
import numpy
from sets import Set

vertices = []
faces = []
# epsilon used for deciding if two vertices are the same
epsilon = 0.1

class vertex:
	def __init__(self):
		self.pos = []
	def __eq__(self, other):
		if isinstance(other, vertex):
			return distance2(other.pos, self.pos) < epsilon

class face (object):
	def __init__(self):
		self.indices = []

def strArr2floatArr (strArr):
	result = []
	for s in strArr:
		result.append(float(s))
	return result

def norm2 (a):
    return dot(a, a)

def dot ( a, b ):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def distance2 (a, b):
	return norm2(map(lambda a,b:a-b, a,b))

def addVertex ( vv ):
	# check if already exists
	isExist = False
	for v in vertices:
		if v == vv:
			isExist = True
	if isExist == False:
		vertices.append(vv)

# get the real index in the non-duplicated list
def getNewIndex ( vv ):
	for index, v in enumerate(vertices):
		if v == vv:
			return index
	return -1

def convert(filename):
	file = open(filename)
	# store all the vertices in the file
	origin_vertices = []
	for line in file:
		#print(line)
		tokens = line.split(' ')
		if tokens[0] == 'v':
			v = vertex()
			v.pos = strArr2floatArr(tokens[1:4])
			origin_vertices.append(v)
			# add the non-duplicated vertices into the list
			addVertex(v)
		elif tokens[0] == 'f':
			ff = face()
			for t in tokens[1:]:
				triple = t.split('/')
				index = int(triple[0])
				newIndex = getNewIndex(origin_vertices[index - 1])
				#print(newIndex)
				ff.indices.append(newIndex)
			faces.append(ff)
	
	print("---Printing Vertices---")
	for index, v in enumerate(vertices):
		print(index, v.pos)

	print("---Printing Faces---")
	for index, ff in enumerate(faces):
		print(index, ff.indices)

def writeToFile(filename):
	file = open(filename, "w")

	# write vertices
	for v in vertices:
		file.write("v")
		for p in v.pos:
			file.write(" ")
			file.write(str(p))
		file.write("\n")

	# write faces
	for f in faces:
		file.write("f")
		for i in f.indices:
			i = str(i + 1)
			file.write(" ")
			# .obj file indices start from 1
			file.write(i)
			# texture index is empty
			file.write("//")
			# actually we don't have normal but three.js can't parse it without normal
			# so I just assign the face index to the normal index, which means they're the same
			file.write(i)
		file.write("\n")
		
if __name__ == "__main__":
	convert("../model/obj_test5.obj")
	writeToFile("../model/obj_test5_converted.obj")