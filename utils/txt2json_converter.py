import json
from sets import Set
from sys import maxint
import math

# tmp hacky functions for vec3

def norm2 (a):
    return dot(a, a)

def dot ( a, b ):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def area (a, b, c):
    u = [ b[0] - a[0], b[1] - a[1], b[2] - a[2] ]
    v = [ c[0] - a[0], c[1] - a[1], c[2] - a[2] ]

    cross2 = norm2(u) * norm2(v) - dot(u, v)
    return math.sqrt(cross2) * 0.5









class DiagramJson:
    def __init__(self):
        self.json = {
            'form': {
                'vertices': {}, 
                'vertices_2_force_faces': {},   # face array
                'vertices_2_force_cells': {},
                'vertices_external': None,         # converted from set: vid: 1

                'edges': {}
            },

            'force': {
                'vertices': {},
                'edges': {},
                'faces_e': {},
                'faces_v': {},
                'cells': {}
            },

            'strength_scaler': {
                'min': maxint,
                'max': 0
            },

            'force_face_2_strength': {}

        }

class Txt2JsonParser:
    def __init__(self):
        self.diagramJson = DiagramJson()

        # # tmp data structures used only when parsing
        # self.form_edge_2_vertex = {}
        self.force_face_2_form_edge = {}    # inverse index, for caluclate edge width i.e. area of faces (strength)
        # self.form_vertex_external_count = {}    # vid: count - 0, 1, 2

    def readFormVertex(self, filename):
        f = open(filename)
        v = self.diagramJson.json['form']['vertices']
        v2fa = self.diagramJson.json['form']['vertices_2_force_faces']
        for line in f:
            vertex = line.strip().split('\t')
            # print vertex
            v[vertex[0]] = map(float, vertex[1:])

            # create array for form_vertices to force_face array (cells)
            v2fa[vertex[0]] = []

        # print self.diagramJson.json
        f.close()

    def readFormEdge(self, filename_edge_vertex, filename_edge_to_force_face, filename_edge_ex):
        f_edge_vertex = open(filename_edge_vertex)
        edges = self.diagramJson.json['form']['edges']
        for line in f_edge_vertex:
            edge = line.strip().split('\t')
            e = edges[edge[0]] = {}
            e['vertex'] = edge[1:]
            # e['external'] = False
            # print edge[0], e['vertex']

        # print edges
        f_edge_vertex.close()

        
        v2fa = self.diagramJson.json['form']['vertices_2_force_faces']

        f_edge_to_force_face = open(filename_edge_to_force_face)
        for line in f_edge_to_force_face:
            edge = line.strip().split('\t')
            f = edge[1] if edge[1] != "Null" else None
            edges[edge[0]]['force_face'] = f

            edge_vertex = edges[edge[0]]['vertex']
            for v in edge_vertex:
                v2fa[v].append(f)

            # force_face_2_form_edge (tmp structure) for compute strength
            if f != None:
                self.force_face_2_form_edge[f] = edge[0]

        f_edge_to_force_face.close()

        
        vertex_ex_set = Set()

        f_edge_ex = open(filename_edge_ex)
        for line in f_edge_ex:
            edge = line.strip().split('\t')
            for e in edge:
                edges[e]['external'] = True

                vertex_ex_set.add(edges[e]['vertex'][0])
                vertex_ex_set.add(edges[e]['vertex'][1])

        f_edge_ex.close()


        self.diagramJson.json['form']['vertices_external'] = dict.fromkeys(vertex_ex_set, 1)



        # label external force edge
        for e in edges:
            is_ex_vertex_0 = edges[e]['vertex'][0] in vertex_ex_set
            is_ex_vertex_1 = edges[e]['vertex'][1] in vertex_ex_set
            if is_ex_vertex_0 != is_ex_vertex_1:
                # print edges[e]['vertex'][0], ':', is_ex_vertex_0, ' , ', edges[e]['vertex'][1], ':', is_ex_vertex_1
                # force vector: from v0 to v1
                edges[e]['ex_force'] = True





        # print edges
        # print self.diagramJson.json


    def readForceVertex(self, filename):
        f = open(filename)
        v = self.diagramJson.json['force']['vertices']
        for line in f:
            vertex = line.strip().split('\t')
            # print vertex
            v[vertex[0]] = map(float, vertex[1:])

        # print self.diagramJson.json
        f.close()

    def readForceEdge(self, filename_edge_vertex):
        f_edge_vertex = open(filename_edge_vertex)
        edges = self.diagramJson.json['force']['edges']
        for line in f_edge_vertex:
            edge = line.strip().split('\t')
            edges[edge[0]] = edge[1:]

        # print edges
        f_edge_vertex.close()
        # print self.diagramJson.json

    def readForceFaceEdge(self, filename_face_edge):
        f_face_edge = open(filename_face_edge)
        edges = self.diagramJson.json['force']['edges']
        faces_e = self.diagramJson.json['force']['faces_e']
        # faces_v = self.diagramJson.json['force']['faces_v']
        for line in f_face_edge:
            face = line.strip().split('\t')
            faces_e[face[0]] = face[1:]

            # # convert face edge to face vertex
            # cur_face_vertex = Set()
            # for e in face[1:]:
            #     # extend vertex array
            #     # cur_face_vertex.extend(edges[e])
            #     for v in edges[e]:
            #         cur_face_vertex.add(v)
            
            # faces_v[face[0]] = list(cur_face_vertex)
            # print faces_v[face[0]]

        f_face_edge.close()
        # print self.diagramJson.json

    def readForceFaceVertex(self, filename_face_vertex):
        f_face_vertex = open(filename_face_vertex)
        # fan shape order
        faces_v = self.diagramJson.json['force']['faces_v']

        strengthScaler = self.diagramJson.json['strength_scaler']
        force_face_2_strength = self.diagramJson.json['force_face_2_strength']

        v = self.diagramJson.json['force']['vertices']
        e = self.diagramJson.json['form']['edges']

        for line in f_face_vertex:
            face = line.strip().split('\t')
            faces_v[face[0]] = face[1:]

            strength = 0

            if len(face) == 4:
                # tri
                strength = area( v[face[1]], v[face[2]], v[face[3]] )                
            elif len(face) == 5:
                # quad
                strength = area( v[face[1]], v[face[2]], v[face[3]] ) + area( v[face[1]], v[face[3]], v[face[4]] )

            # e[ self.force_face_2_form_edge[face[0]] ]['strength'] = strength
            force_face_2_strength[ face[0] ] = strength

            curEdge = e[ self.force_face_2_form_edge[face[0]] ]

            if 'external' not in curEdge and 'ex_force' not in curEdge:
                strengthScaler['max'] = max(strength, strengthScaler['max'])
                strengthScaler['min'] = min(strength, strengthScaler['min'])

        f_face_vertex.close()






if __name__ == "__main__":
    
    foldername = "../model/txt0"
    
    parser = Txt2JsonParser()

    #parser.readFormVertex(foldername + "/form_v.txt")
    #parser.readFormEdge(foldername + "/form_e_v.txt", \
    #                    foldername + "/form_e_to_force_f.txt", \
    #                    foldername + "/form_e_ex.txt")
    
    parser.readForceVertex(foldername + "/force_v.txt")
    #parser.readForceEdge(foldername + "/force_e_v.txt")
    #parser.readForceFaceEdge(foldername + "/force_f_e.txt")
    parser.readForceFaceVertex(foldername + "/force_f_v.txt")

    with open(foldername + '/diagram.json', 'w') as out:
        json.dump(parser.diagramJson.json, out)
    