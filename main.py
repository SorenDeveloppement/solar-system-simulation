import math

from direct.filter.CommonFilters import CommonFilters
from panda3d.core import WindowProperties, Vec4, Vec3D, PointLight, Material
from direct.showbase.ShowBase import ShowBase
from pygments.console import light_colors

from src.constants import MASS_SCALE, DISTANCE_SCALE, TIME_SCALE, G, SIZE_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.celestial.planet import Planet
from src.core.physics.celestial.satellite import Satellite
from src.core.physics.celestial.star import Star
from src.core.physics.physics_manager import PhysicsManager
from src.core.physics.properties.physics_properties import PhysicsProperties


class SolarSystemApp(ShowBase):
    """
    Main application class for the solar system simulation.
    This class initializes the window, camera, lighting, shaders, and the celestial bodies (planets) with their physics properties. It also sets up the main task for updating the physics simulation.
    """
    def __init__(self):
        """
        Init method of the application.
        """
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

        self.cam.setPos(0, 0, 2_000)
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

        self.__init_celestial_bodies()

        # ---------------------------- #
        #       Task Management        #
        # ---------------------------- #

        self.__init_tasks()

    def __init_celestial_bodies(self) -> None:
        """
        Initialize the celestial bodies (planets) with their physics properties and add them to the physics manager.
        """
        # Celestial bodies initialization
        sun_mass = 1.9885e30
        sun_radius = 696340e3

        # TODO: Load the data from a yaml/json file in the future instead of hardcoding it.
        # List: (name, mass in kg, radius in meters, distance in meters, texture, type, satellites)
        bodies = [
            ("Sun", sun_mass, sun_radius, 0.0, "assets/textures/sun.jpg", "star", None),
            ("Mercury", 3.3011e23, 2439.7e3, 57.91e9, "assets/textures/mercury.jpg", "planet", None),
            ("Venus", 4.8675e24, 6051.8e3, 108.21e9, "assets/textures/venus.jpg", "planet", None),
            ("Earth", 5.97237e24, 6371.0e3, 149.60e9, "assets/textures/earth.jpg", "planet",
                [Satellite("Moon", PhysicsProperties(mass=7.342e22, radius=1737.1e3), "Earth", 384400e3)]),
            ("Mars", 6.4171e23, 3389.5e3, 227.92e9, "assets/textures/mars.jpg", "planet", None),
            ("Jupiter", 1.8982e27, 69911e3, 778.57e9, "assets/textures/jupiter.jpg", "planet", None),
            ("Saturn", 5.6834e26, 58232e3, 1433.53e9, "assets/textures/saturn.jpg", "planet", None),
            ("Uranus", 8.6810e25, 25362e3, 2872.46e9, "assets/textures/uranus.png", "planet", None),
            ("Neptune", 1.02413e26, 24622e3, 4495.06e9, "assets/textures/neptune.jpg", "planet", None),
        ]

        self.__objects: dict[str, CelestialBody] = {}

        for name, mass_kg, radius_m, a_m, texture, type, satellites in bodies:
            # Simulation radius is scaled for visibility, but we ensure a minimum size of 1 unit for very small planets.
            radius_sim = max((radius_m / SIZE_SCALE) * 0.2, 1)

            # Physics properties of the planet
            prop = PhysicsProperties(mass_kg, radius_sim, Vec3D(a_m, 0, 0))

            body: CelestialBody | None = None
            match type:
                case "star":
                    body = Star(name, prop, luminosity=1.0, light_color=Vec4(3.0, 2.6, 1.2, 1.0))
                    body.get_physics_properties().set_fixed(True)
                case "planet":
                    body = Planet(name, prop)

            body.set_texture(texture)

            if a_m != 0.0:
                v_real = math.sqrt(G * sun_mass / a_m)
            else:
                v_real = 0.0
            body.get_physics_properties().set_velocity(Vec3D(0, v_real, 0))
            print(body.get_name(), body.get_physics_properties().get_scaled_position(DISTANCE_SCALE), body.get_physics_properties().get_velocity(), body.get_physics_properties().get_position())

            if satellites is not None:
                self.__add_satellites(body, satellites)

            # Scale the model to match the simulation radius.
            try:
                body.get_model().setScale(radius_sim)
            except Exception as e:
                print(f"An exception occurred :\r{e}")

            # Adding the planet to the objects dictionary and the physics manager.
            self.__objects[name] = body

            body.get_model().reparentTo(self.render)
            self.__physics_manager.add_physics_object(body)

    def __add_satellites(self, body: CelestialBody, satellites: list[Satellite] | None) -> None:
        """
        Add satellites to a planet and set their initial positions and velocities.
        Args:
            body (CelestialBody): The planet to which the satellites will be added.
            satellites (list[Satellite] | None): A list of Satellite objects to be added to the planet. If None, no satellites will be added.
        """
        if satellites is not None:
            for satellite in satellites:
                satellite.get_model().reparentTo(self.render)
                self.__objects[satellite.get_name()] = satellite
                self.__physics_manager.add_physics_object(satellite)

                # Set the initial position of the satellite based on its physics properties.
                parent_pos = body.get_physics_properties().get_position()
                satellite.get_physics_properties().set_position(
                    Vec3D(parent_pos.getX() + satellite.get_distance_to_parent(), parent_pos.getY(), parent_pos.getZ()))

                radius_sim = max((satellite.get_physics_properties().get_radius() / SIZE_SCALE) * 0.2, 0.5)
                satellite.get_model().setScale(radius_sim)

                # Set the initial velocity of the satellite based on its physics properties.
                v_parent = body.get_physics_properties().get_velocity()
                v_real = math.sqrt(G * body.get_physics_properties().get_mass() / satellite.get_distance_to_parent())
                satellite.get_physics_properties().set_velocity(
                    v_parent + Vec3D(0, v_real, 0)
                )

                if isinstance(body, Planet):
                    body.add_satellite(satellite)

                print(satellite.get_name(), satellite.get_physics_properties().get_scaled_position(DISTANCE_SCALE), satellite.get_physics_properties().get_velocity(), satellite.get_physics_properties().get_position())

    def __init_tasks(self) -> None:
        """
        Initialize the main tasks for the application.
        """
        # TODO: Create an attribute that stores tasks in a dictionary [str, Task] and the iterate over it to add them to the task manager.
        self.taskMgr.add(self.__physics_manager.update, "Physics Update Task")
        # self.taskMgr.add(lambda task: self.set_camera_focus(self.__objects["Earth"].get_physics_properties().get_scaled_position(DISTANCE_SCALE)), "Camera Focus Task")

    def set_camera_focus(self, target: Vec3D) -> None:
        """
        Reset the focus of the scene camera to a specific target position.
        Args:
            target (Vec3D): The position to focus the camera on.
        """
        self.cam.setPos(target.getX(), target.getY(), target.getZ() + 5)
        self.cam.lookAt(target.getX(), target.getY(), target.getZ())


if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()