from panda3d.core import Vec3D


class PhysicsProperties:
    def __init__(self, mass: float, radius: float, position: Vec3D) -> None:
        self.__mass: float = mass
        self.__radius: float = radius
        self.__acceleration: Vec3D = Vec3D(0, 0, 0)
        self.__position: Vec3D = position
        self.__velocity: Vec3D = Vec3D(0, 0, 0)

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def apply_force(self, force: Vec3D) -> None:
        self.__acceleration += force / self.__mass

    def reset_acceleration(self) -> None:
        self.__acceleration = Vec3D(0, 0, 0)

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_mass(self) -> float:
        return self.__mass

    def get_radius(self) -> float:
        return self.__radius

    def get_position(self) -> Vec3D:
        return self.__position

    def direction(self) -> Vec3D:
        """Returns the normalized direction vector. If the velocity is zero, it returns a zero vector."""
        if self.velocity.lengthSquared() == 0:
            return Vec3D(0, 0, 0)
        return self.velocity / self.velocity.length()

    def get_acceleration(self) -> Vec3D:
        return self.__acceleration

    def get_velocity(self) -> Vec3D:
        return self.__velocity

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_mass(self, mass: float) -> None:
        self.__mass = mass

    def set_radius(self, radius: float) -> None:
        self.__radius = radius

    def set_position(self, position: Vec3D) -> None:
        self.__position = position

    def set_acceleration(self, acceleration: Vec3D) -> None:
        self.__acceleration = acceleration

    def set_velocity(self, velocity: Vec3D) -> None:
        self.__velocity = velocity
