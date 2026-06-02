import os

from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import NodePath, TexturePool

from src.constants import DISTANCE_SCALE, TIME_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.properties.physics_properties import PhysicsProperties
from src.utils import icosphere


class Planet(CelestialBody):
    def __init__(self, name: str, physics_prop: PhysicsProperties) -> None:
        super().__init__(name, physics_prop)

        self.__model: NodePath = icosphere.create_icosphere(subdivisions=4, radius=physics_prop.get_radius())
        self.__model.setP(90)

        self.__texture: str | None = None

        # Set the initial position of the planet based on its physics properties.
        self.__model.setPos(physics_prop.get_position().getX(), physics_prop.get_position().getY(), physics_prop.get_position().getZ())

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def rotate(self, task: Task) -> int:
        self.__model.setH(task.time * 10)
        return task.cont

    def update(self) -> None:
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
        return self.__texture

    def get_model(self) -> NodePath:
        return self.__model

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_texture(self, texture: str) -> None:
        if not os.path.isfile(texture):
            raise FileNotFoundError(f"Texture file '{texture}' does not exist.")

        tex = TexturePool.loadTexture(texture)
        if tex is None:
            raise RuntimeError(f"Failed to load texture '{texture}'.")

        self.__model.setTexture(tex)
        self.__texture = texture