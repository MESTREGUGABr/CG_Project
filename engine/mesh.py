import numpy as np
from OpenGL.GL import *


class Mesh:
    def __init__(self, name=""):
        self.name = name
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.index_count = 0

    def load_obj(self, filepath):
        positions = []
        normals = []
        raw_faces = []  # list of face vertex tuples (v_idx, n_idx)
        has_normals = False

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if parts[0] == 'v':
                    positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'vn':
                    normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                    has_normals = True
                elif parts[0] == 'f':
                    face = []
                    for vert in parts[1:]:
                        vals = vert.split('/')
                        v_idx = int(vals[0]) - 1
                        n_idx = int(vals[2]) - 1 if len(vals) >= 3 and vals[2] else -1
                        face.append((v_idx, n_idx))
                    raw_faces.append(face)

        # Normalize positions to unit size centered at origin
        positions = self._normalize_positions(positions)

        if not has_normals:
            # Build simple index list, then compute smooth normals
            tri_indices = []
            for face in raw_faces:
                v_indices = [v for v, n in face]
                for i in range(1, len(v_indices) - 1):
                    tri_indices.extend([v_indices[0], v_indices[i], v_indices[i + 1]])
            vertices, tri_indices = self._compute_normals(positions, tri_indices)
        else:
            # Build interleaved vertex data with provided normals
            vertices = []
            tri_indices = []
            vertex_map = {}
            for face in raw_faces:
                face_verts = []
                for v_idx, n_idx in face:
                    key = (v_idx, n_idx)
                    if key not in vertex_map:
                        vertex_map[key] = len(vertices)
                        pos = positions[v_idx]
                        norm = normals[n_idx] if n_idx >= 0 else [0.0, 0.0, 0.0]
                        vertices.append(pos + norm)
                    face_verts.append(vertex_map[key])
                for i in range(1, len(face_verts) - 1):
                    tri_indices.extend([face_verts[0], face_verts[i], face_verts[i + 1]])

        vertex_data = np.array(vertices, dtype=np.float32)
        index_data = np.array(tri_indices, dtype=np.uint32)
        self.index_count = len(tri_indices)

        self._setup_buffers(vertex_data, index_data)
        print(f"Loaded '{self.name}': {len(vertices)} vertices, {self.index_count // 3} triangles")

    def _normalize_positions(self, positions):
        """Center and scale positions to fit in a unit sphere."""
        pos = np.array(positions, dtype=np.float32)
        center = (pos.max(axis=0) + pos.min(axis=0)) / 2.0
        pos -= center
        max_extent = np.abs(pos).max()
        if max_extent > 0:
            pos /= max_extent
        return pos.tolist()

    def _compute_normals(self, positions, indices):
        pos = np.array(positions, dtype=np.float32)
        norms = np.zeros_like(pos)
        for i in range(0, len(indices), 3):
            i0, i1, i2 = indices[i], indices[i+1], indices[i+2]
            v0, v1, v2 = pos[i0], pos[i1], pos[i2]
            n = np.cross(v1 - v0, v2 - v0)
            norms[i0] += n
            norms[i1] += n
            norms[i2] += n
        # Normalize
        lengths = np.linalg.norm(norms, axis=1, keepdims=True)
        lengths[lengths == 0] = 1.0
        norms /= lengths
        vertices = np.hstack([pos, norms]).tolist()
        return vertices, indices

    def _setup_buffers(self, vertex_data, index_data):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

        stride = 6 * 4  # 6 floats * 4 bytes
        # Position attribute (location 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Normal attribute (location 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    def draw(self):
        if self.vao is None:
            return
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def cleanup(self):
        if self.vao is not None:
            glDeleteVertexArrays(1, [self.vao])
            glDeleteBuffers(1, [self.vbo])
            glDeleteBuffers(1, [self.ebo])
