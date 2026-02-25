import math
import numpy as np
from engine.transform import look_at


class Camera:
    def __init__(self, target=(0, 0, 0), distance=3.0, yaw=-90.0, pitch=20.0):
        self.target = np.array(target, dtype=np.float32)
        self.distance = distance
        self.yaw = yaw
        self.pitch = pitch
        self.min_distance = 0.5
        self.max_distance = 20.0
        self.min_pitch = -89.0
        self.max_pitch = 89.0
        self.sensitivity = 0.3
        self.zoom_speed = 0.5

    @property
    def position(self):
        x = self.distance * math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
        y = self.distance * math.sin(math.radians(self.pitch))
        z = self.distance * math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
        return self.target + np.array([x, y, z], dtype=np.float32)

    def get_view_matrix(self):
        return look_at(self.position, self.target, [0.0, 1.0, 0.0])

    def rotate(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch += dy * self.sensitivity
        self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch))

    def zoom(self, amount):
        self.distance -= amount * self.zoom_speed
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))
