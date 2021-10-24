from tkinter import *
from math import *
import time

width = 800
height = 800
w = 800
h = height - 200
len1 = 150
len2 = 150
ball_radius = 10
l1_fixed_coords = [w/2,h/4]

canvas = None
l1 = 0
l2 = 0
b1 = 0
b2 = 0
a1 = 0
a2 = 0
s1, s2 = 0, 0
b = 0
button2 = 0
button3 = 0
label = 0

#coords for the equilibrium position
ball1_coords = []
ball2_coords = []
tags = []

app = Tk()
v = StringVar()
t = 0.00

def initUI():
    global canvas, l1, l2, b1, b2, ball1_coords, ball2_coords, s1, s2, b,label
    app.title('Double Pendulum Simulator')
    s1 = Scale(app, from_=-180, to=180,orient=HORIZONTAL,command=slider1)
    s2 = Scale(app, from_=-180,to=180,orient=HORIZONTAL,command=slider2)
    s1.set(0)
    s2.set(0)
    s1.pack()
    s2.pack()
    b =  Button(text='Start',width = 10,height= 2,command=start)
    b.pack(side=BOTTOM,pady=15)
    canvas = Canvas(width=w,height=h)
    l1 = canvas.create_line(l1_fixed_coords[0],l1_fixed_coords[1],l1_fixed_coords[0],l1_fixed_coords[1]+len1,width = 3)
    ball1_coords = canvas.coords(l1)[2:]
    l2 = canvas.create_line(ball1_coords[0],ball1_coords[1],ball1_coords[0],ball1_coords[1]+len2,width = 3)
    ball2_coords = canvas.coords(l2)[2:]
    b1 = create_circle(ball1_coords[0],ball1_coords[1],ball_radius,canvas)
    b2 = create_circle(ball2_coords[0],ball2_coords[1],ball_radius,canvas)
    canvas.pack(fill=BOTH, expand=1)
    v.set('0.00s')
    Label(app,textvariable=v,font=("Arial", 16)).pack(side=TOP,padx=50)

def create_circle(x, y, r, canvasName):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1,fill='red',outline = '')

def ang_to_coords(x,y,length,a):
    x1 = x + (length)*sin((a/180)*pi)
    y1 = y - length + length*cos((a/180)*pi)
    return (x1,y1)


def slider1(a1):
    global ball2_coords
    xdiff = canvas.coords(l2)[2] - canvas.coords(l1)[2]
    ydiff = canvas.coords(l2)[3] - canvas.coords(l1)[3]
    x,y = ang_to_coords(ball1_coords[0],ball1_coords[1],len1,int(a1))
    update_ball(b1,x,y)
    update_line(l1,x,y)
    update_ball(b2,x+xdiff,y+ydiff)
    update_line(l2,x+xdiff,y+ydiff)
    ball2_coords = [canvas.coords(l1)[2],canvas.coords(l1)[3]+len2]
    return

def slider2(a2):
    x,y = ang_to_coords(ball2_coords[0],ball2_coords[1],len2,int(a2))
    update_ball(b2,x,y)
    update_line(l2,x,y)

def update_ball(ball,x,y):
    canvas.coords(ball,x-ball_radius,y-ball_radius,x+ball_radius,y+ball_radius)

def update_line(line,x,y):
    if line == l1:
        canvas.coords(line,l1_fixed_coords[0],l1_fixed_coords[1],x,y)
    else:
        canvas.coords(line,canvas.coords(l1)[2],canvas.coords(l1)[3],x,y)

def move(ball,ang):
    global ang1, ang2
    ang = degrees(ang)
    if ball == b1:
        ang = ang + ang1
        x, y = ang_to_coords(ball1_coords[0],ball1_coords[1],len1,ang)
        update_ball(b1,x,y)
        update_line(l1,x,y)
        ang1 = ang
        r = 1
        return
    else:
        ang = ang + ang2
        x, y = ang_to_coords(canvas.coords(l1)[2],canvas.coords(l1)[3]+len2,len2,ang)
        update_ball(b2,x,y)
        update_line(l2,x,y)
        ang2 = ang
        r = 1
        return
        
ang1, ang2 = 0, 0
g = 9.81
m1, m2 = 2, 2
a1,a2 = 0, 0
v1, v2 = 0, 0

stopp = False

def update():
    global a1, a2, v1, v2, ang1, ang2, v, t
    if stopp == True:
        return
    angg1 = radians(ang1)
    angg2 = radians(ang2)
    lenn1 = len1/1
    lenn2 = len2/1
    a1 = ((-g*(2*m1+m2)*sin(angg1))-(m2*g*sin(angg1-2*angg2)) - (2*sin(angg1-angg2)*m2) * (v2*v2*len2+v1*v1*lenn1*cos(angg1-angg2)) ) / (lenn1 *(2*m1+m2-m2*cos(2*angg1-2*angg2)))
    a2 = ((2*sin(angg1-angg2))*((v1*v1*lenn1*(m1+m2))+(g*(m1+m2)*cos(angg1))+(v2*v2*lenn2*m2*cos(angg1-angg2))))/(lenn2*(2*m1+m2-m2*cos(2*angg1-2*angg2)))
    a1 = a1/100
    a2 = a2/100
    move(b1,v1)
    move(b2,v2)
    v1 += a1
    v2 += a2
    v.set(str(time.time() - t)[:4] + 's')
    canvas.after(10,update)

def start():
    global a1, a2, v1, v2, ang1, ang2, button2, b, stopp, v, t
    b.destroy()
    button2 = Button(text='Stop',width = 10,height= 2,command=stop)
    button2.pack(side=BOTTOM,pady=15)
    ang1 = int(s1.get())
    ang2 = int(s2.get())
    t = time.time()
    if ang1 <0:
        ang1 += 360
    if ang2 <0:
        ang2 += 360
    canvas.after(10,update)
    return

def stop():
    global stopp, button3, button2
    stopp = True
    button2.destroy()
    button3 =Button(text='Reset',width = 10,height= 2,command=reset)
    button3.pack(side=BOTTOM,pady=15)
    return

def reset():
    global stopp, ang1, ang2, v1, v2, a1, a2, b, v, t
    stopp = False
    s1.set(0)
    s2.set(0)
    update_ball(b1,ball1_coords[0],ball1_coords[1])
    update_line(l1,ball1_coords[0],ball1_coords[1])
    update_ball(b2,ball1_coords[0],ball1_coords[1]+len2)
    update_ball(b2,ball1_coords[0],ball1_coords[1]+len2)
    button3.destroy()
    for item in tags:
        canvas.delete(item)
    b = Button(text='Start',width = 10,height= 2,command=start)
    b.pack(side=BOTTOM,pady=15)
    ang1, ang2, v1, v2, a1, a2 = 0,0,0,0,0,0
    v.set('0.00s')
    t = 0.00
    return
    
    
initUI()
app.title('Double Pendulum Simulator')
app.geometry(str(width)+'x'+str(height))
app.mainloop()

