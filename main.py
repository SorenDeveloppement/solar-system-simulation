import math

from direct.filter.CommonFilters import CommonFilters
from panda3d.core import WindowProperties, Vec4, Vec3D, PointLight, Material
from direct.showbase.ShowBase import ShowBase

from src.constants import MASS_SCALE, DISTANCE_SCALE, TIME_SCALE, G
from src.core.physics.celestial.planet import Planet
from src.core.physics.physics_manager import PhysicsManager
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

        self.cam.setPos(0, 0, 1000)
        self.cam.lookAt(0, 0, 0)

        # ---------------------------- #
        #        Lighting Setup        #
        # ---------------------------- #

        point_light = PointLight("point_light")
        point_light.setColor(Vec4(1, 1, 1, 1))

        point_light_node = self.render.attachNewNode(point_light)
        point_light_node.setPos(0, 0, 0)

        self.render.setLight(point_light_node)

        # ---------------------------- #
        #            Shaders           #
        # ---------------------------- #

        self.render.setShaderAuto()

        # Bloom post-process creates a soft halo around emissive objects like the Sun.
        self.filters = CommonFilters(self.win, self.cam)
        bloom_ok = self.filters.setBloom(
            blend=(0.35, 0.4, 0.3, 0.0),
            mintrigger=0.6,
            maxtrigger=1.0,
            desat=0.25,
            intensity=1.6,
            size="medium",
        )
        if not bloom_ok:
            print("Bloom filter is not supported on this GPU/driver.")

        # ---------------------------- #
        #         Other Setup          #
        # ---------------------------- #

        # ---------------------------- #
        #    Physics & Objects Setup   #
        # ---------------------------- #

        # Physics Manager
        self.__physics_manager: PhysicsManager = PhysicsManager()

        # Celestial bodies initialization
        sun_mass = 1.9885e30
        sun_radius = 696340e3

        # List: (name, mass in kg, radius in meters, distance in meters, texture)
        bodies = [
            ("Sun", sun_mass, sun_radius, 0.0, "assets/textures/sun.jpg"),
            ("Mercury", 3.3011e23, 2439.7e3, 57.91e9, "assets/textures/mercury.jpg"),
            ("Venus", 4.8675e24, 6051.8e3, 108.21e9, "assets/textures/venus.jpg"),
            ("Earth", 5.97237e24, 6371.0e3, 149.60e9, "assets/textures/earth.jpg"),
            ("Mars", 6.4171e23, 3389.5e3, 227.92e9, "assets/textures/mars.jpg"),
            ("Jupiter", 1.8982e27, 69911e3, 778.57e9, "assets/textures/jupiter.jpg"),
            ("Saturn", 5.6834e26, 58232e3, 1433.53e9, "assets/textures/saturn.jpg"),
            ("Uranus", 8.6810e25, 25362e3, 2872.46e9, "assets/textures/uranus.png"),
            ("Neptune", 1.02413e26, 24622e3, 4495.06e9, "assets/textures/neptune.jpg"),
        ]

        self.__objects: dict[str, Planet] = {}

        for name, mass_kg, radius_m, a_m, texture in bodies:
            # rayon affiché : on réduit fortement le rayon réel et on impose une taille minimale visible
            radius_sim = max((radius_m / DISTANCE_SCALE) * 0.2, 1) * 2

            prop = PhysicsProperties(mass_kg, radius_sim, Vec3D(a_m, 0, 0))
            planet = Planet(name, prop)
            planet.set_texture(texture)

            if name == "Sun":
                sun_model = planet.get_model()
                sun_model.setShaderAuto()
                sun_model.setLightOff(1)

                # Use an explicit emissive material so the Sun appears self-lit.
                sun_material = Material()
                sun_material.setEmission(Vec4(3.0, 2.6, 1.2, 1.0))
                sun_model.setMaterial(sun_material, 1)

                planet.get_physics_properties().set_velocity(Vec3D(0, 0, 0))
            else:
                v_real = math.sqrt(G * sun_mass / a_m)
                planet.get_physics_properties().set_velocity(Vec3D(0, v_real, 0))
                print(planet.get_physics_properties().get_velocity())

            # mise à l'échelle du modèle pour la visibilité
            try:
                planet.get_model().setScale(radius_sim)
            except Exception as e:
                print(f"An exception occurred :\r{e}")

            self.__objects[name] = planet

            planet.get_model().reparentTo(self.render)
            self.__physics_manager.add_physics_object(planet)

        # ---------------------------- #
        #       Task Management        #
        # ---------------------------- #

        self.__init_tasks()

    def __init_tasks(self) -> None:
        self.taskMgr.add(self.__physics_manager.update, "Physics Update Task")
        """self.taskMgr.add(self.__earth.rotate, "Earth Rotation Task")
        self.taskMgr.add(self.__e2.rotate, "Earth 2 Rotation Task")"""

    def set_camera_focus(self, target: Vec3D) -> None:
        self.cam.setPos(target.getX(), target.getY(), target.getZ() + 5)
        self.cam.lookAt(target.getX(), target.getY(), target.getZ())


if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()