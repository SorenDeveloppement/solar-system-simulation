from direct.showbase.ShowBaseGlobal import globalClock

from src.constants import TIME_SCALE, DISTANCE_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody


class Satellite(CelestialBody):
    """
    The Satellites class overrides the CelestialBody class and represents a satellite in Space.
    """
    def __init__(self, name: str, physics_prop, parent_planet_name: str, distance_to_parent: float) -> None:
        """
        Init method of the Satellites class.
        Args:
            name (str): The name of the satellite (e.g., "Moon", "Phobos", "Deimos").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
            parent_planet_name (str): The planet that the satellite orbits around.
        """
        super().__init__(name, physics_prop)

        self.__parent_planet_name: str = parent_planet_name
        self.__distance_to_parent: float = distance_to_parent

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def update(self) -> None:
        """
        Update the satellite's position based on its velocity and direction. This method is called every frame by the physics manager to update the satellite's position in the simulation.
        """
        if not self.get_physics_properties().is_fixed():
            # Update the planet's position based on its velocity and direction.
            dt: float = globalClock.getDt() * TIME_SCALE
            physics_prop = self.get_physics_properties()
            physics_prop.set_velocity(physics_prop.get_velocity() + physics_prop.get_acceleration() * dt)
            physics_prop.reset_acceleration()
            new_position = physics_prop.get_position() + physics_prop.get_velocity() * dt
            physics_prop.set_position(new_position)

            # Simulation scaled position
            scaled_position = new_position / DISTANCE_SCALE

            # Update the model's position to match the physics properties.
            self._model.setPos(scaled_position.getX(), scaled_position.getY(), scaled_position.getZ())

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_parent_planet(self) -> str:
        """
        Getter for the parent planet that the satellite orbits around.
        Returns:
            Planet: The parent planet that the satellite orbits around.
        """
        return self.__parent_planet_name

    def get_distance_to_parent(self) -> float:
        """
        Getter for the distance from the satellite to its parent planet.
        Returns:
            float: The distance from the satellite to its parent planet.
        """
        return self.__distance_to_parent

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    # A parents planet isn't expected to change, so no setter is provided for the parent planet.
    # If needed, a setter can be implemented to allow changing the parent planet of the satellite.

    def set_distance_to_parent(self, distance: float) -> None:
        """
        Setter for the distance from the satellite to its parent planet.
        Args:
            distance (float): The new distance from the satellite to its parent planet.
        """
        self.__distance_to_parent = distance