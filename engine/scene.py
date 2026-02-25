import os
from engine.mesh import Mesh
from engine.camera import Camera
from engine.light import SunLight, SpotLightManager
from engine.transform import identity, normal_matrix, perspective


class Scene:
    LIGHT_MODE_SUN = 0
    LIGHT_MODE_SPOTLIGHTS = 1

    def __init__(self, models_dir):
        self.camera = Camera(target=(0, 0, 0), distance=3.0)
        self.meshes = []
        self.mesh_names = []
        self.active_mesh_index = 0
        self.light_mode = self.LIGHT_MODE_SUN
        self.sun = SunLight()
        self.spotlights = SpotLightManager()
        self.model_matrix = identity()
        self.object_color = [0.7, 0.7, 0.75]
        self.ambient_strength = 0.15
        self.models_dir = models_dir

    def load_models(self):
        obj_files = sorted([f for f in os.listdir(self.models_dir) if f.endswith('.obj')])
        for fname in obj_files:
            mesh = Mesh(name=fname.replace('.obj', ''))
            mesh.load_obj(os.path.join(self.models_dir, fname))
            self.meshes.append(mesh)
            self.mesh_names.append(mesh.name)
        if not self.meshes:
            raise RuntimeError(f"No .obj files found in {self.models_dir}")
        print(f"Models loaded: {', '.join(self.mesh_names)}")

    def switch_model(self):
        if len(self.meshes) <= 1:
            return
        self.active_mesh_index = (self.active_mesh_index + 1) % len(self.meshes)
        print(f"Switched to model: {self.mesh_names[self.active_mesh_index]}")

    def toggle_light_mode(self, mode):
        self.light_mode = mode
        mode_name = "Sun" if mode == self.LIGHT_MODE_SUN else "Spotlights"
        print(f"Light mode: {mode_name}")

    def update(self, dt):
        if self.light_mode == self.LIGHT_MODE_SUN:
            self.sun.update(dt)

    def get_active_lights(self):
        if self.light_mode == self.LIGHT_MODE_SUN:
            return [self.sun.get_light_data()]
        else:
            data = self.spotlights.get_all_light_data()
            if not data:
                # Default spotlight if none added yet
                return [{'type': 1, 'position': [0, 5, 0], 'direction': [0, -1, 0],
                         'color': [1, 1, 1], 'intensity': 1.5, 'cutoff': 0.0, 'outerCutoff': 0.0}]
            return data

    def render(self, shader, width, height):
        shader.use()

        # Projection
        aspect = width / height if height > 0 else 1.0
        proj = perspective(45.0, aspect, 0.1, 100.0)
        view = self.camera.get_view_matrix()
        model = self.model_matrix
        norm_mat = normal_matrix(model)

        shader.set_mat4("projection", proj)
        shader.set_mat4("view", view)
        shader.set_mat4("model", model)
        shader.set_mat3("normalMatrix", norm_mat)
        shader.set_vec3("viewPos", self.camera.position.tolist())
        shader.set_vec3("objectColor", self.object_color)
        shader.set_float("ambientStrength", self.ambient_strength)

        # Set lights
        lights = self.get_active_lights()
        shader.set_int("numLights", len(lights))
        for i, light in enumerate(lights):
            prefix = f"lights[{i}]"
            shader.set_int(f"{prefix}.type", light['type'])
            shader.set_vec3(f"{prefix}.position", light['position'])
            shader.set_vec3(f"{prefix}.direction", light['direction'])
            shader.set_vec3(f"{prefix}.color", light['color'])
            shader.set_float(f"{prefix}.intensity", light['intensity'])
            shader.set_float(f"{prefix}.cutoff", light['cutoff'])
            shader.set_float(f"{prefix}.outerCutoff", light['outerCutoff'])

        # Draw active mesh
        if self.meshes:
            self.meshes[self.active_mesh_index].draw()

    def cleanup(self):
        for mesh in self.meshes:
            mesh.cleanup()
