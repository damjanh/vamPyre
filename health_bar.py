import pygame as pg


def draw_health_bar(surf, pos, size, border_c, back_c, health_c, progress):
    pg.draw.rect(surf, back_c, (*pos, *size))
    pg.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0]+1, pos[1]+1)
    inner_size = ((size[0]-2) * progress, size[1]-2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pg.draw.rect(surf, health_c, rect)
