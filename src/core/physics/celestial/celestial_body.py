import os

from direct.task import Task
from panda3d.core import NodePath, TexturePool

from src.core.physics.properties.physics_properties import PhysicsProperties
from src.utils.icosphere import create_icosphere


class CelestialBody:
    """
    The CelestialBody class represents a generic celestial body in the solar system, such as a planet, moon, or asteroid. It contains basic properties and methods that are common to all celestial bodies, such as name and physics properties. This class is meant to be extended by specific types of celestial bodies (e.g., Planet, Satellite, Stars, etc.) that will implement their own unique behaviors and characteristics.
    """
    def __init__(self, name: str, physics_properties: PhysicsProperties, age: float = 0.0, surface_temperature: float = 0.0) -> None:
        """
        Init method of the CelestialBody class, which initializes the name and physics properties of the celestial body.
        Args:
            name (str): The name of the celestial body (e.g., "Earth", "Mars", "Jupiter").
            physics_properties (PhysicsProperties): An instance of the PhysicsProperties.
            age (float): The age of the celestial body in billions of years. Defaults to 0.0.
            surface_temperature (float): The surface temperature of the celestial body in Kelvin. Defaults to 0.0.
        """
        self._name = name
        self._physics_properties = physics_properties
        self._model: NodePath = create_icosphere(subdivisions=1, radius=1)
        self._texture: str | None = None
        self._age: float = age
        self._surface_temperature: float = surface_temperature

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def rotate(self, rotation_speed: float, task: Task) -> int:
        """
        Method that rotates the planet around its own axis at a specified speed.
        Args:
            rotation_speed (float): The speed at which the planet should rotate (degrees per second).
            task (Task): The task object provided by the Panda3D task manager, which allows us to control the execution of this function and access timing information.

        Returns:
            int: The return value of the task, which indicates whether the task should continue running or not. In this case, we return Task.cont to indicate that the task should continue running indefinitely.
        """
        self._model.setH(task.time * rotation_speed)
        return task.cont

    def update(self) -> None:
        """Placeholder method to override in subclasses."""
        pass

    def distance_to(self, other: 'CelestialBody') -> float:
        """
        Calculate the distance from this celestial body to another celestial body.
        Args:
            other (CelestialBody): The other celestial body to which we want to calculate the distance.
        Returns:
            float: The distance between this celestial body and the other celestial body, calculated using the positions of both bodies.
        """
        pos1 = self.get_physics_properties().get_position()
        pos2 = other.get_physics_properties().get_position()
        return (pos1 - pos2).length()

    def collides_with(self, other: 'CelestialBody') -> bool:
        """
        Check if this celestial body collides with another celestial body based on their positions and radii.
        Args:
            other (CelestialBody): The other celestial body to check for collision.
        Returns:
            bool: True if the two celestial bodies collide (i.e., the distance between them is less than the sum of their radii), False otherwise.
        """
        # TODO: Change this method to use the 3D models' bounding boxes for more accurate collision detection.
        distance = self.distance_to(other)
        radius_sum = self.get_physics_properties().get_radius() + other.get_physics_properties().get_radius()
        return distance < radius_sum

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_name(self) -> str:
        """
        Getter for the name of the celestial body.
        Returns:
            str: The name of the celestial body.
        """
        return self._name

    def get_physics_properties(self) -> PhysicsProperties:
        """
        Getter for the physics properties of the celestial body.
        Returns:
            PhysicsProperties: The physics properties of the celestial body.
        """
        return self._physics_properties

    def get_texture(self) -> str | None:
        """
        Getter for the texture of the planet.
        Returns:
            str | None: The file path of the planet's texture, or None if no texture is set.
        """
        return self._texture

    def get_model(self) -> NodePath:
        """
        Getter for the 3D model of the planet.
        Returns:
            NodePath: The 3D model of the planet, which can be manipulated and rendered in the scene.
        """
        return self._model

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_name(self, name: str) -> None:
        """
        Setter for the name of the celestial body.
        Args:
            name (str): The new name of the celestial body.
        """
        self._name = name

    def set_physics_properties(self, physics_properties: PhysicsProperties) -> None:
        """
        Setter for the physics properties of the celestial body.
        Args:
            physics_properties (PhysicsProperties): The new physics properties of the celestial body.
        """
        self._physics_properties = physics_properties

    def set_texture(self, texture: str) -> None:
        """
        Setter for the texture of the planet. This method loads the specified texture file and applies it to the planet's 3D model. It also updates the internal state to keep track of the currently applied texture.
        Args:
            texture (str): The file path of the texture to be applied to the planet's model. This should be a valid image file (e.g., PNG, JPEG) that can be loaded as a texture.
        """
        if not os.path.isfile(texture):
            raise FileNotFoundError(f"Texture file '{texture}' does not exist.")

        tex = TexturePool.loadTexture(texture)
        if tex is None:
            raise RuntimeError(f"Failed to load texture '{texture}'.")

        self._model.setTexture(tex)
        self._texture = texture