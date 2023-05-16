import pygame

pygame.init()
pygame.font.init()


class Button(object):
    _font_btn = pygame.font.SysFont("Arial", 15, False)
    BTN_COLOR = "#769656"
    TEXT_COLOR = "#000000"
    BTN_PRESSED_COLOR = "#baca44"

    def __init__(self, text: str, size: pygame.Rect):
        self.text = self._font_btn.render(text, True, self.TEXT_COLOR)
        self._rect = size
        self.is_clicked = False

    def draw(self, surf):
        color = self.BTN_COLOR
        if self.is_clicked:
            color = self.BTN_PRESSED_COLOR
        pygame.draw.rect(surf, color, self._rect)
        surf.blit(self.text,
                  [self._rect.center[0] - self.text.get_width() / 2, self._rect.center[1] - self.text.get_height() / 2])

    def collide(self, pos):
        return self._rect.collidepoint(*pos)

    def change_text(self, text):
        self.text = self._font_btn.render(text, True, self.TEXT_COLOR)


class Menu(object):
    BG_COLOR = "#2d3436"

    _font_title = pygame.font.SysFont("Arial", 100, True)

    def __init__(self, WIN_SIZE: list):
        self.WIN_SIZE = WIN_SIZE  # WIDTH, HEIGHT
        self.screen = pygame.Surface(self.WIN_SIZE)
        self.buttons = []
        self._btn_width = round(self.WIN_SIZE[0] / 2)
        self._btn_height = round(self.WIN_SIZE[0] / 8)
        self._init_buttons()
        self._title = self._font_title.render("CHESS", True, "#f5f6fa")
        self.draw()
        self.offset = [10, 10]

    def _init_buttons(self):
        self.buttons.append(Button("Player vs Player", pygame.Rect(
            [self.WIN_SIZE[0] / 2 - self._btn_width / 2, 130, self._btn_width, self._btn_height])))
        self.buttons.append(Button("Player vs AI", pygame.Rect(
            [self.WIN_SIZE[0] / 2 - self._btn_width / 2, 130 + 1.5 * self._btn_height,
             self._btn_width, self._btn_height])))
        self.buttons.append(Button("Speech commands: OFF", pygame.Rect(
            [self.WIN_SIZE[0] / 2 - self._btn_width / 2, 130 + 3 * self._btn_height,
             self._btn_width, self._btn_height])))
        self.buttons.append(
            Button("PLAY", pygame.Rect([self.WIN_SIZE[0] / 2 - self._btn_width / 2, 130 + 4.5 * self._btn_height,
                                        self._btn_width, self._btn_height])))

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.screen.blit(self._title, [self.WIN_SIZE[0] / 2 - self._title.get_width() / 2, 20])
        for btn in self.buttons:
            btn.draw(self.screen)

    def update(self, events):
        play = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = [pos[0] - self.offset[0], pos[1] - self.offset[1]]
                for i, btn in enumerate(self.buttons):
                    if btn.collide(pos):
                        if i == 0:
                            btn.is_clicked = not btn.is_clicked
                            if btn.is_clicked:
                                self.buttons[i + 1].is_clicked = False
                        elif i == 1:
                            btn.is_clicked = not btn.is_clicked
                            if btn.is_clicked:
                                self.buttons[i - 1].is_clicked = False
                        elif i == 2:
                            btn.is_clicked = not btn.is_clicked
                            btn.change_text("Speech commands: " + ("ON" if btn.is_clicked else "OFF"))
                        elif i == 3:
                            btn.is_clicked = True
                            play = True
                        self.draw()
        return play

    def get_settings(self):
        return [self.buttons[i].is_clicked for i in range(3)]


if __name__ == "__main__":

    menu = Menu([480, 480])
    win = pygame.display.set_mode((480, 480))
    menu.draw()
    win.blit(menu.screen, [0, 0])
    pygame.display.flip()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        if menu.update(events):
            print(menu.get_settings())
            run = False
        win.blit(menu.screen, [0, 0])
        pygame.display.flip()
