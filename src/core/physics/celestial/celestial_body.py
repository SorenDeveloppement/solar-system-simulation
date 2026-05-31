from src.core.physics.properties.physics_properties import PhysicsProperties


class CelestialBody:
    def __init__(self, name: str, physics_properties: PhysicsProperties) -> None:
        self.__name = name
        self.__physics_properties = physics_properties

    # ----------------------------- #
    #            Getters            #
    # ----------------------------- #

    def get_name(self) -> str:
        return self.__name

    def get_physics_properties(self) -> PhysicsProperties:
        return self.__physics_properties

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_name(self, name: str) -> None:
        self.__name = name

    def set_physics_properties(self, physics_properties: PhysicsProperties) -> None:
        self.__physics_properties = physics_properties