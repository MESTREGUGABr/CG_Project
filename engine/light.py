import math
import numpy as np


class SunLight:
    def __init__(self, orbit_radius=5.0, speed=30.0, color=(1.0, 1.0, 0.9), intensity=1.0):
        self.orbit_radius = orbit_radius
        self.speed = speed  # degrees per second
        self.angle = 0.0    # current angle in degrees
        self.color = list(color)
        self.intensity = intensity
        self.height = 4.0

    def update(self, dt):
        self.angle += self.speed * dt
        self.angle %= 360.0

    @property
    def position(self):
        x = self.orbit_radius * math.cos(math.radians(self.angle))
        z = self.orbit_radius * math.sin(math.radians(self.angle))
        return [x, self.height, z]

    @property
    def direction(self):
        pos = self.position
        length = math.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
        return [-pos[0]/length, -pos[1]/length, -pos[2]/length]

    def change_speed(self, delta):
        self.speed = max(5.0, min(200.0, self.speed + delta))

    def get_light_data(self):
        return {
            'type': 0,  # directional
            'position': self.position,
            'direction': self.direction,
            'color': self.color,
            'intensity': self.intensity,
            'cutoff': 0.0,
            'outerCutoff': 0.0,
        }


class SpotLight:
    def __init__(self, position, direction=(0, -1, 0), color=(1.0, 1.0, 1.0),
                 intensity=2.0, cutoff=25.0, outer_cutoff=35.0):
        self.position = list(position)
        self.direction = list(direction)
        self.color = list(color)
        self.intensity = intensity
        self.cutoff = math.cos(math.radians(cutoff))
        self.outer_cutoff = math.cos(math.radians(outer_cutoff))

    def get_light_data(self):
        return {
            'type': 1,  # point/spot
            'position': self.position,
            'direction': self.direction,
            'color': self.color,
            'intensity': self.intensity,
            'cutoff': self.cutoff,
            'outerCutoff': self.outer_cutoff,
        }


class SpotLightManager:
    """Manages multiple spotlights."""
    MAX_SPOTLIGHTS = 9  # reserve 1 slot for other lights

    def __init__(self):
        self.lights = []

    def add_spotlight(self, camera_pos, camera_target):
        if len(self.lights) >= self.MAX_SPOTLIGHTS:
            print(f"Maximum of {self.MAX_SPOTLIGHTS} spotlights reached.")
            return
        direction = camera_target - camera_pos
        length = np.linalg.norm(direction)
        if length > 0:
            direction = direction / length
        light = SpotLight(
            position=camera_pos.tolist(),
            direction=direction.tolist(),
            color=[1.0, 1.0, 1.0],
            intensity=2.5,
        )
        self.lights.append(light)
        print(f"Spotlight added ({len(self.lights)} total)")

    def clear(self):
        self.lights.clear()
        print("All spotlights cleared")

    def get_all_light_data(self):
        return [l.get_light_data() for l in self.lights]
