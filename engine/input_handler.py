import pygame


class InputHandler:
    def __init__(self):
        self.mouse_dragging = False
        self.last_mouse_pos = None
        self.quit_requested = False
        self.key_events = []
        self.scroll_delta = 0

    def process_events(self):
        self.key_events.clear()
        self.scroll_delta = 0
        dx, dy = 0, 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_dragging = True
                    self.last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    self.last_mouse_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_dragging and self.last_mouse_pos is not None:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.last_mouse_pos = event.pos

            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_delta = event.y

            elif event.type == pygame.KEYDOWN:
                self.key_events.append(event.key)

        return dx, dy
