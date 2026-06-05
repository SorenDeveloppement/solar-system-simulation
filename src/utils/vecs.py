from panda3d.core import Vec4D, Vec3D, Vec4F


def vec3d_as_tuple(vec: Vec3D) -> tuple[float, float, float]:
    """
    Convert a Vec3D instance to a tuple of (x, y, z) coordinates.
    Args:
        vec (Vec3D): The Vec3D instance to convert.
    Returns:
        tuple[float, float, float]: A tuple containing the x, y, and z coordinates of the Vec3D instance.
    """
    return vec.getX(), vec.getY(), vec.getZ()

def vec4d_as_tuple(vec: Vec4D) -> tuple[float, float, float, float]:
    """
    Convert a Vec4D instance to a tuple of (x, y, z, w) coordinates.
    Args:
        vec (Vec4D): The Vec4D instance to convert.
    Returns:
        tuple[float, float, float, float]: A tuple containing the x, y, z, and w coordinates of the Vec4D instance.
    """
    return vec.getX(), vec.getY(), vec.getZ(), vec.getW()

def tuple_as_vec3d(tup: tuple[float, float, float]) -> Vec3D:
    """
    Convert a tuple of (x, y, z) coordinates to a Vec3D instance.
    Args:
        tup (tuple[float, float, float]): A tuple containing the x, y, and z coordinates to convert.
    Returns:
        Vec3D: A Vec3D instance with the specified x, y, and z coordinates.
    """
    return Vec3D(tup[0], tup[1], tup[2])

def tuple_as_vec4d(tup: tuple[float, float, float, float]) -> Vec4D:
    """
    Convert a tuple of (x, y, z, w) coordinates to a Vec4D instance.
    Args:
        tup (tuple[float, float, float, float]): A tuple containing the x, y, z, and w coordinates to convert.
    Returns:
        Vec4D: A Vec4D instance with the specified x, y, z, and w coordinates.
    """
    return Vec4D(tup[0], tup[1], tup[2], tup[3])

def tuple_as_vec4f(tup: tuple[float, float, float, float]) -> Vec4D:
    """
    Convert a tuple of (x, y, z, w) coordinates to a Vec4F instance.
    Args:
        tup (tuple[float, float, float, float]): A tuple containing the x, y, z, and w coordinates to convert.
    Returns:
        Vec4D: A Vec4F instance with the specified x, y, z, and w coordinates.
    """
    return Vec4F(tup[0], tup[1], tup[2], tup[3])