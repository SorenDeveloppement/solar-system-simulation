from panda3d.core import Vec4D, Vec3D


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