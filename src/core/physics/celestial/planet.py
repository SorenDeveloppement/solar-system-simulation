import os

from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import NodePath, TexturePool

from src.constants import DISTANCE_SCALE, TIME_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.properties.physics_properties import PhysicsProperties
from src.utils import icosphere


class Planet(CelestialBody):
    """
    The Planet class overrides the CelestialBody class and represents a planet in Space.
    """
    def __init__(self, name: str, physics_prop: PhysicsProperties) -> None:
        """
        Init method of the Planet class, which initializes the name and physics properties of the planet, as well as its 3D model and texture.
        Args:
            name (str): The name of the planet (e.g., "Earth", "Mars", "Jupiter").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
        """
        super().__init__(name, physics_prop)

        # TODO: Find a way to control each planet rotation through the task manager.

        self.__model: NodePath = icosphere.create_icosphere(subdivisions=4, radius=physics_prop.get_radius())
        self.__model.setP(90)

        self.__texture: str | None = None

        # Set the initial position of the planet based on its physics properties.
        self.__model.setPos(physics_prop.get_position().getX(), physics_prop.get_position().getY(), physics_prop.get_position().getZ())

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
        self.__model.setH(task.time * 10)
        return task.cont

    def update(self) -> None:
        """
            Update the planet's position based on its velocity and direction. This method is called every frame by the physics manager to update the planet's position in the simulation.

        """
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
        self.__model.setPos(scaled_position.getX(), scaled_position.getY(), scaled_position.getZ())

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_texture(self) -> str | None:
        """
        Getter for the texture of the planet.
        Returns:
            str | None: The file path of the planet's texture, or None if no texture is set.
        """
        return self.__texture

    def get_model(self) -> NodePath:
        """
        Getter for the 3D model of the planet.
        Returns:
            NodePath: The 3D model of the planet, which can be manipulated and rendered in the scene.
        """
        return self.__model

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

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

        self.__model.setTexture(tex)
        self.__texture = texture