import math
import pygame

s_w = pygame.s_w
s_h = pygame.s_h
r_w = pygame.r_w
r_h = pygame.r_h

class Quad:
    def __init__(self,points,color,texture):
        self.points = points
        self.color = color
        self.texture = texture
        self.calc_corners()
    def calc_corners(self):
        self.corners = []
        for p in self.points:
            tp = self.trans(p)
            self.corners.append(tp)
    def trans(self,p):
        x,y,z,u,v = p
        z = float((z*1.0/300.0)+1)
        if z==0:
            z=0.1
        d = s_w
        x = (d*x/float(r_w))/z
        x+=s_w//2
        d = s_h
        y = (d*y/float(r_w))/z
        y+=s_h//2
        return [x,y,z,u,v]
    def rot(self,rx=0,ry=0,rz=0,center=[0,0,0]):
        for q in self.points:
            x,y,z = q[:3]
            cx,cy,cz = center[:3]
            x=x-cx
            y=y-cy
            z=z-cz
            if rx:
                theta = rx*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                y = y*c-z*s
                z = y*s+z*c
                x = x
            if ry:
                theta = ry*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                z = z*c-x*s
                x = z*s+x*c
                y = y
            if rz:
                theta = rz*math.pi/180.0
                s,c = math.sin(theta),math.cos(theta)
                x = x*c-y*s
                y = x*s+y*c
                z = z
            q[0]=x+cx
            q[1]=y+cy
            q[2]=z+cz