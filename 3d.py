import pygame
import pygame.gfxdraw
import psyco
import numpy
import math
import random


psyco.full()

s_w,s_h = 150,100
r_w,r_h = 400,300
pygame.s_w = s_w
pygame.s_h = s_h
pygame.r_w = r_w
pygame.r_h = r_h
pygame.screen = s = pygame.display.set_mode([r_w,r_h],pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.surf = pygame.Surface([s_w,s_h])
pygame.arr = pygame.surfarray.pixels2d(pygame.surf)

from models import *

def load_tex(img):
    tex = pygame.image.load(img)
    
    texarr = []
    mem = []
    alpha = 255
    for z in range(50):
        blank = tex.convert()
        blank.fill([0,0,0])
        tex.set_alpha(alpha)
        blank.blit(tex,[0,0])
        alpha = int(0.96*alpha)
        arr = pygame.surfarray.pixels2d(blank)
        texarr.append(arr)
        mem.append(blank)
    tw = tex.get_width()-1
    th = tex.get_height()-1
    return texarr,mem,tw,th
    
texarr,mem,tw,th = load_tex("bm.bmp")

def trans(q,x=0,y=0,z=0):
    for p in q.points[:4]:
        p[0]+=x
        p[1]+=y
        p[2]+=z
def push(q,z=0):
    q.points[0][2]+=z
    q.points[3][2]+=z
def uvscroll(q,u=0,v=0):
    for p in q.points[:4]:
        p[3]+=u
        p[4]+=v

quad = Quad([[0,0,0,0,0],
            [140,0,0,1,0],
            [140,140,0,1,1],
            [0,140,0,0,1]],
            [255,255,255],
            texarr)
quad2 = Quad([[0,0,140,0,0],
            [140,0,140,1,0],
            [140,140,140,1,1],
            [0,140,140,0,1]],
            [255,0,0],
            texarr)
quad3 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,0,1]],
            [0,255,0],
            texarr)
quad4 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,0,1]],
            [0,255,0],
            texarr)
trans(quad4,x=140)
quads = [quad,quad2,quad3,quad4]
odepth = [1000 for i in range(s_w*s_h)]
pygame.depth = odepth[:]

def draw_point(x,y,z,u,v,texture):
    #pygame.points += 1
    if x<0 or x>=s_w:
        return
    if y<0 or y>=s_h:
        return
    if z<=0:
        return
    if pygame.depth[y*s_w+x]<z:
        return
    pygame.depth[y*s_w+x] = z
    pygame.arr[x,y] = texture[int(z*10)][int(u%1*tw),int(v%1*th)]
        
def draw_tri(a,b,c,texture):
    """draws triangle with horizontal lines"""
    #Sort points vertically
    a,b,c = sorted([a,b,c],key=lambda t: t[1])
    #upside down triangle with flat top
    if a[1]==b[1]:
        draw_tri_point_down(a,b,c,texture)
        return
    #triangle with flat bottom
    if b[1]==c[1]:
        draw_tri_point_up(a,b,c,texture)
        return
    #triangle should be split
    else:
        draw_tri_split(a,b,c,texture)
        
def draw_tri_split(a,b,c,texture):
    """Split a rotated triangle into an upward and downward pointing one"""
    d = [0,b[1],0,0,0]
    if c[0]==a[0]:
        d[0] = c[0]
    else:
        m = (c[1]-a[1])/(c[0]-a[0])
        i=a[1]-m*a[0]
        d[0] = (d[1]-i)/m
    if c[2]==a[2]:
        d[2] = c[2]
    else:
        m = (c[1]-a[1])/(c[2]-a[2])
        i=a[1]-m*a[2]
        d[2] = (d[1]-i)/m
    if c[3]==a[3]:
        d[3] = c[3]
    else:
        m = (c[1]-a[1])/(c[3]-a[3])
        i=a[1]-m*a[3]
        d[3] = (d[1]-i)/m
    if c[4]==a[4]:
        d[4] = c[4]
    else:
        m = (c[1]-a[1])/(c[4]-a[4])
        i=a[1]-m*a[4]
        d[4] = (d[1]-i)/m
    draw_tri_point_up(a,b,d,texture)
    draw_tri_point_down(b,d,c,texture)
    
def draw_line(x1,y1,z1,u1,v1,x2,y2,z2,u2,v2,texture):
    """horizontal"""
    x,y,z,u,v = x1,y1,z1,u1,v1
    w = abs(x2-x1)
    if not w:
        return
    if y<0 or y>=s_h:
        return
    dx = 1
    dy = 0
    dz = (z2-z1)/w
    du = (u2-u1)/w
    dv = (v2-v1)/w
    while x<x2:
        if x>=s_w:
            return
        if x>=0:
            draw_point(int(x),int(y),z,u,v,texture)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv

