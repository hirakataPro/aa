import os
import sys
import math
import time
import pathlib


sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from engine.vectors import Vector3
from engine.matrices import Matrix4
from engine.mesh import Mesh
from engine.camera import Camera
from engine.pen import new_screen, line, label, track_keys, square

"""0は何もない、1は普通のマス、2はゴール、3は脆い床(垂直に乗ると壊れる)、4はスタート"""

stage = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,4,1,1,1,0,0,0],
    [0,0,0,3,1,1,1,0,0,0],
    [0,0,0,3,1,1,1,0,0,0],
    [0,0,0,3,1,1,2,0,0,0],
    [0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

stage2 = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,4,1,1,1,1,1,1],
    [1,1,1,3,1,1,1,1,1,1],
    [1,1,1,3,1,1,1,1,1,1],
    [1,1,1,3,1,1,2,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1]
]
stages = [stage, stage2]
WIDTH = 800
HEIGHT = 800

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)
RED = (255, 0, 0)

cam = Camera(Vector3(-3.3, 14.1, -11.6), 0.6, 0.6)
p_mesh = Mesh.cube(size=1,type=1)
ANGLE = 63.434948822922
HYPOT = 2.2360679774998
x_angle = 0
z_angle = 0
pivot_x = 0
pivot_y = 0
pivot_z = 0

end = 0
stage_count = 1
screen, pen = new_screen("bloxorz", WIDTH, HEIGHT)

def new_stage():
    pass

"""ステージ描画"""
def stage_draw():
    for i in range(len(stages[stage_count])):
        for j in range(len(stages[stage_count][i])):
            if stages[stage_count][i][j] == 1:
                x = j * 2
                z = i * 2
                pos = Vector3(x, 0, z)
                mesh = Mesh.cube()
                mesh.transform = Matrix4.translation(pos.x, pos.y, pos.z)
                mesh.draw(pen, cam, WHITE)

        for j in range(len(stages[stage_count][i])):
            if stages[stage_count][i][j] == 2:
                x = j * 2
                z = i * 2
                pos = Vector3(x, 0, z)
                mesh = Mesh.cube()
                mesh.transform = Matrix4.translation(pos.x, pos.y, pos.z)
                mesh.draw(pen, cam, RED)
            
            if stages[stage_count][i][j] == 3:
                x = j * 2
                z = i * 2
                pos = Vector3(x, 0, z)
                mesh = Mesh.cube()
                mesh.transform = Matrix4.translation(pos.x, pos.y, pos.z)
                mesh.draw(pen, cam, ORANGE)

            if stages[stage_count][i][j] == 4:
                x = j * 2
                z = i * 2
                pos = Vector3(x, 0, z)
                mesh = Mesh.cube()
                mesh.transform = Matrix4.translation(pos.x, pos.y, pos.z)
                mesh.draw(pen, cam, BLUE)
                


