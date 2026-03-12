import math
import numpy as np
from OpenGL.GL import *
import ctypes


class Room:
    def __init__(self, size=6.0, height=4.0, pedestal_radius=0.6, pedestal_height=0.15, segments=40):
        self.vao = None
        self.vbo = None
        self.vertex_count = 0
        self.pedestal_top_y = -1.0 + pedestal_height  # exposto para o scene usar
        self._setup(size, height, pedestal_radius, pedestal_height, segments)

    def _quad(self, p0, p1, p2, p3, normal):
        verts = []
        for p in [p0, p1, p2, p0, p2, p3]:
            verts.extend(p)
            verts.extend(normal)
        return verts

    def _cylinder_top(self, cy, radius, segments):
        """Disco superior do cilindro."""
        verts = []
        for i in range(segments):
            a0 = 2 * math.pi * i / segments
            a1 = 2 * math.pi * (i + 1) / segments
            center = [0.0, cy, 0.0];  n = [0.0, 1.0, 0.0]
            p0 = [math.cos(a0) * radius, cy, math.sin(a0) * radius]
            p1 = [math.cos(a1) * radius, cy, math.sin(a1) * radius]
            verts.extend(center + n); verts.extend(p0 + n); verts.extend(p1 + n)
        return verts

    def _cylinder_sides(self, cy_bot, cy_top, radius, segments):
        """Lados do cilindro com normais suaves por vértice."""
        verts = []
        for i in range(segments):
            a0 = 2 * math.pi * i / segments
            a1 = 2 * math.pi * (i + 1) / segments
            n0 = [math.cos(a0), 0.0, math.sin(a0)]
            n1 = [math.cos(a1), 0.0, math.sin(a1)]
            bl = [math.cos(a0)*radius, cy_bot, math.sin(a0)*radius]
            br = [math.cos(a1)*radius, cy_bot, math.sin(a1)*radius]
            tl = [math.cos(a0)*radius, cy_top, math.sin(a0)*radius]
            tr = [math.cos(a1)*radius, cy_top, math.sin(a1)*radius]
            verts.extend(bl+n0); verts.extend(tl+n0); verts.extend(br+n1)
            verts.extend(br+n1); verts.extend(tl+n0); verts.extend(tr+n1)
        return verts

    def _setup(self, s, h, pr, ph, segments):
        floor_y = -1.0
        top_y   = floor_y + ph
        verts = []

        # Paredes da sala (iguais ao anterior)
        verts += self._quad([-s,floor_y,-s],[s,floor_y,-s],[s,floor_y,s],[-s,floor_y,s],[0,1,0])
        verts += self._quad([-s,floor_y+h,-s],[-s,floor_y+h,s],[s,floor_y+h,s],[s,floor_y+h,-s],[0,-1,0])
        verts += self._quad([-s,floor_y,-s],[-s,floor_y+h,-s],[s,floor_y+h,-s],[s,floor_y,-s],[0,0,1])
        verts += self._quad([s,floor_y,s],[s,floor_y+h,s],[-s,floor_y+h,s],[-s,floor_y,s],[0,0,-1])
        verts += self._quad([-s,floor_y,s],[-s,floor_y+h,s],[-s,floor_y+h,-s],[-s,floor_y,-s],[1,0,0])
        verts += self._quad([s,floor_y,-s],[s,floor_y+h,-s],[s,floor_y+h,s],[s,floor_y,s],[-1,0,0])

        # Pedestal redondo
        verts += self._cylinder_top(top_y, pr, segments)
        verts += self._cylinder_sides(floor_y, top_y, pr, segments)

        data = np.array(verts, dtype=np.float32)
        self.vertex_count = len(data) // 6

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        stride = 6 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3*4))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        glBindVertexArray(0)

    def cleanup(self):
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(1, [self.vbo])