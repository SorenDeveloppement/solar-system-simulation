from direct.showbase.ShowBaseGlobal import globalClock

from src.constants import DISTANCE_SCALE, TIME_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.celestial.satellite import Satellite
from src.core.physics.properties.physics_properties import PhysicsProperties
from src.utils import icosphere


class Planet(CelestialBody):
    """
    The Planet class overrides the CelestialBody class and represents a planet in Space.
    """
    def __init__(self, name: str, physics_prop: PhysicsProperties, has_atmosphere: bool = False, surface_gravity: float = 1.0,
                 satellites: list[Satellite] = None) -> None:
        """
        Init method of the Planet class, which initializes the name and physics properties of the planet, as well as its 3D model and texture.
        Args:
            name (str): The name of the planet (e.g., "Earth", "Mars", "Jupiter").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
            has_atmosphere (bool, optional): A boolean indicating whether the planet has an atmosphere. Defaults to False.
            surface_gravity (float, optional): The surface gravity of the planet, which determines how much force it exerts on objects on its surface. Defaults to 1.0.
            satellites (list[Satellites], optional): A list of Satellite objects that orbit the planet. Defaults to None.
        """
        super().__init__(name, physics_prop)

        self.__has_atmosphere: bool = has_atmosphere
        self.__surface_gravity: float = surface_gravity

        if satellites is None:
            self.__satellites: list[Satellite] = []
        else:
            self.__satellites: list[Satellite] = satellites

        # TODO: Find a way to control each planet rotation through the task manager.

        self._model = icosphere.create_icosphere(subdivisions=4, radius=physics_prop.get_radius())
        self._model.setP(90)

        # Set the initial position of the planet based on its physics properties (scaled to scene units).
        # Physics positions are stored in meters; convert to scene units using DISTANCE_SCALE before placing the model.
        phys_pos = physics_prop.get_position()
        scaled_pos = phys_pos / DISTANCE_SCALE
        self._model.setPos(scaled_pos.getX(), scaled_pos.getY(), scaled_pos.getZ())

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def update(self) -> None:
        """
        Update the planet's position based on its velocity and direction. This method is called every frame by the physics manager to update the planet's position in the simulation.
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

    def has_atmosphere(self) -> bool:
        """
        Getter for whether the planet has an atmosphere.
        Returns:
            bool: A boolean indicating whether the planet has an atmosphere.
        """
        return self.__has_atmosphere

    def get_surface_gravity(self) -> float:
        """
        Getter for the surface gravity of the planet.
        Returns:
            float: The surface gravity of the planet, which determines how much force it exerts on objects on its surface.
        """
        return self.__surface_gravity

    def get_satellites(self) -> list[Satellite]:
        """
        Getter for the list of satellites that orbit the planet.
        Returns:
            list[Satellite]: A list of Satellite objects that orbit the planet.
        """
        return self.__satellites

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def add_satellite(self, satellite: Satellite) -> None:
        """
        Add a satellite to the list of satellites that orbit the planet.
        Args:
            satellite (Satellite): The Satellite object to be added to the list of satellites that orbit the planet.
        """
        self.__satellites.append(satellite)