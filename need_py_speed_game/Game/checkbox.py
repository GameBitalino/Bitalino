import pygame as pg

pg.init()


class Checkbox:
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        # checkbox object
        self.size_obj = 50
        self.checkbox_obj = pg.Rect(self.x, self.y, self.size_obj, self.size_obj)
        self.checkbox_outline = self.checkbox_obj.copy()
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False
        self.changed = False
        self.mouse_position_x = 0
        self.mouse_position_y = 0

    def _draw_button_text(self):
        self.font = pg.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 12 / 2 - w / 2 + self.to[0], self.y + 12 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pg.draw.circle(self.surface, self.cc, (self.x + 25, self.y + 25), 10)

        elif self.unchecked:
            pg.draw.rect(self.surface, self.color, self.checkbox_obj)
            pg.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = event_object.pos
        # self.x, self.y, 12, 12
        px, py, w, h = self.checkbox_obj  # getting check box dimensions
        if px < x < px + w and px < x < px + w:
            self.active = True
        else:
            self.active = False

    def _mouse_up(self):
        if self.click and self.mouse_position_x > self.x \
                and (self.mouse_position_x < (self.x + self.size_obj)) and self.mouse_position_y > self.y \
                and (self.mouse_position_y < (self.y + self.size_obj)):
            if not self.checked:
                self.checked = True
            elif self.checked:
                self.checked = False
                self.unchecked = True

            if self.click is True:
                if self.checked:
                    self.checked = True
                if self.unchecked:
                    self.unchecked = True
                self.active = False
            self.changed = True
        else:
            self.changed = False

    def update_checkbox(self, event_object):
        if event_object.type == pg.MOUSEBUTTONDOWN:
            self.click = True
            self.mouse_position_x, self.mouse_position_y = pg.mouse.get_pos()
            # self._mouse_down()
        if event_object.type == pg.MOUSEBUTTONUP:
            self._mouse_up()
        if event_object.type == pg.mouse.get_pressed():
            self._update(event_object)
        return self.changed

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False
