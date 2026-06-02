"""Physical constants used in the project."""

G: float = 6.67430e-11
"""Gravitational constant in m^3 kg^-1 s^-2 or N m^2 kg^-2"""

AU: float = 149597870700
"""Astronomical Unit in meters"""

DISTANCE_SCALE = AU * 1E-2
"""Scene distance scale factor. 1 unit in the scene corresponds to 3e11 meters in real life."""

MASS_SCALE = 1e21
"""Scene mass scale factor. 1 unit of mass in the scene corresponds to 1e21 kg in real life."""

TIME_SCALE = 86400 * 7
"""Scene time scale factor. 1 second in the scene corresponds to 86400 seconds (1 day) in real life."""
