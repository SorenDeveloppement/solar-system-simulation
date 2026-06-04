from __future__ import annotations

import math

from direct.task import Task
from panda3d.core import NodePath, Light, Vec3D, Vec4
from typing import TYPE_CHECKING

from src.constants import SIZE_SCALE, DISTANCE_SCALE, G
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.celestial.planet import Planet
from src.core.physics.celestial.satellite import Satellite
from src.core.physics.celestial.star import Star
from src.core.physics.physics_manager import PhysicsManager
from src.core.physics.properties.physics_properties import PhysicsProperties

if TYPE_CHECKING:
    from main import SolarSystemApp


class Scene:
    """
    Base class for all scenes in the application. It manages the celestial bodies and the physics simulation.
    Stores cameras, lights, and other scene-related objects.
    """
    def __init__(self, parent: SolarSystemApp, name: str) -> None:
        """
        Init method of the Scene class. Initializes the scene with a name, an empty dictionary for celestial bodies, and a physics manager instance.
        Args:
            name (str): The name of the scene.
        """
        self.__parent: SolarSystemApp = parent
        self.__name = name
        self.__objects: dict[str, CelestialBody] = {}
        self.__physics_manager = PhysicsManager()
        self.__cameras: dict[str, NodePath] = {}
        self.__lights: list[Light] = []

        # Initialisation of the scene
        # TODO: Remove hardcoded celestial bodies initialization
        self.__init_celestial_bodies()

    # ---------------------------- #
    #           Methods            #
    # ---------------------------- #

    def add_object(self, name: str, body: CelestialBody) -> None:
        """
        Adds a celestial body to the scene and the physics manager.
        Args:
            name (str): The name of the celestial body.
            body (CelestialBody): The CelestialBody instance to be added to the scene.
        """
        self.__objects[name] = body
        self.__physics_manager.add_physics_object(body)

    def add_camera(self, name: str, camera: NodePath) -> None:
        """
        Adds a camera to the scene.
        Args:
            name (str): The name of the camera.
            camera (Camera): The Camera instance to be added to the scene.
        """
        self.__cameras[name] = camera

    def add_light(self, light: Light) -> None:
        """
        Adds a light to the scene.
        Args:
            light (Light): The Light instance to be added to the scene.
        """
        self.__lights.append(light)

    def remove_object(self, name: str) -> None:
        """
        Removes a celestial body from the scene and the physics manager.
        Args:
            name (str): The name of the celestial body to be removed from the scene.
        """
        if name in self.__objects:
            body = self.__objects[name]
            del self.__objects[name]
            self.__physics_manager.remove_physics_object(body)

    def remove_camera(self, name: str) -> None:
        """
        Removes a camera from the scene.
        Args:
            name (str): The name of the camera to be removed from the scene.
        """
        if name in self.__cameras:
            del self.__cameras[name]

    def remove_light(self, light: Light) -> None:
        """
        Removes a light from the scene.
        Args:
            light (Light): The Light instance to be removed from the scene.
        """
        if light in self.__lights:
            self.__lights.remove(light)

    def update(self, task: Task) -> Task:
        """
        Updates the scene. This method should be called every frame to update the physics simulation and any other necessary updates.
        """
        return self.__physics_manager.update(task)

    def load_scene(self, scene_path: str) -> None:
        """
        Loads a scene from a file. This method should be implemented by subclasses to load specific scenes.
        The file format must be yaml.
        Args:
            scene_path (str): The path to the scene file to be loaded.
        """
        # TODO: Implement a method to load a scene from a yaml file.
        raise NotImplementedError("The load_scene method must be implemented before being used.")

    def save_scene(self, scene_path: str) -> None:
        """
        Saves the current scene to a file. This method should be implemented by subclasses to save specific scenes.
        Args:
            scene_path (str): The path to the scene file to be saved.
        """
        # TODO: Implement a method to save the current scene to a yaml file.
        raise NotImplementedError("The save_scene method must be implemented before being used.")

    # ---------------------------- #
    #            Getters           #
    # ---------------------------- #

    def get_name(self) -> str:
        """
        Getter for the name of the scene.
        Returns:
            str: The name of the scene.
        """
        return self.__name

    def get_objects(self) -> dict[str, CelestialBody]:
        """
        Getter for the celestial bodies in the scene.
        Returns:
            dict[str, CelestialBody]: A dictionary of celestial bodies in the scene, where the key is the name of the body and the value is the CelestialBody instance.
        """
        return self.__objects

    def get_object_by_name(self, name: str) -> CelestialBody | None:
        """
        Getter for a specific celestial body in the scene by its name.
        Args:
            name (str): The name of the celestial body to be retrieved.
        Returns:
            CelestialBody | None: The CelestialBody instance with the specified name, or None if no body with that name exists in the scene.
        """
        return self.__objects.get(name, None)

    def get_physics_manager(self) -> PhysicsManager:
        """
        Getter for the physics manager of the scene.
        Returns:
            PhysicsManager: The physics manager instance of the scene.
        """
        return self.__physics_manager

    def get_cameras(self) -> dict[str, NodePath]:
        """
        Getter for the cameras in the scene.
        Returns:
            dict[str, Camera]: A dictionary of cameras in the scene, where the key is the name of the camera and the value is the Camera instance.
        """
        return self.__cameras

    def get_cameras_names(self) -> list[str]:
        """
        Getter for the names of the cameras in the scene.
        Returns:
            list[str]: A list of the names of the cameras in the scene.
        """
        return list(self.__cameras.keys())

    def get_camera_by_name(self, name: str) -> NodePath | None:
        """
        Getter for a specific camera in the scene by its name.
        Args:
            name (str): The name of the camera to be retrieved.
        Returns:
            Camera | None: The Camera instance with the specified name, or None if no camera with that name exists in the scene.
        """
        return self.__cameras.get(name, None)

    def get_lights(self) -> list[Light]:
        """
        Getter for the lights in the scene.
        Returns:
            list[Light]: A list of Light instances in the scene.
        """
        return self.__lights

    # ---------------------------- #
    #            Setters           #
    # ---------------------------- #

    def set_name(self, name: str) -> None:
        """
        Setter for the name of the scene.
        Args:
            name (str): The new name of the scene.
        """
        self.__name = name

    # ---------------------------- #
    #     Stuff to remove later    #
    # ---------------------------- #

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

        for name, mass_kg, radius_m, a_m, texture, c_type, satellites in bodies:
            # Simulation radius is scaled for visibility, but we ensure a minimum size of 1 unit for very small planets.
            radius_sim = max((radius_m / SIZE_SCALE) * 0.2, 1)

            # Physics properties of the planet
            prop = PhysicsProperties(mass_kg, radius_sim, Vec3D(a_m, 0, 0))

            body: CelestialBody | None = None
            match c_type:
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

            body.get_model().reparentTo(self.__parent.get_render())
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
                satellite.get_model().reparentTo(self.__parent.get_render())
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