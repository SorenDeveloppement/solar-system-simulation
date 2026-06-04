from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec4D, Material

from src.constants import TIME_SCALE, DISTANCE_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.properties.physics_properties import PhysicsProperties


class Star(CelestialBody):
    """
    The Star class overrides the CelestialBody class and represents a star in Space.
    """
    def __init__(self, name: str, physics_prop: PhysicsProperties, luminosity: float = 1.0, light_color: Vec4D = Vec4D(1, 1, 1, 1)) -> None:
        """
        Init method of the Star class.
        Args:
            name (str): The name of the star (e.g., "Sun", "Betelgeuse", "Sirius").
            physics_prop (PhysicsProperties): An instance of the PhysicsProperties class.
            luminosity (float, optional): The luminosity of the star, which determines how much light it emits. Defaults to 1.0.
            light_color (Vec4D, optional): The color of the light emitted by the star, represented as a Vec4D object (RGBA). Defaults to Vec4D(1, 1, 1, 1) for white light.
        """
        super().__init__(name, physics_prop)

        self.__luminosity: float = luminosity
        self.__light_color: Vec4D = light_color
        self.__material: Material = Material()

        self._model.setShaderAuto()
        self._model.setLightOff(1)

        self.__material.setEmission(self.__light_color * self.__luminosity)
        self._model.setMaterial(self.__material)

    # ----------------------------- #
    #            Methods            #
    # ----------------------------- #

    def update(self) -> None:
        """
        Update the star's position based on its velocity and direction. This method is called every frame by the physics manager to update the star's position in the simulation.
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

    def get_luminosity(self) -> float:
        """
        Getter for the luminosity of the star.
        Returns:
            float: The luminosity of the star, which determines how much light it emits.
        """
        return self.__luminosity

    def get_light_color(self) -> Vec4D:
        """
        Getter for the light color of the star.
        Returns:
            Vec4D: The color of the light emitted by the star, represented as a Vec4D object (RGBA).
        """
        return self.__light_color

    def get_material(self) -> Material:
        """
        Getter for the material of the star, which is used to set the emission color based on the star's luminosity and light color.
        Returns:
            Material: The material of the star, which can be used to set properties such as emission color.
        """
        return self.__material

    # ----------------------------- #
    #            Setters            #
    # ----------------------------- #

    def set_luminosity(self, luminosity: float) -> None:
        """
        Setter for the luminosity of the star, which updates the emission color of the star's material based on the new luminosity and light color.
        Args:
            luminosity (float): The new luminosity of the star, which determines how much light it emits.
        """
        self.__luminosity = luminosity
        self.__material.setEmission(self.__light_color * self.__luminosity)

    def set_light_color(self, light_color: Vec4D) -> None:
        """
        Setter for the light color of the star, which updates the emission color of the star's material based on the new light color and luminosity.
        Args:
            light_color (Vec4D): The new color of the light emitted by the star, represented as a Vec4D object (RGBA).
        """
        self.__light_color = light_color
        self.__material.setEmission(self.__light_color * self.__luminosity)