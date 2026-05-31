import os

from panda3d.core import NodePath, TexturePool

from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.properties.physics_properties import PhysicsProperties
from src.utils import icosphere


class Planet(CelestialBody):
    def __init__(self, name: str, physics_prop: PhysicsProperties) -> None:
        super().__init__(name, physics_prop)

        self.__model: NodePath = icosphere.create_icosphere(subdivisions=4, radius=physics_prop.get_radius())
        self.__model.setP(90)

        self.__texture: str | None = None

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