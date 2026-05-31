import math
from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomNode, GeomPoints, GeomVertexWriter, NodePath, GeomTriangles


# -----------------------------
# Utils math
# -----------------------------
def normalize(v):
    l = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return (v[0]/l, v[1]/l, v[2]/l)


def midpoint(a, b):
    return normalize(((a[0]+b[0])/2,
                      (a[1]+b[1])/2,
                      (a[2]+b[2])/2))


def spherical_uv(v):
    x, y, z = v

    u = math.atan2(x, z) / (2 * math.pi) + 0.5

    v = y * 0.5 + 0.5

    return u % 1.0, v


# -----------------------------
# Ico-sphere generation with proper UVs
# -----------------------------

def create_icosphere(subdivisions=3, radius=1.0):

    # -----------------------------
    # Base icosahedron
    # -----------------------------
    t = (1.0 + math.sqrt(5.0)) / 2.0

    verts = [
        normalize((-1,  t,  0)),
        normalize(( 1,  t,  0)),
        normalize((-1, -t,  0)),
        normalize(( 1, -t,  0)),

        normalize(( 0, -1,  t)),
        normalize(( 0,  1,  t)),
        normalize(( 0, -1, -t)),
        normalize(( 0,  1, -t)),

        normalize(( t,  0, -1)),
        normalize(( t,  0,  1)),
        normalize((-t,  0, -1)),
        normalize((-t,  0,  1)),
    ]

    faces = [
        (0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),
        (1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
        (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),
        (4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)
    ]

    # -----------------------------
    # Subdivision
    # -----------------------------
    cache = {}

    def get_mid(a, b):
        key = tuple(sorted((a, b)))
        if key in cache:
            return cache[key]

        m = midpoint(verts[a], verts[b])
        verts.append(m)
        idx = len(verts) - 1
        cache[key] = idx
        return idx

    for _ in range(subdivisions):
        new_faces = []
        for a, b, c in faces:
            ab = get_mid(a, b)
            bc = get_mid(b, c)
            ca = get_mid(c, a)

            new_faces += [
                (a, ab, ca),
                (b, bc, ab),
                (c, ca, bc),
                (ab, bc, ca)
            ]
        faces = new_faces

    # scale to radius
    verts = [(v[0]*radius, v[1]*radius, v[2]*radius) for v in verts]

    # -----------------------------
    # Panda3D geometry (IMPORTANT PART)
    # -----------------------------
    fmt = GeomVertexFormat.getV3n3t2()
    vdata = GeomVertexData("icosphere", fmt, Geom.UH_static)

    vw = GeomVertexWriter(vdata, "vertex")
    nw = GeomVertexWriter(vdata, "normal")
    tw = GeomVertexWriter(vdata, "texcoord")

    tris = GeomTriangles(Geom.UH_static)

    index = 0

    # -----------------------------
    # CRITICAL FIX: per-face vertices
    # -----------------------------
    for a, b, c in faces:

        va = verts[a]
        vb = verts[b]
        vc = verts[c]

        ua, va_uv = spherical_uv(va)
        ub, vb_uv = spherical_uv(vb)
        uc, vc_uv = spherical_uv(vc)

        # -----------------------------
        # SEAM FIX (CRITICAL)
        # -----------------------------
        if max(ua, ub, uc) - min(ua, ub, uc) > 0.5:
            if ua < 0.5: ua += 1.0
            if ub < 0.5: ub += 1.0
            if uc < 0.5: uc += 1.0

        tri_vertices = [
            (va, ua, va_uv),
            (vb, ub, vb_uv),
            (vc, uc, vc_uv)
        ]

        for v, u, t in tri_vertices:
            vw.addData3(v)
            nw.addData3(normalize(v))
            tw.addData2(u, t)

            tris.addVertex(index)
            index += 1

        tris.closePrimitive()

    geom = Geom(vdata)
    geom.addPrimitive(tris)

    node = GeomNode("icosphere")
    node.addGeom(geom)

    return NodePath(node)