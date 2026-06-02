from src.core.physics.properties.physics_properties import PhysicsProperties


class CelestialBody:
    """
    The CelestialBody class represents a generic celestial body in the solar system, such as a planet, moon, or asteroid. It contains basic properties and methods that are common to all celestial bodies, such as name and physics properties. This class is meant to be extended by specific types of celestial bodies (e.g., Planet, Satellite, Stars, etc.) that will implement their own unique behaviors and characteristics.
    """
    def __init__(self, name: str, physics_properties: PhysicsProperties) -> None:
        """
        Init method of the CelestialBody class, which initializes the name and physics properties of the celestial body.
        Args:
            name (str): The name of the celestial body (e.g., "Earth", "Mars", "Jupiter").
            physics_properties (PhysicsProperties): An instance of the PhysicsProperties.
        """
        self.__name = name
        self.__physics_properties = physics_properties

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def update(self) -> None:
        """Placeholder method to override in subclasses."""
        pass

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_name(self) -> str:
        """
        Getter for the name of the celestial body.
        Returns:
            str: The name of the celestial body.
        """
        return self.__name

    def get_physics_properties(self) -> PhysicsProperties:
        """
        Getter for the physics properties of the celestial body.
        Returns:
            PhysicsProperties: The physics properties of the celestial body.
        """
        return self.__physics_properties

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_name(self, name: str) -> None:
        """
        Setter for the name of the celestial body.
        Args:
            name (str): The new name of the celestial body.
        """
        self.__name = name

    def set_physics_properties(self, physics_properties: PhysicsProperties) -> None:
        """
        Setter for the physics properties of the celestial body.
        Args:
            physics_properties (PhysicsProperties): The new physics properties of the celestial body.
        """
        self.__physics_properties = physics_properties