from src.core.scenes.scene import Scene


class SceneManager:
    """
    Manages different scenes in the game, allowing for easy switching between them.
    """
    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None

    # ---------------------------- #
    #           Methods            #
    # ---------------------------- #

    def add_scene(self, name: str, scene: Scene) -> None:
        self.scenes[name] = scene

    # ---------------------------- #
    #           Getters            #
    # ---------------------------- #

    def get_current_scene(self) -> Scene | None:
        return self.current_scene

    def get_scenes(self) -> dict[str, Scene]:
        return self.scenes

    # ---------------------------- #
    #           Setters            #
    # ---------------------------- #

    def set_current_scene(self, name: str) -> None:
        if name in self.scenes:
            self.current_scene = self.scenes[name]
        else:
            raise ValueError(f"Scene '{name}' not found in SceneManager.")