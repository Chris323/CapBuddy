from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect
from .aspect_ratio_drawer import AspectRatioDrawer
from .composition_drawer import RuleofThirdsDrawer, HorizonLineDrawer
from .crosshairs_drawer import CrosshairDrawer
from .dot_reticle_drawer import DotReticleDrawer


class OverlayDrawerManager:
    #white, red, green, blue
    COLORS = [
        QColor(255, 255, 255, 120),
        QColor(255, 0, 0, 120),
        QColor(0, 255, 0, 120),
        QColor(0, 0, 255, 120),
    ]

    def __init__(self):
        self.color_index = 0
        self.current_color = self.COLORS[self.color_index]

        # Drawer instances
        self.aspect_drawers = {
            "9:16": AspectRatioDrawer(self.current_color, 9, 16),
            "4:3": AspectRatioDrawer(self.current_color, 4, 3),
            "1:1": AspectRatioDrawer(self.current_color, 1, 1),
        }

        self.composition_drawers = {
            "Rule of Thirds": RuleofThirdsDrawer(self.current_color),
            "Horizon Line": HorizonLineDrawer(self.current_color),
        }

        self.crosshair = CrosshairDrawer(self.current_color)
        self.dot_reticle = DotReticleDrawer(self.current_color)

    def cycle_color(self):
        self.color_index = (self.color_index + 1) % len(self.COLORS)
        self.current_color = self.COLORS[self.color_index]

        # Update all drawers
        for drawer in list(self.aspect_drawers.values()) + list(self.composition_drawers.values()) + [self.crosshair, self.dot_reticle]:
            drawer.color = self.current_color

    def calculate_aspect_rect(self, full_rect, w_ratio, h_ratio):
        screen_w, screen_h = full_rect.width(), full_rect.height()
        target_w = screen_w
        target_h = target_w * h_ratio / w_ratio
        if target_h > screen_h:
            target_h = screen_h
            target_w = target_h * w_ratio / h_ratio
        x = full_rect.x() + (screen_w - target_w) / 2
        y = full_rect.y() + (screen_h - target_h) / 2
        return QRect(int(x), int(y), int(target_w), int(target_h))

    def get_draw_commands(self, config, full_rect):
        draw_cmds = []

        aspect_rect = full_rect

        if config.aspect_ratio and config.aspect_ratio != "None" and config.aspect_ratio in self.aspect_drawers:
            w, h = map(int, config.aspect_ratio.split(":"))
            aspect_rect = self.calculate_aspect_rect(full_rect, w, h)
            # Draw the aspect ratio rectangle on the full screen (or full_rect)
            draw_cmds.append((self.aspect_drawers[config.aspect_ratio], full_rect))
        else:
            # No aspect ratio selected → no rectangle drawn, aspect_rect stays full_rect
            aspect_rect = full_rect

        # Draw composition only if selected and aspect_rect is valid
        if config.composition and config.composition != "None" and config.composition in self.composition_drawers:
            draw_cmds.append((self.composition_drawers[config.composition], aspect_rect))

        if config.show_crosshair:
            draw_cmds.append((self.crosshair, full_rect))

        if config.show_reticle:
            draw_cmds.append((self.dot_reticle, full_rect))

        return draw_cmds