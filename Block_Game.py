from tkinter import*
import time
import random

tk=Tk()
canvas=Canvas(tk,width=1000,height=1000)
canvas.pack()
tk.update()

class Moving_Object:
    def __init__(self,id,x,y,w,h,vx):
        self.id=id
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.vx=vx
    def redraw(self):
        id=self.id
        x=self.x
        y=self.y
        w=self.w
        h=self.h
        canvas.coords(id,x,y,x+w,y+h)
class Ball(Moving_Object):
    def __init__(self,id,x,y,w,h,vx,vy):
        super().__init__(id,x,y,w,h,vx)
        self.vy=vy
    def move(self):
        self.x=self.x+self.vx
        self.y=self.y+self.vy

class Paddle(Moving_Object):
    def __init__(self,id,x,y,w,h,vx=0):
        super().__init__(id,x,y,w,h,vx)
    def move_paddle(self):
        self.x=self.x+self.vx
    def left_paddle(self,event):
      self.vx=-7
    def right_paddle(self,event):
      self.vx=7
    def stop_paddle(self,event):
      self.vx=0
class Block:
    def __init__(self,id,x,y,w,h,color,count):
        self.id=id
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.color=color
        self.count=count
    def delete(self):
        canvas.delete(self.id)
class Box:
    def __init__(self,x,y,w,h,duration):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.duration=duration
        self.blocks=[]
    #ボール関係-----------------------------------------
    def create_ball(self,x,y,w,h):
        id=canvas.create_oval(x,y,x+w,y+h,fill="black")
        return Ball(id,x,y,w,h,4,5)
    def set_ball(self):
        ball=self.create_ball(400,300,20,20)
        self.ball=ball
    #パドル関係---------------------------------------------------
    def create_paddle(self,x,y,w,h):
        id=canvas.create_rectangle(x,y,x+w,y+h,fill="blue")
        return Paddle(id,x,y,w,h)
    def set_paddle(self):
        paddle=self.create_paddle(200,650,150,25)
        self.paddle=paddle
        canvas.bind_all("<KeyPress-Right>",paddle.right_paddle)
        canvas.bind_all("<KeyRelease-Right>",paddle.stop_paddle)
        canvas.bind_all("<KeyRelease-Left>",paddle.stop_paddle)
        canvas.bind_all("<KeyPress-Left>",paddle.left_paddle)
    #ブロック関係-----------------------------------------------
    def create_block(self,x,y,w,h):
        count=random.choice([1,1,1,1,1,2,2,3])
        if count==1:
            color="green"
        elif count==2:
            color="gray"
        elif count==3:
            color="black"
        id=canvas.create_rectangle(x,y,x+w,y+h,fill=color)
        return Block(id,x,y,w,h,color,count)
    def set_blocks(self,n):
        x=10
        y=10
        for z in range(n):
            if z==9:
                x=x-990
                y=y+80
            block=self.create_block(x,y,100,50)
            self.blocks.append(block)
            x=x+100+10
    #反射関係--------------------------------------------
    def check_wall(self,ball):
        if ball.y<=0:
            ball.vy=-ball.vy
        if ball.x<=0 or ball.x+ball.w>=1000:
            ball.vx=-ball.vx

    def check_block(self,block,ball):
        center_y=ball.y+ball.w/2
        center=ball.x+ball.w/2
        if block.x<center and center<block.x+block.w and ball.y<=block.y+block.h:
            ball.vy=-ball.vy
            block.count=block.count-1
        elif block.y<=center_y and center_y<=block.y+block.h and(block.x<=ball.x+ball.w and ball.x+ball.w<block.x+block.w):
            ball.vx=-ball.vx
            block.count=block.count-1
        elif (block.y<center_y and center_y<=block.y+block.h) and(block.x<ball.x and ball.x<=block.x+block.w):
            ball.vx=-ball.vx
            block.count=block.count-1
        if block.count==2:
            block.color="gray"
        elif block.count==1:
            block.color="green"
        canvas.itemconfigure(block.id,fill=block.color)
        if block.count==0:
            block.delete()
            self.blocks.remove(block)

    def check_paddle(self,paddle,ball):
        center=ball.x+ball.w/2
        if ball.vx>=0:
            if paddle.x<=center and center<=paddle.x+paddle.w/8 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
                ball.vx=-ball.vx
            elif paddle.x<=center and center<=paddle.x+paddle.w/2 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
            elif paddle.x<=center and center<=paddle.x+paddle.w*7/8 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
            elif paddle.x<=center and center<=paddle.x+paddle.w and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
                ball.vx=-ball.vx
        elif ball.vx<0:
            if paddle.x<=center and center<=paddle.x+paddle.w/8 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
                ball.vx=-ball.vx
            elif paddle.x<=center and center<=paddle.x+paddle.w/2 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
            elif paddle.x<=center and center<=paddle.x+paddle.w*7/8 and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
            elif paddle.x<=center and center<=paddle.x+paddle.w and paddle.y<=ball.y+ball.h:
                ball.vy=-ball.vy
                ball.vx=-ball.vx
        if(paddle.y<=ball.y+ball.h/2 and ball.y+ball.h/2<=paddle.y+paddle.h)and(paddle.x<=ball.x+ball.w and ball.x+ball.w<paddle.x+paddle.w):
            ball.vx=-ball.vx
        elif (paddle.y<=ball.y+ball.w/2 and ball.y+ball.w/2<=paddle.y+paddle.h)and (paddle.x<ball.x and ball.x<=paddle.x+paddle.w):
            ball.vx=-ball.vx
    #ウィンドウの削除(終了)
    def del_window(self,event):
        tk.withdraw()
    def animate(self):
        ball=self.ball
        paddle=self.paddle
        while True:
            paddle.move_paddle()
            ball.move()
            canvas.bind("<Button-1>",self.on)
            self.check_wall(ball)
            self.check_paddle(paddle,ball)
            for block in self.blocks:
                self.check_block(block,ball)
            ball.redraw()
            paddle.redraw()
            time.sleep(self.duration)
            tk.update()
            number=len(self.blocks)
            if number==0:
                canvas.create_text(500,300,text="GAME CLEAR",fill="blue",font=('Courier',80))
                canvas.create_text(500,400,text="spaceで終了",font=('Courier',50))
                canvas.bind_all("<KeyPress-space>",self.del_window)
                break
            if ball.y>=750:
                canvas.create_text(500,300,text="GAME OVER",fill="red",font=('Courier',80))
                canvas.create_text(500,400,text="spaceで終了",font=('Courier',50))
                canvas.bind_all("<KeyPress-space>",self.del_window)
                break
    def on(self,event):
        print("x:{},y:{}".format(event.x,event.y))
    def game_start(self):
        canvas.delete("all")
        btn.destroy()
        self.set_paddle()
        self.set_blocks(18)
        self.set_ball()
        self.animate()

box=Box(10,0,0,0,0.005)
btn=Button(tk,text="スタート",font=('Courier',40),command=box.game_start)
btn.pack()
btn.place(x=350,y=350)
tk.mainloop()
