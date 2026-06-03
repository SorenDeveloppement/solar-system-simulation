from direct.task import Task
from panda3d.core import Camera, Light

from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.physics_manager import PhysicsManager


class Scene:
    """
    Base class for all scenes in the application. It manages the celestial bodies and the physics simulation.
    Stores cameras, lights, and other scene-related objects.
    """
    def __init__(self, name: str) -> None:
        """
        Init method of the Scene class. Initializes the scene with a name, an empty dictionary for celestial bodies, and a physics manager instance.
        Args:
            name (str): The name of the scene.
        """
        self.__name = name
        self.__objects: dict[str, CelestialBody] = {}
        self.__physics_manager = PhysicsManager()
        self.__cameras: dict[str, Camera] = {}
        self.__lights: list[Light] = []

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

    def add_camera(self, name: str, camera: Camera) -> None:
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

    def get_physics_manager(self) -> PhysicsManager:
        """
        Getter for the physics manager of the scene.
        Returns:
            PhysicsManager: The physics manager instance of the scene.
        """
        return self.__physics_manager

    def get_cameras(self) -> dict[str, Camera]:
        """
        Getter for the cameras in the scene.
        Returns:
            dict[str, Camera]: A dictionary of cameras in the scene, where the key is the name of the camera and the value is the Camera instance.
        """
        return self.__cameras

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