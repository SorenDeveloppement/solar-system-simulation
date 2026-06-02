"""
This module provides a function to create a Fibonacci sphere, which is a method of distributing points evenly on the surface of a sphere. The function `create_fibonacci_sphere` generates a specified number of points on the sphere's surface using the Fibonacci lattice method.
"""

import math
from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomNode, GeomPoints, GeomVertexWriter, NodePath, GeomTriangles


def create_fibonacci_sphere(radius=1.0, samples=1000):
    """Generates a sphere using the Fibonacci lattice method for even point distribution.

    Source: https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
    """
    fmt = GeomVertexFormat.getV3()
    vdata = GeomVertexData("sphere", fmt, Geom.UH_static)

    vertex = GeomVertexWriter(vdata, "vertex")

    golden_angle = math.pi * (3 - math.sqrt(5))

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # 1 → -1
        r = math.sqrt(1 - y * y)

        theta = golden_angle * i

        x = math.cos(theta) * r
        z = math.sin(theta) * r

        vertex.addData3(x * radius, y * radius, z * radius)

    points = GeomPoints(Geom.UH_static)
    points.addNextVertices(samples)

    geom = Geom(vdata)
    geom.addPrimitive(points)

    node = GeomNode("fibonacci_sphere")
    node.addGeom(geom)

    return NodePath(node)