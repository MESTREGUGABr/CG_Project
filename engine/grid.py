import numpy as np
from OpenGL.GL import *
import ctypes


class Grid:
    def __init__(self, size=8.0, y=-1.0):
        self.vao = None
        self.vbo = None
        self._setup(size, y)

    def _setup(self, size, y):
        # Simple ground plane quad
        vertices = np.array([
            -size, y, -size,
             size, y, -size,
             size, y,  size,
            -size, y, -size,
             size, y,  size,
            -size, y,  size,
        ], dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

    def cleanup(self):
        if self.vao is not None:
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(1, [self.vbo])
