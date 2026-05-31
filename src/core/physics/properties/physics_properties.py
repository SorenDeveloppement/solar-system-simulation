from panda3d.core import Vec3D


class PhysicsProperties:
    def __init__(self, mass: float, radius: float, speed: float, direction: Vec3D) -> None:
        self.__mass = mass
        self.__radius = radius
        self.__speed = speed
        self.__direction = Vec3D.normalized(direction)

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_name(self) -> str:
        return self.__name

    def get_mass(self) -> float:
        return self.__mass

    def get_radius(self) -> float:
        return self.__radius

    def get_speed(self) -> float:
        return self.__speed

    def get_direction(self) -> Vec3D:
        return self.__direction

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_mass(self, mass: float) -> None:
        self.__mass = mass

    def set_radius(self, radius: float) -> None:
        self.__radius = radius

    def set_speed(self, speed: float) -> None:
        self.__speed = speed

    def set_direction(self, direction: Vec3D) -> None:
        self.__direction = Vec3D.normalized(direction)