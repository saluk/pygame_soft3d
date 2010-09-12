import pygame
import pygame.gfxdraw
import psyco

psyco.full()

s_w,s_h = 100,75
r_w,r_h = 400,300
pygame.screen = s = pygame.display.set_mode([r_w,r_h],pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.surf = pygame.Surface([s_w,s_h])
pygame.arr = pygame.surfarray.pixels3d(pygame.surf)

tex = pygame.image.load("bm.bmp").convert()
texarr = pygame.surfarray.pixels3d(tex)

def trans(q,x=0,y=0,z=0):
    for p in q[:4]:
        p[0]+=x
        p[1]+=y
        p[2]+=z
def push(q,z=0):
    q[0][2]+=z
    q[3][2]+=z

class Quad:
    def __init__(self,points,color):
        self.points = points
        self.color = color
        self.calc_corners()
    def calc_corners(self):
        self.corners = []
        for p in self.points:
            tp = self.trans(p)
            self.corners.append(tp)
    def trans(self,p):
        x,y,z,u,v = p
        z = float((z*1.0/300)+1)
        x = (x*s_w/float(r_w))/z+s_w//2
        y = (y*s_w/float(r_w))/z+s_h//2
        return [x,y,z,u,v]
    def __getitem__(self,k):
        return self.points[k]
quad = Quad([[0,0,0,0,0],
            [140,0,0,1,0],
            [140,140,0,1,1],
            [0,140,0,0,1]],
            [255,255,255])
quad2 = Quad([[0,0,140,0,0],
            [140,0,140,1,0],
            [140,140,140,1,1],
            [0,140,140,0,1]],
            [255,0,0])
quad3 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,1,1]],
            [0,255,0])
quad4 = Quad([[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,1,1]],
            [0,255,0])
trans(quad4,x=140)
quads = [quad,quad2,quad3,quad4]

odepth = [1000 for i in range(s_w*s_h)]
pygame.depth = odepth[:]

def draw_point(x,y,z,u,v,color=None):
    pygame.points += 1
    #z = 0 to 1
    #want z = 0 to 400
    #z/z`=140/20
    #z = 140/20*z`
    z = float((z*1.0/300)+1)
    if z<=0:
        return
    #x = 0 to s_w
    #x = 0 to r_w
    x = (x*s_w/float(r_w))/z+s_w//2
    y = (y*s_w/float(r_w))/z+s_h//2
    x,y = int(x),int(y)
    if x<0 or x>=s_w or y<0 or y>=s_h:
        return
    if pygame.depth[y*s_w+x]<z:
        return
    pygame.depth[y*s_w+x] = z
    if not color:
        color = texarr[int(u*(tex.get_width()-1)),int(v*(tex.get_height()-1))]
        #~ color = [int(color[0]/z),int(color[1]/z),int(color[2]/z)]
    pygame.arr[x,y] = color

def draw_line(s,e,color):
    line = [s,e]
    x,y,z,u,v = line[0]
    steps = 100
    xs = (line[1][0]-line[0][0])/float(steps)
    ys = (line[1][1]-line[0][1])/float(steps)
    zs = (line[1][2]-line[0][2])/float(steps)
    us = (line[1][3]-line[0][3])/float(steps)
    vs = (line[1][4]-line[0][4])/float(steps)
    for i in range(steps):
        draw_point(x,y,z,u,v)
        x+=xs
        y+=ys
        z+=zs
        u+=us
        v+=vs
        
def draw_point2(x,y,z,u,v):
    pygame.points += 1
    if x<0 or x>=s_w:
        return
    if y<0 or y>=s_h:
        return
    if pygame.depth[y*s_w+x]<z:
        return
    pygame.depth[y*s_w+x] = z
    #~ if u>1: u=1
    #~ if u<0: u=0
    #~ if v>1: v=1
    #~ if v<0: v=0
    color = texarr[int(u*(tex.get_width()-1)),int(v*(tex.get_height()-1))]
    #color = [int(color[0]/z),int(color[1]/z),int(color[2]/z)]
    pygame.arr[x,y] = color

