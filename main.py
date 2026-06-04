from direct.filter.CommonFilters import CommonFilters
from panda3d.core import WindowProperties, Vec4, Vec3D, PointLight, Material, NodePath, PerspectiveLens, Camera
from direct.showbase.ShowBase import ShowBase

from src.constants import DISTANCE_SCALE
from src.core.scenes.scene import Scene


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

        self.__scene: Scene = Scene(self, "Solar System")

        # ---------------------------- #
        #    Physics & Objects Setup   #
        # ---------------------------- #

        # ---------------------------- #
        #       Task Management        #
        # ---------------------------- #

        self.__init_tasks()

    def __init_tasks(self) -> None:
        """
        Initialize the main tasks for the application.
        """
        # TODO: Create an attribute that stores tasks in a dictionary [str, Task] and then iterate over it to add them to the task manager.
        # Physics update should run continuously
        self.taskMgr.add(self.__scene.get_physics_manager().update, "Physics Update Task")

        # Camera focus task: must return task.cont to continue running each frame
        def camera_focus_task(task):
            # Move camera to follow Earth (scaled position)
            target = self.__scene.get_object_by_name("Earth").get_physics_properties().get_scaled_position(DISTANCE_SCALE)
            self.set_camera_focus(target)
            return task.cont

        # Focus Earth for tests purposes
        # self.taskMgr.add(camera_focus_task, "Camera Focus Task")

    def set_camera_focus(self, target: Vec3D) -> None:
        """
        Reset the focus of the scene camera to a specific target position.
        Args:
            target (Vec3D): The position to focus the camera on.
        """
        self.cam.setPos(target.getX() - 15, target.getY() - 15, target.getZ() + 25)
        self.cam.lookAt(target.getX(), target.getY(), target.getZ())

    def switch_to_cam(self, camera: NodePath) -> None:
        """
        Switch the current camera to a new camera.
        Args:
            camera (NodePath): The new camera to switch to.
        """
        if camera is None:
            raise ValueError("Camera cannot be None.")

        self.win.getDisplayRegion(0).setCamera(camera)

        self.cam = camera
        self.camera = camera
        self.camNode = camera.node()

    def create_camera(self, name: str, position: tuple[float, float, float], look_at: tuple[float, float, float]) -> NodePath:
        """
        Static method to create a camera with a given name, position, and look-at point.
        Args:
            name (str): The name of the camera.
            position (tuple[float, float, float]): The position of the camera in the scene as a tuple of (x, y, z) coordinates.
            look_at (tuple[float, float, float]): The point that the camera should look at in the scene as a tuple of (x, y, z) coordinates.
        Returns:
            Camera: A new Camera instance with the specified properties.
        """
        cam_node = Camera(name)
        cam_np = self.render.attachNewNode(cam_node)
        cam_np.setPos(*position)
        cam_np.lookAt(*look_at)

        lens = PerspectiveLens()
        cam_node.setLens(lens)
        return cam_np

    def get_render(self) -> NodePath:
        """
        Getter for the render node of the scene.
        Returns:
            NodePath: The render node of the scene.
        """
        return self.render


if __name__ == "__main__":
    app = SolarSystemApp()
    app.run()