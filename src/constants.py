"""Physical constants used in the project.
And apps constants."""

G: float = 6.67430e-11
"""Gravitational constant in m^3 kg^-1 s^-2 or N m^2 kg^-2"""

AU: float = 149597870700
"""Astronomical Unit in meters"""

SIZE_SCALE = 1e6
"""Scene size scale factor. 1 unit in the scene corresponds to 10 meters in real life."""

DISTANCE_SCALE = 1e8
"""Scene distance scale factor. 1 unit in the scene corresponds to 3e11 meters in real life."""

MASS_SCALE = 1e21
"""Scene mass scale factor. 1 unit of mass in the scene corresponds to 1e21 kg in real life."""

TIME_SCALE = 86400
"""Scene time scale factor. 1 second in the scene corresponds to 86400 seconds (1 day) in real life."""

APP_VERSION: str = "0.1.0"
"""Version of the application. Useful for scene saving/loading to ensure compatibility."""