from src.core.physics.celestial.celestial_body import CelestialBody


class Satellites(CelestialBody):
    """
    The Satellites class overrides the CelestialBody class and represents a satellite in Space.
    """
    def __init__(self, name: str, physics_prop, parent_planet: "Planet") -> None:
        """
        Init method of the Satellites class.
        Args:
            name (str): The name of the satellite (e.g., "Moon", "Phobos", "Deimos").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
            parent_planet (Planet): The planet that the satellite orbits around.
        """
        super().__init__(name, physics_prop)

        self.__parent_planet: "Planet" = parent_planet