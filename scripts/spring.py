import pygame
import pygame.gfxdraw
from scripts.util import draw_circle, get_curve, load_img
from scripts.consts import (
    BLUE,
    RED,
    WHITE,
    G_CONST,
    DELTA,
    BG_COLOR,
)


class Blob:
    def __init__(self, pos, radius, color=WHITE, isStatic=False, update_x=False):
        """
        What blob has :-
            pos - (x,y)
            radius - float
            color - (r,g,b)
            isStatic - Bool
            update_x - Bool
        """
        self.pos = list(pos)
        self.radius = radius
        self.color = color
        self.vel = [0, 0]
        self.acc = [0, 0]

        self.force = (0, 0)
        self.isStatic = isStatic
        self.x_axis = update_x

        self.circle = draw_circle(radius, color)

    def applyForce(self, force=(0, 0)):
        if self.isStatic:
            return

        self.force = (self.force[0] + force[0], self.force[1] + force[1])

    def copy(self):
        return Blob(self.pos, self.radius, self.color, self.isStatic)

    def applyGravity(self):
        self.applyForce((0, G_CONST * self.radius))

    def render(self, surf):
        surf.blit(self.circle, (self.pos[0] - self.radius, self.pos[1] - self.radius))

    def update(self):
        if self.isStatic:
            return

        if self.x_axis:
            # Acceleration
            self.acc[0] = (self.force[0] / self.radius) / 4
            # Velocity
            self.vel[0] += self.acc[0] / DELTA
            # Positions
            self.pos[0] += self.vel[0] / DELTA

        # Acceleration
        self.acc[1] = self.force[1] / self.radius
        # Velocity
        self.vel[1] += self.acc[1] / DELTA
        # Position
        self.pos[1] += self.vel[1] / DELTA

        # Reseting force
        self.force = [0, 0]


class Spring:

    """
    What Spring has :-
        blob1 - object
        blob2 - object
        Resting distance - r
        Spring Constant - ks
        Damping Factor - kd

    """

    def __init__(self, blob1, blob2, r=10, ks=0.1, kd=0.07):
        self.rest_len = r
        self.k_stiff = ks
        self.k_damp = kd

        self.blobs = (blob1, blob2)

    def update(self):
        pos_one = self.blobs[0].pos
        pos_two = self.blobs[1].pos

        # Getting distance
        dist_vect = (pos_two[0] - pos_one[0], pos_two[1] - pos_one[1])
        dist_mag = (dist_vect[0] ** 2 + dist_vect[1] ** 2) ** 0.5
        # Spring Force ------------------------------------------------------------|
        sucess = True
        force = (0, 0)

        # Values can reach infinity thats why using try-except
        try:
            dist_unit = (dist_vect[0] / dist_mag, dist_vect[1] / dist_mag)
            x = dist_mag - self.rest_len
            force = (dist_unit[0] * x * self.k_stiff, dist_unit[1] * x * self.k_stiff)
        except:
            # Calculating spring force
            sucess = False

        # Skipping to apply force for that frame if values are too high
        if sucess:
            self.blobs[0].applyForce(force)
            self.blobs[1].applyForce((-force[0], -force[1]))

        # Damping Force -----------------------------------------------------------|

        sucess = True
        force = (0, 0)
        vel_one = self.blobs[0].vel
        vel_two = self.blobs[1].vel
        try:
            dist_unit = (dist_vect[0] / dist_mag, dist_vect[1] / dist_mag)
            vel_diff = (vel_two[0] - vel_one[0], vel_two[1] - vel_one[1])

            fMag = (
                dist_unit[0] * vel_diff[0] + dist_unit[1] * vel_diff[1]
            ) * self.k_damp
            force = (dist_unit[0] * fMag, dist_unit[1] * fMag)
        except:
            sucess = False

        if sucess:
            self.blobs[0].applyForce(force)
            self.blobs[1].applyForce((-force[0], -force[1]))

        for blob in self.blobs:
            blob.update()

    def render(self, surf):
        pygame.draw.aaline(surf, WHITE, self.blobs[0].pos, self.blobs[1].pos)
        for blob in self.blobs:
            blob.render(surf)
        pass


class Lake:

    """
    What lake has :-
        start_pos - position of first particle/blob
        end_pos - position of last particle/blob
        spacing  - spacing between two particle/blob
        height - height of lake
        ks1 - Spring Constant for anchors
        ks2 - Spring Constant for connected spring
        kd1 - Damping Factor for anchors
        kd2 - Damping Factor for connected spring
    """

    def __init__(self, start_pos, end_pos, height, spacing, ks1, ks2, kd1, kd2):
        # self.texture = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))
        self.texture = load_img("textures/texture6.png")  # pygame.Surface((10, 10))
        self.texture.set_alpha(150)

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.spacing = spacing
        self.height = height

        # Calculating distance of lake
        distance = (
            (start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2
        ) ** 0.5

        # Counting total springs needed
        self.count = int(distance // spacing)

        self.springs = []

        self.blobs = []

        # Adding blobks and anchors
        for i in range(0, self.count + 1):
            blob = Blob((start_pos[0] + i * spacing, start_pos[1]), 5, RED)
            self.blobs.append(blob)
            anchor = Blob(
                (start_pos[0] + i * spacing, start_pos[1]),
                1,
                RED,
                True,
            )
            self.springs.append(Spring(blob, anchor, 0, ks1, kd1))

        # Adding springs
        for i in range(len(self.blobs) - 1):
            blob1 = self.blobs[i]
            blob2 = self.blobs[i + 1]
            self.springs.append(Spring(blob1, blob2, self.spacing, ks2, kd2))
        self.points = [start_pos]

        # Seperating points to easily access it
        for blob in self.blobs:
            self.points.append(blob.pos)
        self.points.append(end_pos)

    def update(self):
        for spring in self.springs:
            spring.update()

    def render(self, surf):
        # Getting render points using  bezier curve spline
        render_points = get_curve(self.points, 0.2)
        render_points.append((self.end_pos[0], self.end_pos[1] + self.height))
        render_points.append((self.start_pos[0], self.start_pos[1] + self.height))

        # Drawing textured lake
        pygame.gfxdraw.textured_polygon(
            surf, render_points, self.texture, 0, 512 // 2 + 50
        )

        # Drawing boundary for lake
        for i in range(0, len(render_points) - 3):
            p1 = render_points[i]
            p2 = render_points[i + 1]

            pygame.draw.aaline(surf, WHITE, p1, p2)

    def pull_blob(self):
        # To pull blob using mouse
        mouse_pos = pygame.mouse.get_pos()
        dist = 5000000
        my_blob = None
        for blob in self.blobs:
            if abs(blob.pos[0] - mouse_pos[0]) < dist:
                dist = abs(blob.pos[0] - mouse_pos[0])
                my_blob = blob
        my_blob.pos[1] = mouse_pos[1]
