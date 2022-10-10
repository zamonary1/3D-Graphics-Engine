import glm
import pygame as pg
import pygame

FOV = 50  # deg
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.04
DEAD_ZONE = 0.15 #only for joystick

pygame.init()
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()

print(pygame.joystick.get_count())

   

class Camera:
    

    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        if pygame.joystick.get_count() > 1:
            if my_joystick.get_axis(2) > DEAD_ZONE or my_joystick.get_axis(2) < (0 - DEAD_ZONE):
                self.yaw += my_joystick.get_axis(2) * SENSITIVITY * 15
            if my_joystick.get_axis(3) > DEAD_ZONE or my_joystick.get_axis(3) < (0 - DEAD_ZONE):       
                self.pitch -= my_joystick.get_axis(3) * SENSITIVITY * 15
                self.pitch = max(-89, min(89, self.pitch))
        else:
            rel_x, rel_y = pg.mouse.get_rel()
            self.yaw += rel_x * SENSITIVITY
            self.pitch -= rel_y * SENSITIVITY
            self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        if pygame.joystick.get_count() > 1:
            # pygame.joystick.Joystick(0).init()
            ljx=my_joystick.get_axis(0)
            ljy=my_joystick.get_axis(1)
            lt = (my_joystick.get_axis(4) + 1) / 2
            rt = (my_joystick.get_axis(5) + 1) / 2
            # rjx=ljoy.get_axis(2)
            # rjy=ljoy.get_axis(3)
            clock=pygame.time.Clock()
            velocity = SPEED * self.app.delta_time
            # keys = pg.key.get_pressed()
            if ljy > DEAD_ZONE:
                self.position -= self.forward * velocity * ljy
            if ljy < (0 - DEAD_ZONE):
                self.position += self.forward * velocity * (ljy - (ljy + ljy))
            if ljx < (0 - DEAD_ZONE):
                self.position -= self.right * velocity * (ljx - (ljx + ljx))
            if ljx > DEAD_ZONE:
                self.position += self.right * velocity * ljx
            if lt > DEAD_ZONE: #left trigger
                self.position += self.up * velocity * lt
            if rt > DEAD_ZONE: #right trigger
                self.position -= self.up * velocity * rt
            pygame.time.Clock().tick(1000)
        else:
            velocity = SPEED * self.app.delta_time
            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.position += self.forward * velocity
            if keys[pg.K_s]:
                self.position -= self.forward * velocity
            if keys[pg.K_a]:
                self.position -= self.right * velocity
            if keys[pg.K_d]:
                self.position += self.right * velocity
            if keys[pg.K_q]:
                self.position += self.up * velocity
            if keys[pg.K_e]:
                self.position -= self.up * velocity
        

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)




















