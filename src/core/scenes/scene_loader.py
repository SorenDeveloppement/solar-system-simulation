from __future__ import annotations
from typing import Any

import yaml
from panda3d.core import Vec4D, Vec3D, PointLight, DirectionalLight, Spotlight
from typing import TYPE_CHECKING

from src.constants import SIZE_SCALE
from src.core.physics.celestial.celestial_body import CelestialBody
from src.core.physics.celestial.planet import Planet
from src.core.physics.celestial.satellite import Satellite
from src.core.physics.celestial.star import Star
from src.core.physics.properties.physics_properties import PhysicsProperties
from src.core.scenes.scene import Scene
from src.utils.vecs import tuple_as_vec4d, tuple_as_vec3d, tuple_as_vec4f

if TYPE_CHECKING:
    from main import SolarSystemApp


class SceneLoader:
    """
    Loads a scene from a file and creates the necessary objects and components.
    """
    def __init__(self, parent: SolarSystemApp, path: str) -> None:
        """
        Initializes the SceneLoader instance.

        Args:
            path (str): The file path to load the scene from.
        """
        self.__scene_path: str = path

        self.__loaded_scene: Scene = Scene(parent, "")

        self.__scene_other_properties: dict[str, Any] = {}

    def load(self) -> Scene | None:
        """
        Loads the scene from the specified file path and creates a Scene instance.

        Returns:
            Scene: The loaded Scene instance.
        """
        with open(self.__scene_path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        if data is None:
            raise ValueError(f"Failed to load scene from {self.__scene_path}.")

        if not data.get("type") == "SceneData":
            raise ValueError(f"Invalid scene data in {self.__scene_path}. Expected type 'SceneData', got '{data.get('type')}'.")

        # TODO: Add compatibility check for app version.
        #  But it doesn't mean that the file is incompatible, different versions may have the same Saver/Loader structure.

        self.__loaded_scene.set_name(data.get("scene_name", ""))

        self.__load_objects(data.get("objects", {}))
        self.__load_cameras(data.get("cameras", {}))
        self.__load_lights(data.get("lights", []))
        self.__load_other_properties(data.get("other_properties", {}))

        return self.__loaded_scene

    def __reparent_obj(self, obj: CelestialBody) -> None:
        """
        Reparents the given celestial body object to the scene's root node.

        Args:
            obj (CelestialBody): The celestial body object to be reparented.
        """
        obj.get_model().reparentTo(self.__loaded_scene.get_parent().get_render())

    def __load_objects(self, objects_data: dict[str, Any]) -> None:
        """
        Loads the objects from the scene data and creates the corresponding objects in the scene.

        Args:
            objects_data (dict[str, Any]): The dictionary containing the objects data to be loaded.
        """
        for name, obj_data in objects_data.items():
            obj_type = obj_data.get("type")
            match obj_type:
                case "Star":
                    self.__load_star_obj(name, obj_data)
                case "Planet":
                    self.__load_planet_obj(name, obj_data)
                case "Satellite":
                    self.__load_satellite_obj(name, obj_data)
                case _:
                    self.__load_generic_celestial_body(name, obj_data)

    def __load_star_obj(self, name: str, obj_data: dict[str, Any]) -> None:
        """
        Loads a star object from the scene data and creates the corresponding star in the scene.

        Args:
            name (str): The name of the star object to be loaded.
            obj_data (dict[str, Any]): The dictionary containing the star object data to be loaded.
        """
        luminosity: float = obj_data.get("luminosity", 1.0)
        light_color: Vec4D = tuple_as_vec4f(obj_data.get("light_color", (1.0, 1.0, 1.0, 1.0)))
        texture: str | None = obj_data.get("texture", None)

        physics_prop: PhysicsProperties = SceneLoader._load_physics_properties(obj_data.get("physics_properties", {}))

        obj: Star = Star(name, physics_prop, luminosity, light_color)
        if texture is not None:
            obj.set_texture(texture)
        self.__reparent_obj(obj)

        self.__loaded_scene.add_object(name, obj)

    def __load_planet_obj(self, name: str, obj_data: dict[str, Any]) -> None:
        """
        Loads a planet object from the scene data and creates the corresponding planet in the scene.

        Args:
            name (str): The name of the planet object to be loaded.
            obj_data (dict[str, Any]): The dictionary containing the planet object data to be loaded.
        """
        has_atmosphere: bool = obj_data.get("has_atmosphere", False)
        surface_gravity: float = obj_data.get("surface_gravity", 1.0)
        physics_prop: PhysicsProperties = SceneLoader._load_physics_properties(obj_data.get("physics_properties", {}))
        texture: str | None = obj_data.get("texture", None)
        # Satellites will be added in self.__load_satellite_obj.

        obj: Planet = Planet(name, physics_prop, has_atmosphere, surface_gravity)
        if texture is not None:
            obj.set_texture(texture)

        radius_sim = max((obj.get_physics_properties().get_radius() / SIZE_SCALE) * 0.2, 1)
        obj.get_model().setScale(radius_sim)
        self.__reparent_obj(obj)

        self.__loaded_scene.add_object(name, obj)

    def __load_satellite_obj(self, name: str, obj_data: dict[str, Any]) -> None:
        """
        Loads a satellite object from the scene data and creates the corresponding satellite in the scene.

        Args:
            name (str): The name of the satellite object to be loaded.
            obj_data (dict[str, Any]): The dictionary containing the satellite object data to be loaded.
        """
        parent_planet_name: str = obj_data.get("parent_planet", "")
        distance_to_parent: float = obj_data.get("distance_to_parent", 1.0)
        physics_prop: PhysicsProperties = SceneLoader._load_physics_properties(obj_data.get("physics_properties", {}))
        texture: str | None = obj_data.get("texture", None)

        obj: Satellite = Satellite(name, physics_prop, parent_planet_name, distance_to_parent)
        if texture is not None:
            obj.set_texture(texture)

        radius_sim = max(
            (obj.get_physics_properties().get_radius() / SIZE_SCALE) * 0.2,
            0.5
        )
        obj.get_model().setScale(radius_sim)
        self.__reparent_obj(obj)

        self.__loaded_scene.add_object(name, obj)

        body = self.__loaded_scene.get_object_by_name(parent_planet_name)
        if isinstance(body, Planet):
            body.add_satellite(obj)

    def __load_generic_celestial_body(self, name: str, obj_data: dict[str, Any]) -> None:
        """
        Loads a generic celestial body object from the scene data and creates the corresponding celestial body in the scene.

        Args:
            name (str): The name of the celestial body object to be loaded.
            obj_data (dict[str, Any]): The dictionary containing the celestial body object data to be loaded.
        """
        physics_prop: PhysicsProperties = SceneLoader._load_physics_properties(obj_data.get("physics_properties", {}))

        obj: CelestialBody = CelestialBody(name, physics_prop)
        self.__reparent_obj(obj)

        self.__loaded_scene.add_object(name, obj)

    def __load_cameras(self, cameras_data: dict[str, Any]) -> None:
        """
        Loads the cameras from the scene data and creates the corresponding cameras in the scene.

        Args:
            cameras_data (dict[str, Any]): The dictionary containing the cameras data to be loaded.
        """
        for name, cam_data in cameras_data.items():
            position: tuple[float, float, float] = cam_data.get("position", (0.0, 0.0, 0.0))
            look_at: tuple[float, float, float] = cam_data.get("look_at", (0.0, 0.0, 0.0))

            camera = self.__loaded_scene.get_parent().create_camera(name, position, look_at)
            self.__loaded_scene.add_camera(name, camera)

    def __load_lights(self, lights_data: list[dict[str, Any]]) -> None:
        """
        Loads the lights from the scene data and creates the corresponding lights in the scene.

        Args:
            lights_data (list[dict[str, Any]]): The list of dictionaries containing the lights data to be loaded.
        """
        lights_type_mapping: dict[str, Any] =  {
            "PointLight": PointLight,
            "DirectionalLight": DirectionalLight,
            "Spotlight": Spotlight
        }
        for light_data in lights_data:
            light_type: str | None = light_data.get("type", None)

            if light_type is None:
                continue

            name: str = light_data.get("name", "Unnamed Light")
            color: Vec4D = tuple_as_vec4d(light_data.get("color", (1.0, 1.0, 1.0, 1.0)))
            position: Vec3D = tuple_as_vec3d(light_data.get("position", (0.0, 0.0, 0.0)))
            direction: Vec3D = tuple_as_vec3d(light_data.get("direction", (0.0, -1.0, 0.0)))

            light = lights_type_mapping[light_type](name)
            light.setColor(color)
            light.setPosition(position)

            if isinstance(light, (DirectionalLight, Spotlight)):
                light.setDirection(direction)

            self.__loaded_scene.get_parent().get_render().setLight(light)

            self.__loaded_scene.add_light(light)

    def __load_other_properties(self, other_properties_data: dict[str, Any]) -> None:
        """
        Loads the other properties from the scene data and stores them in the SceneLoader instance.

        Args:
            other_properties_data (dict[str, Any]): The dictionary containing the other properties data to be loaded.
        """
        self.__scene_other_properties = other_properties_data

    @staticmethod
    def _load_physics_properties(physics_data: dict[str, Any]) -> PhysicsProperties:
        """
        Loads the physics properties from the scene data and creates a PhysicsProperties instance.

        Args:
            physics_data (dict[str, Any]): The dictionary containing the physics properties data to be loaded.
        Returns:
            PhysicsProperties: The loaded PhysicsProperties instance.
        """
        mass: float = physics_data.get("mass", 1.0)
        radius: float = physics_data.get("radius", 1.0)
        position: Vec3D = tuple_as_vec3d(physics_data.get("position", (0.0, 0.0, 0.0)))
        velocity: Vec3D = tuple_as_vec3d(physics_data.get("velocity", (0.0, 0.0, 0.0)))
        fixed: bool = physics_data.get("fixed", False)
        rotation_speed: float = physics_data.get("rotation_speed", 0.0)
        orbital_inclination: float = physics_data.get("orbital_inclination", 0.0)

        props = PhysicsProperties(mass, radius, position, fixed, rotation_speed, orbital_inclination)
        props.set_velocity(velocity)

        return props
