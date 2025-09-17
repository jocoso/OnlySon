import pygame
import sys


class Paper:
    def __init__(self, size_tuple, fps, caption):
        self.size_tuple = size_tuple
        self.fps = fps
        self.caption = caption
        self.user_input = ""
        self.buffer = ""
        self.newlines = 0

    def init(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode(self.size_tuple)
        self.clock = pygame.time.Clock()
        self.running = True

    def refresh(self):
        self.screen.fill((255, 255, 255))

        line_height = 40
        lines = self.buffer.split("\n")

        for i, line in enumerate(lines):
            y = 36 + i * line_height
            self.draw_text(line, 36, (0, 0, 0), 36, y)

        self.draw_text(self.user_input, 36, (0, 0, 0), 36, self.size_tuple[1] - 36)
        pygame.display.flip()

    def print(self, text):
        self.buffer = text

    def get_buffer(self):
        return self.buffer

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def read(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    char = event.unicode
                    if event.key == pygame.K_RETURN:
                        self.buffer += f"{self.user_input}\n"
                        self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.user_input) > 0:
                            self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += char

            self.refresh()
            self.clock.tick(self.fps)

        pygame.quit()
