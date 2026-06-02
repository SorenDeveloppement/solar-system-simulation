from panda3d.core import Vec4D, Material

from src.core.physics.celestial.celestial_body import CelestialBody


class Star(CelestialBody):
    """
    The Star class overrides the CelestialBody class and represents a star in Space.
    """
    def __init__(self, name: str, physics_prop, luminosity: float = 1.0, light_color: Vec4D = Vec4D(1, 1, 1, 1)) -> None:
        """
        Init method of the Star class.
        Args:
            name (str): The name of the star (e.g., "Sun", "Betelgeuse", "Sirius").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
            luminosity (float, optional): The luminosity of the star, which determines how much light it emits. Defaults to 1.0.
            light_color (Vec4D, optional): The color of the light emitted by the star, represented as a Vec4D object (RGBA). Defaults to Vec4D(1, 1, 1, 1) for white light.
        """
        super().__init__(name, physics_prop)

        self.__luminosity: float = 0.0
        self.__light_color: Vec4D = light_color
        self.__material: Material = Material()