def draw_line2(x1,y1,z1,u1,v1,x2,y2,z2,u2,v2):
    x,y,z,u,v = x1,y1,z1,u1,v1
    w = abs(x2-x1)
    if not w:
        return
    dx = (x2-x1)/w
    dy = (y2-y1)/w
    dz = (z2-z1)/w
    du = (u2-u1)/w
    dv = (v2-v1)/w
    while 1:
        draw_point2(int(x),int(y),z,u,v)
        x+=dx
        y+=dy
        z+=dz
        u+=du
        v+=dv
        if x2>x1 and x>x2:
            break
        if x2<x1 and x<x2:
            break
        
def draw_quad2(q):
    """Draws a quad sample in screen space"""
    q.calc_corners()
    ul = q.corners[0]
    ur = q.corners[1]
    br = q.corners[2]
    bl = q.corners[3]
    #left side and right side moving from top to bottom
    left = ul
    right = ur
    dy = 1
    w = abs(bl[1]-ul[1])
    dxl = (bl[0]-ul[0])/w
    dxr = (ur[0]-br[0])/w
    dzl = (bl[2]-ul[2])/w
    dzr = (ur[2]-br[2])/w
    dul = (bl[3]-ul[3])/w
    dur = (ur[3]-br[3])/w
    dvl = (bl[4]-ul[4])/w
    dvr = (ur[4]-br[4])/w
    while left[1]<bl[1]:
        draw_line2(*(left+right))
        left[0]+=dxl
        left[1]+=dy
        left[2]+=dzl
        left[3]+=dul
        left[4]+=dvl
        right[0]+=dxr
        right[1]+=dy
        right[2]+=dzr
        right[3]+=dur
        right[4]+=dvr
    

def draw_quad1(q):
    """Draws a quad by sampling in polygon space across and down"""
    color = q.color
    #march start from q[0] to q[1]
    #march end from q[3] to q[2]
    x1 = q[0][0]
    y1 = q[0][1]
    z1 = q[0][2]
    u1 = q[0][3]
    v1 = q[0][4]
    x2 = q[3][0]
    y2 = q[3][1]
    z2 = q[3][2]
    u2 = q[3][3]
    v2 = q[3][4]
    xw1 = q[1][0]-q[0][0]
    yw1 = q[1][1]-q[0][1]
    zw1 = q[1][2]-q[0][2]
    uw1 = q[1][3]-q[0][3]
    vw1 = q[1][4]-q[0][4]
    xw2 = q[2][0]-q[3][0]
    yw2 = q[2][1]-q[3][1]
    zw2 = q[2][2]-q[3][2]
    uw2 = q[2][3]-q[3][3]
    vw2 = q[2][4]-q[3][4]
    w = float(max([abs(x) for x in [xw1,zw1,xw2,zw2]]))
    #sample based on average distance
    az = ((q[0][2]+q[1][2]+q[2][2]+q[3][2])/140.0+2)
    if az<=0:
        return
    w = 1/az*100
    d1 = [x/w for x in [xw1,yw1,zw1,uw1,vw1]]
    d2 = [x/w for x in [xw2,yw2,zw2,uw2,vw2]]
    p1 = [x1,y1,z1,u1,v1]
    p2 = [x2,y2,z2,u2,v2]
    while w>0:
        draw_line(p1,p2,color)
        w-=1
        for i in range(5):
            p1[i]+=d1[i]
            p2[i]+=d2[i]

draw_quad = draw_quad2

running = 1
while running:
    dt = clock.tick(60)
    pygame.display.set_caption("%s"%clock.get_fps())
    pygame.points = 0
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running = 0
        if e.type==pygame.KEYDOWN and e.key==pygame.K_1:
            draw_quad = draw_quad1
        if e.type==pygame.KEYDOWN and e.key==pygame.K_2:
            draw_quad = draw_quad2
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
    pygame.depth = odepth[:]
    pygame.surf.fill([0,0,0])
    [draw_quad(q) for q in quads]
    print pygame.points
    surf = pygame.transform.scale(pygame.surf,[r_w,r_h])
    pygame.screen.blit(surf,[0,0])
    pygame.display.flip()