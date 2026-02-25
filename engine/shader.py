import os
from OpenGL.GL import *
import numpy as np


class Shader:
    def __init__(self, vertex_path, fragment_path):
        vertex_src = self._read_file(vertex_path)
        fragment_src = self._read_file(fragment_path)

        vertex_shader = self._compile(vertex_src, GL_VERTEX_SHADER)
        fragment_shader = self._compile(fragment_src, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program).decode()
            raise RuntimeError(f"Shader link error: {info}")

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        self._uniform_cache = {}

    def use(self):
        glUseProgram(self.program)

    def _get_loc(self, name):
        if name not in self._uniform_cache:
            self._uniform_cache[name] = glGetUniformLocation(self.program, name)
        return self._uniform_cache[name]

    def set_int(self, name, value):
        glUniform1i(self._get_loc(name), value)

    def set_float(self, name, value):
        glUniform1f(self._get_loc(name), value)

    def set_vec3(self, name, value):
        glUniform3f(self._get_loc(name), *value)

    def set_mat3(self, name, value):
        glUniformMatrix3fv(self._get_loc(name), 1, GL_TRUE, np.array(value, dtype=np.float32))

    def set_mat4(self, name, value):
        glUniformMatrix4fv(self._get_loc(name), 1, GL_TRUE, np.array(value, dtype=np.float32))

    def _read_file(self, path):
        with open(path, 'r') as f:
            return f.read()

    def _compile(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(shader).decode()
            kind = "Vertex" if shader_type == GL_VERTEX_SHADER else "Fragment"
            raise RuntimeError(f"{kind} shader compile error: {info}")
        return shader
