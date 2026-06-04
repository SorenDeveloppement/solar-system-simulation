import os.path
from typing import Self, Any

import yaml

from panda3d.core import NodePath, Light, Vec3D, Vec4D

from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.celestial.planet import Planet
from src.core.physics.celestial.satellite import Satellite
from src.core.physics.celestial.star import Star
from src.utils.vecs import vec3d_as_tuple, vec4d_as_tuple


class SceneSaver:
    """
    SceneSaver class is responsible for saving the current state of the scene to a file. It provides functionality to serialize the scene data and write it to a specified location on disk.
    """
    def __init__(self) -> None:
        """
        Initializes the SceneSaver instance.
        """
        self.__scene_name: str = str()
        self.__scene_objects: dict[str, dict[str, Any]] = {}
        self.__scene_cameras: dict[str, dict[str, tuple[float, float, float]]] = {}
        self.__scene_lights: list[dict[str, Any]] = []
        self.__scene_other_properties: dict[str, Any] = {}

    def save_scene(self, file_name: str, path: str) -> None:
        """
        Saves the current state of the scene to a file.
        Args:
            file_name (str): The name of the file to save the scene to.
            path (str): The directory path where the file should be saved.
        """
        if not os.path.exists(path):
            os.mkdir(path)

        data: dict[str, Any] = {
            "scene_name": self.__scene_name,
            "objects": self.__scene_objects,
            "cameras": self.__scene_cameras,
            "lights": self.__scene_lights,
            "other_properties": self.__scene_other_properties
        }

        with open(f"{path}/{file_name}.yaml", "w") as file:
            yaml.dump(data, file)
            file.close()

    def name(self, name: str) -> Self:
        """
        Sets the name of the scene to be saved.
        Args:
            name (str): The name of the scene.
        Returns:
            Self: The SceneSaver instance for method chaining.
        """
        self.__scene_name = name
        return self

    def objects(self, objects: dict[str, CelestialBody]) -> Self:
        """
        Sets the list of objects in the scene to be saved.
        Args:
            objects (dict[str, CelestialBody]): A dictionary of celestial bodies in the scene, where the key is the name of the body and the value is the CelestialBody instance.
        Returns:
            Self: The SceneSaver instance for method chaining.
        """
        for name, obj in objects.items():
            if isinstance(obj, Star):
                self.__scene_objects[name] = {
                    "type": "Star",
                    "luminosity": obj.get_luminosity(),
                    "light_color": vec4d_as_tuple(obj.get_light_color())
                }
            elif isinstance(obj, Planet):
                self.__scene_objects[name] = {
                    "type": "Planet",
                    "has_atmosphere": obj.has_atmosphere(),
                    "surface_gravity": obj.get_surface_gravity()
                }
            elif isinstance(obj, Satellite):
                self.__scene_objects[name] = {
                    "type": "Satellite",
                    "parent_planet": obj.get_parent_planet(),
                    "distance_to_parent": obj.get_distance_to_parent()
                }
            else:
                self.__scene_objects[name] = {
                    "type": "CelestialBody"
                }
            self.__scene_objects[name]["physics_properties"] = {}
            for p_name, property in obj.get_physics_properties().as_dict().items():
                if isinstance(property, Vec3D):
                    self.__scene_objects[name]["physics_properties"][p_name] = vec3d_as_tuple(property)
                elif isinstance(property, Vec4D):
                    self.__scene_objects[name]["physics_properties"][p_name] = vec4d_as_tuple(property)
                else:
                    self.__scene_objects[name]["physics_properties"][p_name] = property
        return self

    def cameras(self, cameras: dict[str, NodePath]) -> Self:
        """
        Sets the list of cameras in the scene to be saved.
        Args:
            cameras (dict[str, NodePath]): A dictionary of cameras in the scene, where the key is the name of the camera and the value is the NodePath instance representing the camera.
        Returns:
            Self: The SceneSaver instance for method chaining.
        """
        for name, camera in cameras.items():
            pos = camera.getPos()
            hpr = camera.getHpr()
            look_at = camera.getLookAt()
            self.__scene_cameras[name] = {
                "position": vec3d_as_tuple(pos),
                "hpr": vec3d_as_tuple(hpr),
                "look_at": vec3d_as_tuple(look_at)
            }
        return self

    def lights(self, lights: list[Light]) -> Self:
        """
        Sets the list of lights in the scene to be saved.
        Args:
            lights (list[Light]): A list of Light instances representing the lights in the scene.
        Returns:
            Self: The SceneSaver instance for method chaining.
        """
        for light in lights:
            self.__scene_lights.append({
                "type": type(light).__name__,
                "position": vec3d_as_tuple(light.getPos()),
                "color": vec4d_as_tuple(light.getColor())
            })
        return self
