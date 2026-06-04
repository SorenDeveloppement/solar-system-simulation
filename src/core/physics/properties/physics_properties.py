from panda3d.core import Vec3D


class PhysicsProperties:
    """
    The PhysicsProperties class encapsulates the physical properties of a celestial body, such as mass, radius, position, velocity, and acceleration. It provides methods to apply forces to the body and update its state based on the applied forces.
    """
    def __init__(self, mass: float = 1.0, radius: float = 1.0, position: Vec3D = Vec3D(0, 0, 0), fixed: bool = False,
                 rotation_speed: float = 1.0, orbital_inclination: float = 0.0) -> None:
        """
            Init method of the PhysicsProperties class, which initializes the mass, radius, position, velocity, and acceleration of the celestial body.
        Args:
            mass (float): The mass of the celestial body, which determines how much it will be affected by gravitational forces and how much force it will exert on other bodies. Defaults to 1.0.
            radius (float): The radius of the celestial body, which is used for collision detection and rendering purposes. Defaults to 1.0.
            position (Vec3D): The initial position of the celestial body in 3D space, represented as a Vec3D object. This position will be updated over time based on the body's velocity and acceleration. Defaults to Vec3D(0, 0, 0).
            fixed (bool): A boolean flag indicating whether the celestial body is fixed in space (i.e., it does not move or respond to forces). If set to True, the body will not be affected by forces and will not update its position or velocity. Defaults to False.
            rotation_speed (float): The rotation speed of the celestial body, which determines how fast it rotates around its own axis.
            orbital_inclination (float): The orbital inclination of the celestial body, which is the angle between the body's orbital plane and a reference plane (usually the ecliptic plane).
        """
        self.__mass: float = mass
        self.__radius: float = radius
        self.__acceleration: Vec3D = Vec3D(0, 0, 0)
        self.__position: Vec3D = position
        self.__velocity: Vec3D = Vec3D(0, 0, 0)
        self.__fixed: bool = fixed
        self.__rotation_speed: float = rotation_speed
        self.__orbital_inclination: float = orbital_inclination

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def apply_force(self, force: Vec3D) -> None:
        """
        Apply a force to the celestial body, which will affect its acceleration based on Newton's second law of motion (F = m * a).

        The acceleration is updated by adding the force divided by the mass of the body
        Args:
            force (Vec3D): The force vector to be applied to the celestial body. This force will affect the body's acceleration and, consequently, its velocity and position over time.
        """
        self.__acceleration += force / self.__mass

    def reset_acceleration(self) -> None:
        """
        Reset the acceleration of the celestial body to zero. This is typically called at the end of each update cycle after the forces have been applied and the velocity and position have been updated, to prepare for the next cycle of force calculations.
        """
        self.__acceleration = Vec3D(0, 0, 0)

    def as_dict(self) -> dict[str, float | Vec3D | bool]:
        """
        Convert the physics properties of the celestial body into a dictionary format.

        Returns:
            dict[str, float | Vec3D | bool]: A dictionary containing the mass, radius, position, velocity, acceleration, fixed status, rotation speed, and orbital inclination of the celestial body.
        """
        return {
            "mass": self.__mass,
            "radius": self.__radius,
            "position": self.__position,
            "velocity": self.__velocity,
            "acceleration": self.__acceleration,
            "fixed": self.__fixed,
            "rotation_speed": self.__rotation_speed,
            "orbital_inclination": self.__orbital_inclination
        }

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_mass(self) -> float:
        """
        Getter for the mass of the celestial body.
        Returns:
            float: The mass of the celestial body.
        """
        return self.__mass

    def get_radius(self) -> float:
        """
        Getter for the radius of the celestial body.
        Returns:
            float: The radius of the celestial body.
        """
        return self.__radius

    def get_position(self) -> Vec3D:
        """
        Getter for the position of the celestial body.
        Returns:
            Vec3D: The position of the celestial body in 3D space.
        """
        return self.__position

    def get_scaled_position(self, scale: float) -> Vec3D:
        """
        Getter for the scaled position of the celestial body, which is the position divided by a specified scale factor. This is useful for rendering purposes, where the actual positions may be too large to display directly.

        Args:
            scale (float): The scale factor by which to divide the position of the celestial body.
        Returns:
            Vec3D: The scaled position of the celestial body in 3D space.
        """
        return self.__position / scale

    def direction(self) -> Vec3D:
        """
        Returns the normalized direction vector. If the velocity is zero, it returns a zero vector.

        Returns:
            Vec3D: The normalized direction vector of the velocity, or a zero vector if the velocity is zero.
        """
        if self.__velocity.lengthSquared() == 0:
            return Vec3D(0, 0, 0)
        return self.__velocity / self.__velocity.length()

    def get_acceleration(self) -> Vec3D:
        """
        Getter for the acceleration of the celestial body.
        Returns:
            Vec3D: The acceleration of the celestial body in 3D space.
        """
        return self.__acceleration

    def get_velocity(self) -> Vec3D:
        """
        Getter for the velocity of the celestial body.
        Returns:
            Vec3D: The velocity of the celestial body in 3D space.
        """
        return self.__velocity

    def get_rotation_speed(self) -> float:
        """
        Getter for the rotation speed of the celestial body.
        Returns:
            float: The rotation speed of the celestial body.
        """
        return self.__rotation_speed

    def is_fixed(self) -> bool:
        """
        Getter for the fixed status of the celestial body.
        Returns:
            bool: True if the celestial body is fixed in space (i.e., it does not move or respond to forces), False otherwise.
        """
        return self.__fixed

    def get_orbital_inclination(self) -> float:
        """
        Getter for the orbital inclination of the celestial body.
        Returns:
            float: The orbital inclination of the celestial body in degrees.
        """
        return self.__orbital_inclination

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_mass(self, mass: float) -> None:
        """
        Setter for the mass of the celestial body.
        Args:
            mass (float): The new mass of the celestial body.
        """
        self.__mass = mass

    def set_radius(self, radius: float) -> None:
        """
        Setter for the radius of the celestial body.
        Args:
            radius (float): The new radius of the celestial body.
        """
        self.__radius = radius

    def set_position(self, position: Vec3D) -> None:
        """
        Setter for the position of the celestial body.
        Args:
            position (Vec3D): The new position of the celestial body in 3D space.
        """
        self.__position = position

    def set_acceleration(self, acceleration: Vec3D) -> None:
        """
        Setter for the acceleration of the celestial body.
        Args:
            acceleration (Vec3D): The new acceleration of the celestial body in 3D space.
        """
        self.__acceleration = acceleration

    def set_velocity(self, velocity: Vec3D) -> None:
        """
        Setter for the velocity of the celestial body.
        Args:
            velocity (Vec3D): The new velocity of the celestial body in 3D space.
        """
        self.__velocity = velocity

    def set_rotation_speed(self, rotation_speed: float) -> None:
        """
        Setter for the rotation speed of the celestial body.
        Args:
            rotation_speed (float): The new rotation speed of the celestial body.
        """
        self.__rotation_speed = rotation_speed

    def set_fixed(self, fixed: bool) -> None:
        """
        Setter for the fixed status of the celestial body.
        Args:
            fixed (bool): A boolean flag indicating whether the celestial body is fixed in space or not.
        """
        self.__fixed = fixed

    def set_orbital_inclination(self, orbital_inclination: float) -> None:
        """
        Setter for the orbital inclination of the celestial body.
        Args:
            orbital_inclination (float): The new orbital inclination of the celestial body in degrees.
        """
        self.__orbital_inclination = orbital_inclination