class Player:
    """
    stateは、立っているとき"0", 縦向きのとき"1", 横向きの時"2"
    
    倒れているときの座標は、縦向きの時は下側が原点、横向きの時は左側が原点となる
    """
    
    
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        
        
    def check(self, x, y, state):
        global stage_count, end
        
        x = x
        y = y
        state = state
        x1, y1, x2, y2 = 0, 0, 0, 0
        if state == 0:
            x1, y1 = x, y
            x2, y2 = x, y
        if state == 1:
            x1, y1 = x, y
            x2, y2 = x, y + 1
        if state == 2:
            x1, y1= x, y
            x2, y2 = x + 1, y
        
        if x1 >= len(stages[stage_count][0]) or y1 >= len(stages[stage_count]) or x2 >= len(stages[stage_count][0]) or y2 >= len(stages[stage_count]) or x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
            return False
        else :
            return (stages[stage_count][y1][x1], stages[stage_count][y2][x2])


    def animation(self, direction):
        global p_mesh, x_angle, z_angle, pivot_x, pivot_y, pivot_z
        d = direction
        rot_speed = 3
        if x_angle == 180 or x_angle == -180: x_angle = 0
        if z_angle == 180 or z_angle == -180: z_angle = 0
        if d == 0:
            if self.state == 0: 
                pivot_x = self.x * 2
                pivot_y = 0
                pivot_z = self.y * 2  + 1
            elif self.state == 1:
                pivot_x = self.x * 2
                pivot_y = 0
                pivot_z = self.y * 2 + 3
            elif self.state == 2:
                pivot_x = self.x * 2 + 1
                pivot_y = 0
                pivot_z = self.y * 2  + 1
                

            for i in range(int(90/rot_speed)):
                    x_angle += rot_speed
                    if self.state == 0: 
                        p_mesh.transform = Matrix4.translation(pivot_x, 
                                                               math.sin(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                               pivot_z - math.cos(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                    elif self.state == 1:
                        p_mesh.transform = Matrix4.translation(pivot_x, 
                                                               math.sin(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT,
                                                               pivot_z - math.cos(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                    elif self.state == 2:
                        p_mesh.transform = Matrix4.translation(pivot_x, 
                                                               math.sin(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                               pivot_z - math.cos(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2)) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                    pen.clear()
                    p_mesh.draw(pen, cam, WHITE)
                    stage_draw()
                    screen.update()
                    time.sleep(0.005)
                    
        elif d == 1:
            if self.state == 0: 
                pivot_x = self.x * 2 + 1
                pivot_y = 0
                pivot_z = self.y * 2
            elif self.state == 1:
                pivot_x = self.x * 2 + 1
                pivot_y = 0
                pivot_z = self.y * 2 + 1
            elif self.state == 2:
                pivot_x = self.x * 2 + 3
                pivot_y = 0
                pivot_z = self.y * 2
                

            for i in range(int(90/rot_speed)):
                    z_angle -= rot_speed
                    if self.state == 0: 
                        p_mesh.transform = Matrix4.translation(pivot_x - math.cos(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                               pivot_y + math.sin(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                                pivot_z) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                    elif self.state == 1:
                        p_mesh.transform = Matrix4.translation(pivot_x - math.cos(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                               pivot_y + math.sin(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                                pivot_z) @ Matrix4.rotation_z(math.radians(z_angle)) @ Matrix4.rotation_x(math.radians(x_angle))
                    elif self.state == 2:
                        p_mesh.transform = Matrix4.translation(pivot_x - math.cos(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT, 
                                                               math.sin(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT,
                                                                pivot_z) @ Matrix4.rotation_z(math.radians(z_angle)) @ Matrix4.rotation_x(math.radians(x_angle))
                    pen.clear()
                    p_mesh.draw(pen, cam, WHITE)
                    stage_draw()
                    screen.update()
                    time.sleep(0.005)
        elif d == 2:
                    if self.state == 0: 
                        pivot_x = self.x * 2
                        pivot_y = 0
                        pivot_z = self.y * 2  - 1
                    elif self.state == 1:
                        pivot_x = self.x * 2
                        pivot_y = 0
                        pivot_z = self.y * 2 - 1
                    elif self.state == 2:
                        pivot_x = self.x * 2 + 1
                        pivot_y = 0
                        pivot_z = self.y * 2  - 1
                        
        
                    for i in range(int(90/rot_speed)):
                            x_angle -= rot_speed
                            if self.state == 0: 
                                p_mesh.transform = Matrix4.translation(pivot_x, 
                                                                    math.sin(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                                    pivot_z + math.cos(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                            elif self.state == 1:
                                p_mesh.transform = Matrix4.translation(pivot_x, 
                                                                    math.sin(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT,
                                                                    pivot_z + math.cos(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                            elif self.state == 2:
                                p_mesh.transform = Matrix4.translation(pivot_x, 
                                                                    math.sin(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                                    pivot_z + math.cos(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2)) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                            pen.clear()
                            p_mesh.draw(pen, cam, WHITE)
                            stage_draw()
                            screen.update()
                            time.sleep(0.005)
                            
        elif d == 3:
            if self.state == 0: 
                pivot_x = self.x * 2 - 1
                pivot_y = 0
                pivot_z = self.y * 2
            elif self.state == 1:
                pivot_x = self.x * 2 - 1
                pivot_y = 0
                pivot_z = self.y * 2 + 1
            elif self.state == 2:
                pivot_x = self.x * 2 - 1
                pivot_y = 0
                pivot_z = self.y * 2
                

            for i in range(int(90/rot_speed)):
                    z_angle += rot_speed
                    if self.state == 0: 
                        p_mesh.transform = Matrix4.translation(pivot_x + math.cos(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                            pivot_y + math.sin(math.radians(ANGLE + (i + 1) * rot_speed)) * HYPOT, 
                                                                pivot_z) @ Matrix4.rotation_x(math.radians(x_angle)) @ Matrix4.rotation_z(math.radians(z_angle))
                    elif self.state == 1:
                        p_mesh.transform = Matrix4.translation(pivot_x + math.cos(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                            pivot_y + math.sin(math.radians(45 + (i + 1) * rot_speed)) * math.sqrt(2), 
                                                                pivot_z) @ Matrix4.rotation_z(math.radians(z_angle)) @ Matrix4.rotation_x(math.radians(x_angle))
                    elif self.state == 2:
                        p_mesh.transform = Matrix4.translation(pivot_x + math.cos(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT, 
                                                            math.sin(math.radians((90 - ANGLE) + (i + 1) * rot_speed)) * HYPOT,
                                                                pivot_z) @ Matrix4.rotation_z(math.radians(z_angle)) @ Matrix4.rotation_x(math.radians(x_angle))
                    pen.clear()
                    p_mesh.draw(pen, cam, WHITE)
                    stage_draw()
                    screen.update()
                    time.sleep(0.005)

    
    def move(self, held, end):
        if end == 0:
            if "w" in held:
                if self.state == 0 and self.check(self.x, self.y + 1, self.state + 1) != False and 0 not in self.check(self.x, self.y + 1, self.state + 1):
                    self.animation(0)
                    self.y += 1
                    self.state = 1
                    
                elif self.state == 1 and self.check(self.x, self.y + 2, self.state - 1) != False and 0 not in self.check(self.x, self.y + 2, self.state - 1):
                    self.animation(0)
                    self.y += 2
                    self.state = 0
                    
                elif self.state == 2 and self.check(self.x, self.y + 1, self.state) != False and 0 not in self.check(self.x, self.y + 1, self.state):
                    self.animation(0)
                    self.y += 1
                    self.state = 2
                    

            if "s" in held:
                if self.state == 0 and self.check(self.x, self.y - 2, self.state + 1) != False and 0 not in self.check(self.x, self.y - 2, self.state + 1):
                    self.animation(2)
                    self.y -= 2
                    self.state = 1
                elif self.state == 1 and self.check(self.x, self.y - 1, self.state - 1) != False and 0 not in self.check(self.x, self.y - 1, self.state - 1):
                    self.animation(2)
                    self.y -= 1
                    self.state = 0
                elif self.state == 2 and self.check(self.x, self.y - 1, self.state) != False and 0 not in self.check(self.x, self.y - 1, self.state):
                    self.animation(2)
                    self.y -= 1

            if "d" in held:
                if self.state == 0 and self.check(self.x + 1, self.y, self.state + 2) != False and 0 not in self.check(self.x + 1, self.y, self.state + 2):
                    self.animation(1)
                    self.x += 1
                    self.state = 2
                elif self.state == 1 and self.check(self.x + 1, self.y, self.state) != False and 0 not in self.check(self.x + 1, self.y, self.state):
                    self.animation(1)
                    self.x += 1
                    self.state = 1
                elif self.state == 2 and self.check(self.x + 2, self.y, self.state - 2) != False and 0 not in self.check(self.x + 2, self.y, self.state - 2):
                    self.animation(1)
                    self.x += 2
                    self.state = 0

            if "a" in held:
                if self.state == 0 and self.check(self.x - 2, self.y, self.state + 2) != False and 0 not in self.check(self.x - 2, self.y, self.state + 2):
                    self.animation(3)
                    self.x -= 2
                    self.state = 2
                elif self.state == 1 and self.check(self.x - 1, self.y, self.state) != False and 0 not in self.check(self.x - 1, self.y, self.state) :
                    self.animation(3)
                    self.x -= 1
                elif self.state == 2 and self.check(self.x - 1, self.y, self.state - 2) != False and 0 not in self.check(self.x - 1, self.y, self.state - 2):
                    self.animation(3)
                    self.x -= 1
                    self.state = 0

            if "8" in held:
                cam.position = cam.position + cam.forward() * 0.1
            if "5" in held:
                cam.position = cam.position - cam.forward() * 0.1
            if "6" in held:
                cam.position = cam.position + cam.right() * 0.1
            if "4" in held:
                cam.position = cam.position - cam.right() * 0.1
            if "Left" in held:
                cam.yaw -= 0.03
            if "Right" in held:
                cam.yaw += 0.03
            if "Up" in held:
                cam.pitch -= 0.03
            if "Down" in held:
                cam.pitch += 0.03
            if "space" in held:
                cam.position = cam.position + cam.up() * 0.1
            if "Shift_L" in held:
                cam.position = cam.position - cam.up() * 0.1
                
    def draw(self):
        if self.state == 0:
            x = self.x * 2
            y = 2
            z = self.y * 2
            p_mesh.transform = Matrix4.translation(x, y, z)
            

for y in range(len(stages[stage_count])):
    for x in range(len(stages[stage_count][0])):
        if stages[stage_count][y][x] == 4:
            start_x = x
            start_y = y
            
player = Player(start_x, start_y, 0)

player.state += 0


held = track_keys(screen, ["w", "s", "a", "d", "Left", "Right", "Up", "Down", "4", "5", "6", "8", "Shift_L", "space"])

while True:
    pen.clear()
    stage_draw()
    player.draw()
    p_mesh.draw(pen, cam, WHITE)

    """移動"""
    start = player.move(held, end)
    
    if player.state == 0 and player.check(player.x, player.y, player.state) == (2,2):
        label(pen, -30, 0, "CLEAR!")
        end = 1
        stage_count = 1
        
        end = 0
    if player.state == 0 and player.check(player.x, player.y, player.state) == (3,3):
        stages[stage_count][player.y][player.x] = 0
    """アニメーション"""
    print(x_angle, z_angle, pivot_x, pivot_y, pivot_z)
            
    label(pen, -350, 300, (round(cam.position.x, 1), round(cam.position.y, 1), round(cam.position.z, 1), round(cam.yaw, 1), round(cam.pitch, 1)), size=20,)


    screen.update()
    
    
    """次回は、d == 1のときの移動をやる"""