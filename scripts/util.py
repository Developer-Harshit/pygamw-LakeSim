import pygame


def load_img(rpath):
    path = rpath

    img = pygame.image.load(path).convert()  # convert method makes it easier to render

    img.set_colorkey((0, 0, 0))
    return img


def draw_circle(radius, color=(255, 255, 255)):
    surf = pygame.Surface((radius * 2, radius * 2))

    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def bezier(p0, p1, p2, t):
    x = ((1 - t) ** 2 * p0[0]) + (2 * (1 - t) * t * p1[0]) + (t * t * p2[0])
    y = ((1 - t) ** 2 * p0[1]) + (2 * (1 - t) * t * p1[1]) + (t * t * p2[1])
    return (x, y)


# (1-t)**2 p0[0] + 2*(1-t) *t*p1[0] + t**2*p2[0]
def get_curve(points, inc=0.1):
    pt_len = len(points)

    extra_points = [points[pt_len - 1]] * 2
    control_points = points + extra_points

    curve = []
    for i in range(0, pt_len, 2):
        p0 = control_points[i]
        p1 = control_points[i + 1]
        p2 = control_points[i + 2]
        t = 0
        while t < 1:
            new_point = bezier(p0, p1, p2, t)
            curve.append(new_point)
            if (
                new_point[0] == control_points[-1][0]
                and new_point[1] == control_points[-1][1]
            ):
                break
            t += inc

    return curve
