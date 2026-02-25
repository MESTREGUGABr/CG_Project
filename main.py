import os
import sys
import pygame
from OpenGL.GL import *

from engine.shader import Shader
from engine.scene import Scene
from engine.grid import Grid
from engine.input_handler import InputHandler
from engine.transform import perspective


# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "CG Project - 3D Statue Viewer"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHADERS_DIR = os.path.join(BASE_DIR, "shaders")
MODELS_DIR = os.path.join(BASE_DIR, "models")


def init_pygame():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE
    )
    pygame.display.set_caption(WINDOW_TITLE)
    return screen


def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.08, 0.08, 0.10, 1.0)


def print_controls():
    print("=" * 50)
    print("  CG Project - 3D Statue Viewer")
    print("=" * 50)
    print("  Controls:")
    print("  Mouse drag (LMB) - Rotate camera")
    print("  Mouse scroll     - Zoom in/out")
    print("  Tab              - Switch model")
    print("  1                - Sun mode (orbital light)")
    print("  2                - Spotlight mode")
    print("  +/-              - Sun speed up/down")
    print("  Space            - Add spotlight")
    print("  C                - Clear spotlights")
    print("  ESC              - Quit")
    print("=" * 50)


def main():
    screen = init_pygame()
    init_opengl()
    print_controls()

    # Load shaders
    model_shader = Shader(
        os.path.join(SHADERS_DIR, "vertex.glsl"),
        os.path.join(SHADERS_DIR, "fragment.glsl"),
    )
    grid_shader = Shader(
        os.path.join(SHADERS_DIR, "grid_vertex.glsl"),
        os.path.join(SHADERS_DIR, "grid_fragment.glsl"),
    )

    # Load scene
    scene = Scene(MODELS_DIR)
    scene.load_models()

    # Create grid floor
    grid = Grid(size=8.0, y=-1.0)

    input_handler = InputHandler()
    clock = pygame.time.Clock()

    width, height = WINDOW_WIDTH, WINDOW_HEIGHT

    while not input_handler.quit_requested:
        dt = clock.tick(60) / 1000.0

        # Process input
        dx, dy = input_handler.process_events()

        # Camera controls
        if dx != 0 or dy != 0:
            scene.camera.rotate(dx, -dy)
        if input_handler.scroll_delta != 0:
            scene.camera.zoom(input_handler.scroll_delta)

        # Key events
        for key in input_handler.key_events:
            if key == pygame.K_ESCAPE:
                input_handler.quit_requested = True
            elif key == pygame.K_TAB:
                scene.switch_model()
            elif key == pygame.K_1:
                scene.toggle_light_mode(Scene.LIGHT_MODE_SUN)
            elif key == pygame.K_2:
                scene.toggle_light_mode(Scene.LIGHT_MODE_SPOTLIGHTS)
            elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                scene.sun.change_speed(10)
                print(f"Sun speed: {scene.sun.speed:.0f} deg/s")
            elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                scene.sun.change_speed(-10)
                print(f"Sun speed: {scene.sun.speed:.0f} deg/s")
            elif key == pygame.K_SPACE:
                scene.spotlights.add_spotlight(
                    scene.camera.position,
                    scene.camera.target,
                )
            elif key == pygame.K_c:
                scene.spotlights.clear()

        # Handle window resize
        current_size = pygame.display.get_surface().get_size()
        if current_size != (width, height):
            width, height = current_size
            glViewport(0, 0, width, height)

        # Update
        scene.update(dt)

        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw 3D model
        scene.render(model_shader, width, height)

        # Draw grid floor
        aspect = width / height if height > 0 else 1.0
        proj = perspective(45.0, aspect, 0.1, 100.0)
        view = scene.camera.get_view_matrix()
        grid_shader.use()
        grid_shader.set_mat4("projection", proj)
        grid_shader.set_mat4("view", view)
        grid.draw()

        # Update window title with info
        mode_name = "Sun" if scene.light_mode == Scene.LIGHT_MODE_SUN else "Spotlights"
        model_name = scene.mesh_names[scene.active_mesh_index] if scene.mesh_names else "None"
        fps = clock.get_fps()
        pygame.display.set_caption(
            f"{WINDOW_TITLE} | Model: {model_name} | Light: {mode_name} | FPS: {fps:.0f}"
        )

        pygame.display.flip()

    # Cleanup
    scene.cleanup()
    grid.cleanup()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
