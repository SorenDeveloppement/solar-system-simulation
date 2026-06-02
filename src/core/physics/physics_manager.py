from direct.task import Task
from panda3d.core import Vec3D

from src.constants import G
from src.core.physics.celestial.celestial_body import CelestialBody


class PhysicsManager:
    """
    The PhysicsManager class is responsible for managing the physics simulation of the celestial bodies in the solar system. It keeps track of all the physics objects (celestial bodies) and updates their positions and velocities based on the gravitational forces between them.
    """
    def __init__(self) -> None:
        """
        Init method of the physics manager.
        """
        self.__physics_objects: list[CelestialBody] = []

    def add_physics_object(self, physics_object: CelestialBody) -> None:
        """
        Add a physics object to the manager.
        Args:
            physics_object (CelestialBody): The physics object to be added to the manager.
        """
        self.__physics_objects.append(physics_object)

    def remove_physics_object(self, physics_object: CelestialBody) -> None:
        """
        Remove a physics object from the manager. This is useful when an object is destroyed or removed from the simulation.
        Args:
            physics_object (CelestialBody): The physics object to be removed from the manager.
        """
        if physics_object in self.__physics_objects:
            self.__physics_objects.remove(physics_object)

    def update(self, task: Task) -> None:
        """
        Update function of the physics manager, responsible for calculating the gravitational forces between all objects in space and updating their positions and velocities accordingly.

        This function is called every frame by the task manager.
        Args:
            task (Task): The task object provided by the Panda3D task manager, which allows us to control the execution of this function and access timing information.
        """
        # Each object in space interacts with others through gravity, so we need to calculate the forces between them and apply them to their physics properties.
        for i, object1 in enumerate(self.__physics_objects):
            # No need to calculate again the same pair of objects, so we start the inner loop from the next index.
            for object2 in self.__physics_objects[i+1:]:
                # Quick check to avoid self-interaction
                if object1 is not object2:
                    # Recovering physics properties of both objects.
                    prop1 = object1.get_physics_properties()
                    prop2 = object2.get_physics_properties()

                    # Calculus of the gravitational force between object1 and object2 using Newton's law of universal gravitation: F = G * (m1 * m2) / d^2
                    distance = (prop1.get_position() - prop2.get_position()).length()
                    F: float = G * (prop1.get_mass() * prop2.get_mass()) / (distance ** 2)

                    # The direction of the force is from object1 to object2, so we need to calculate the unit vector in that direction and multiply it by the force magnitude to get the force vector.
                    direction: Vec3D = Vec3D.normalized(prop2.get_position() - prop1.get_position())

                    # Finally, we apply the force to both objects. The force on object1 is in the direction of object2, while the force on object2 is in the opposite direction (Newton's third law).
                    if not object1.get_name() == "Sun":
                        object1.get_physics_properties().apply_force(direction * F)

                    if not object2.get_name() == "Sun":
                        object2.get_physics_properties().apply_force(-direction * F)

        for obj in self.__physics_objects:
            obj.update()

        return task.cont
