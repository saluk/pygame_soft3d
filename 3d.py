import pygame
import pygame.gfxdraw
import psyco

psyco.full()

s_w,s_h = 200,150
r_w,r_h = 400,300
pygame.screen = s = pygame.display.set_mode([r_w,r_h],pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.surf = pygame.Surface([s_w,s_h])
pygame.arr = pygame.surfarray.pixels2d(pygame.surf)

tex = pygame.image.load("bm.bmp").convert()
texarr = pygame.surfarray.pixels2d(tex)

def trans(q,x=0,y=0,z=0):
    for p in q[:4]:
        p[0]+=x
        p[1]+=y
        p[2]+=z
def push(q,z=0):
    q[0][2]+=z
    q[3][2]+=z

quad = [[0,0,0,0,0],
            [140,0,0,1,0],
            [140,140,0,1,1],
            [0,140,0,0,1],
            [255,255,255]]
quad2 = [[0,0,140,0,0],
            [140,0,140,1,0],
            [140,140,140,1,1],
            [0,140,140,0,1],
            [255,0,0]]
quad3 = [[0,0,0,0,0],
            [0,0,140,1,0],
            [0,140,140,1,1],
            [0,140,0,1,1],
            [0,255,0]]
quads = [quad,quad2,quad3]

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
        #~ r = abs(((color>>16) & 0xff))
        #~ g = abs(((color>>8) & 0xff))
        #~ b = abs(((color) & 0xff))
        #~ r/=float(z*2)
        #~ g/=float(z*2)
        #~ b/=float(z*2)
        #~ if r<0: r=0
        #~ if r>255: r=255
        #~ if g<0: g=0
        #~ if g>255: g=255
        #~ if b<0: b=0
        #~ if b>255: b=255
        #~ color = int((hex(r)[2:-1]+hex(g)[2:-1]+hex(b)[2:-1]),16)
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
        
def draw_tquad(q):
    points = []
    for p in q[:4]:
        x,y,z = p
        z = float(z+0.1)
        x = x/z*120+200
        y = y/z*120+150
        x,y = int(x),int(y)
        points.append([x,y])
    pygame.gfxdraw.textured_polygon(s, points, tex, 0,0)

def draw_quad(q):
    color = q[4]
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
    w = float(max([abs(x) for x in [xw1,zw1,xw2,zw2]]))/4
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

running = 1
while running:
    dt = clock.tick(60)
    pygame.display.set_caption("%s"%clock.get_fps())
    pygame.points = 0
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running = 0
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