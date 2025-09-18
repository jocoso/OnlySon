import pygame
import sys


class Pen:
    def __init__(
        self,
        caption,
        color=(0, 0, 0),
        bg_color=(255, 255, 255),
        indentation=36,
        size=(640, 480),
        fps=60,
    ):

        self.color = color
        self.bg_color = bg_color
        self.indentation = indentation
        self.paper = None
        self.size = size
        self.fps = fps
        self.caption = caption

    def init(self):
        self.paper = Paper(self.size, self.fps, self.caption)
        self.paper.init()

    def print_title(self, text):
        self.paper.print(text, self.indentation, self.color, x=self.indentation)

    def read(self):
        self.paper.read()


class Paper:
    def __init__(self, size, fps, caption):
        self.size = size
        self.fps = fps
        self.caption = caption
        self.user_input = ""
        self.buffer = []
        self.black = (0, 0, 0)

    def init(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.running = True

    def refresh(self):
        white = (255, 255, 255)
        self.screen.fill(white)
        text_size = 36
        line_height = 40

        for i, objs in enumerate(self.buffer):
            text_size = objs.get("size")
            x = objs.get("x", 0)
            y = text_size + i * line_height
            self.draw_text(
                objs.get("message"), text_size, objs.get("color", self.black), x, y
            )

        self.draw_text(
            self.user_input,
            text_size,
            self.black,
            text_size,
            self.size[1] - text_size,
        )
        pygame.display.flip()

    def print(self, text, text_size, text_color=None, x=0):
        self.buffer.append(
            {
                "message": text,
                "size": text_size,
                "color": text_color or self.black,
                "x": x,
            }
        )

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
                        self.buffer.append(
                            {
                                "message": self.user_input,
                                "size": 36,
                                "color": self.black,
                            }
                        )
                        self.user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.user_input) > 0:
                            self.user_input = self.user_input[:-1]
                    else:
                        self.user_input += char

            self.refresh()
            self.clock.tick(self.fps)

        pygame.quit()
