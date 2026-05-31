from panda3d.core import WindowProperties, DirectionalLight, Vec4, Vec3D
from direct.showbase.ShowBase import ShowBase

from src.core.physics.celestial.planet import Planet
from src.core.physics.properties.physics_properties import PhysicsProperties


class SolarSystemApp(ShowBase):
    def __init__(self):
        super().__init__()

        # ---------------------------- #
        #     Window configuration     #
        # ---------------------------- #

        window_properties = WindowProperties()
        window_properties.setTitle("Solar System Simulation")
        window_properties.setSize(1280, 720)

        self.win.requestProperties(window_properties)

        # Background Color
        self.setBackgroundColor(0.02, 0.02, 0.02, 1)

        # ---------------------------- #
        #     Camera Configuration     #
        # ---------------------------- #

        self.cam.setPos(0, -10, 0)
        self.cam.lookAt(0, 0, 0)

        # ---------------------------- #
        #        Lighting Setup        #
        # ---------------------------- #

        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(Vec4(1, 1, 1, 1))

        directional_light_node = self.render.attachNewNode(directional_light)

        directional_light_node.setHpr(45, -45, 0)

        self.render.setLight(directional_light_node)

        # ---------------------------- #
        #            Shaders           #
        # ---------------------------- #

        self.render.setShaderAuto()

        # ---------------------------- #
        #         Other Setup          #
        # ---------------------------- #

        self.__earth_physics_prop = PhysicsProperties(1, 1, 0, Vec3D(0, 0, 0))
        self.__earth: Planet = Planet("Earth", self.__earth_physics_prop)
        self.__earth.set_texture("assets/textures/earth_surface_texture_bis.jpg")

        self.__earth.get_model().reparentTo(self.render)


if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()