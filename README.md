# PolyTool
Expand half-edge to half-face in order to find cells

[Click here for the live demo](http://www.miaokaixiang.com/PolyTool/)

# How to find cells

1. construct half-faces first, each face will have 2 half-faces
2. construct the topology of these half-faces (which half-face is adjacent to the other)
3. use BFS to traverse all the half-faces. Each closure forms a cell