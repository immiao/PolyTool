# this .py file is used to eliminate the duplicated vertices in the original .obj file
import numpy
from sets import Set

def strArr2floatArr (strArr):
	result = []
	for s in strArr:
		result.append(float(s))
	return result

vertices = []
faces = []

def getKey(item):
	return item[0]

def readFile(inputDir):
	force_v_file = open(inputDir + '/force_v.txt')
	force_f_v_file = open(inputDir + '/force_f_v.txt')

	for line in force_v_file:
		#print(line)
		tokens = line.split('\t')
		vertices.append((int(tokens[0]), tokens[1:4]))

	for line in force_f_v_file:
		tokens = line.split('\t')
		index = int(tokens[0][0:len(tokens[0])-1])
		faces.append((index, tokens[1:]))

	vertices.sort(key=getKey)
	faces.sort(key=getKey)

def writeToFile(filename):
	file = open(filename, "w")

	# write vertices
	for v in vertices:
		file.write("v")
		for vv in v[1]:
			file.write(" ")
			file.write(vv)
		file.write("\n")

	# write faces
	for f in faces:
		file.write("f")
		for i in f[1]:
			i = str(int(i) + 1)
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
	inputDir = "../model/txt0"
	readFile(inputDir)
	writeToFile(inputDir + "/txt0_converted.obj")