def draw_tri_point_up(a,b,c,texture):
    """flat bottom"""
    b,c = sorted([b,c],key=lambda t: t[0])
    x,y,z,u,v = a
    ex,ey,ez,eu,ev = a
    if c[0]<b[0]:
        b,c = c,b
    ydist = float(b[1]-y)
    dx1 = (b[0]-x)/ydist
    dx2 = (c[0]-ex)/ydist
    dy1 = 1
    dy2 = 1
    dz1 = (b[2]-z)/ydist
    dz2 = (c[2]-ez)/ydist
    du1 = (b[3]-u)/ydist
    du2 = (c[3]-eu)/ydist
    dv1 = (b[4]-v)/ydist
    dv2 = (c[4]-ev)/ydist
    while y<=b[1]:
        draw_line(x,y,z,u,v,ex,ey,ez,eu,ev,texture)
        x+=dx1
        y+=dy1
        z+=dz1
        u+=du1
        v+=dv1
        ex+=dx2
        ey+=dy2
        ez+=dz2
        eu+=du2
        ev+=dv2

def draw_tri_point_down(a,b,c,texture):
    """flat top"""
    if b[0]<a[0]:
        b,a = a,b
    x,y,z,u,v = a
    ex,ey,ez,eu,ev = b
    ydist = float(c[1]-y)
    dx1 = (c[0]-x)/ydist
    dx2 = (c[0]-ex)/ydist
    dy1 = 1
    dy2 = 1
    dz1 = (c[2]-z)/ydist
    dz2 = (c[2]-ez)/ydist
    du1 = (c[3]-u)/ydist
    du2 = (c[3]-eu)/ydist
    dv1 = (c[4]-v)/ydist
    dv2 = (c[4]-ev)/ydist
    while y<=c[1]:
        draw_line(x,y,z,u,v,ex,ey,ez,eu,ev,texture)
        x+=dx1
        y+=dy1
        z+=dz1
        u+=du1
        v+=dv1
        ex+=dx2
        ey+=dy2
        ez+=dz2
        eu+=du2
        ev+=dv2
        
def draw_quad(q):
    """Draws a quad sample in screen space"""
    q.calc_corners()
    ul = q.corners[0]
    ur = q.corners[1]
    br = q.corners[2]
    bl = q.corners[3]
    draw_tri(ul,ur,br,q.texture)
    draw_tri(ul,br,bl,q.texture)

def main():
    next_update = 1
    running = 1
    while running:
        dt = clock.tick(200)
        pygame.display.set_caption("%s"%clock.get_fps())
        pygame.points = 0
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running = 0
            #~ if e.type==pygame.KEYDOWN and e.key==pygame.K_1:
                #~ draw_line3 = draw_line3_inline
            #~ if e.type==pygame.KEYDOWN and e.key==pygame.K_2:
                #~ draw_line3 = draw_line3_func
        keys = pygame.key.get_pressed()
        spd = 5
        if keys[pygame.K_a]:
            [trans(quad,z=-spd) for quad in quads]
        if keys[pygame.K_z]:
            [trans(quad,z=spd) for quad in quads]
        if keys[pygame.K_LEFT]:
            [trans(quad,x=-spd) for quad in quads]
        if keys[pygame.K_RIGHT]:
            [trans(quad,x=spd) for quad in quads]
        if keys[pygame.K_UP]:
            [trans(quad,y=-spd) for quad in quads]
        if keys[pygame.K_DOWN]:
            [trans(quad,y=spd) for quad in quads]
        if keys[pygame.K_r]:
            [q.rot(ry=1,center=quads[0].points[0]) for q in quads]
        if keys[pygame.K_t]:
            [q.rot(rx=1,center=quads[0].points[0]) for q in quads]
        if keys[pygame.K_y]:
            [q.rot(rz=1,center=quads[0].points[0]) for q in quads]
        if keys[pygame.K_f]:
            [q.rot(-1,center=quads[0].points[0]) for q in quads]
        uvscroll(quads[0],u=0,v=.01)
        if next_update<0:
            #[quad.calc_corners() for quad in quads]
            next_update = 0#100
            pygame.depth = odepth[:]
            pygame.surf.fill([0,0,0])
            [draw_quad(q) for q in quads]
            surf = pygame.transform.scale(pygame.surf,[r_w,r_h])
            pygame.screen.blit(surf,[0,0])
        next_update -= dt
        pygame.display.flip()

#~ import cProfile as profile
#~ profile.run("main()")
main()