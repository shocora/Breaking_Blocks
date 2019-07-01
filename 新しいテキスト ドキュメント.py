
from tkinter import *
import time
import random

tk=Tk()
canvas=Canvas(tk,width=1000,height=800)
canvas.pack()
tk.update()
#-------------------------------
#パドル系
# パドルの生成
def new_paddle(id,x,y,w,h,c="blue"):
    return{"id":id,"x":x,"y":y,"w":w,"h":h,"vx":0,"c":c}

# パドルの描画・登録
def make_paddle(x,y,w=120,h=20,c="blue"):
    id=canvas.create_rectangle(x,y,x+w,y+h,fill=c,outline=c)
    return new_paddle(id,x,y,w,h,c)

# パドルの移動( 左右)
def move_paddle(pad):
    pad["x"]=pad["x"]+pad["vx"]

#パドルの再描画
def redraw_paddle(pad):
    id=pad["id"]
    x=pad["x"]
    y=pad["y"]
    w=pad["w"]
    h=pad["h"]
    canvas.coords(id,x,y,x+w,y+h)

#パドルの色を変える
def change_paddle_color(pad,c="red"):
    id=pad["id"]
    canvas.itemconfigure(id,fill=c)
    canvas.itemconfigure(id,outline=c)
    redraw_paddle(pad)

#---------------------------
#ボール系
def new_ball(id,x,y,vx,vy,d,c):#ボールの生成
    return{"id":id,"x":x,"y":y,"vx":vx,"vy":vy,"d":d,"c":c}
def make_ball(x,y,vx,vy,d=10,c="black"):#ボールの描画.登録
    id=canvas.create_oval(x,y,x+d,y+d,fill=c,outline=c)
    return new_ball(id,x,y,vx,vy,d,c)
def move_ball(ball):#ボールの移動（上下）
    ball["y"]=ball["y"]+ball["vy"]
    ball["x"]=ball["x"]+ball["vx"]
def redraw_ball(ball):#ボールの再描画
    id=ball["id"]
    x=ball["x"]
    y=ball["y"]
    d=ball["d"]
    canvas.coords(id,x,y,x+d,y+d)
#--------------------------------
#ブロック系
def new_block(id,x,y,w,h,c):#ブロックの生成
    return{"id":id,"x":x,"y":y,"w":w,"h":h,"c":c}
def make_block(x,y,w,h,c="green"):#ブロックの描画。登録
    id=canvas.create_rectangle(x,y,x+w,y+h,fill=c,outline=c)
    return new_block(id,x,y,w,h,c)
def make_blocks(n_rows,x0,y0,w,h,pad=5):#複数のブロックを生成する
    blocks=[]
    for y in range(3):
        y0=y0-h-10
        for x in range(n_rows):
            blocks.append(make_block(x0,y0,w,h))
            x0=x0+w+pad
        x0=10
    return blocks
def delete_block(block):#ブロックを消す
    id=block["id"]
    canvas.delete(id)

#-----------------------------------
#壁系
def make_walls(ox,oy,width,height):#壁の生成
    canvas.create_rectangle(ox,oy,ox+width,oy+height)



#------------------------------------
#初期状態の設定(ball)
duration=0.01#描画間隔
ball_x0=500#ボールの初期位置（ｘ）
ball_y0=300#ボールの初期位置（ｙ）
ball_d=30#ボールの大きさ
ball_vy0=3#ボールの速度(y)
ball_vx0=5#ボールの速度(x)


#初期状態の設定(paddle)
paddle_x0=500#パドルの初期位置（ｘ）
paddle_y0=500#パドルの初期位置（ｙ）
pad=make_paddle(paddle_x0,paddle_y0)
pad_vx=5#パドルの速度

#初期状態の設定（ブロック）
num_blocks=8
block_x=10#ブロックの位置（ｘ）
block_y=150#ブロックの位置（ｙ）
block_w=120#ブロックの幅
block_h=20#ブロックの高さ


colors=["blue","red","green","yellow","brown","gray"]
#ball_vy=5

make_walls=(0,0,1000,800)

ball=make_ball(ball_x0,ball_y0,ball_vy0,ball_vx0)
blocks=make_blocks(num_blocks,block_x,block_y,block_w,block_h)

#------------------------------------
# SPACE の入力待ち
games = {" start ": False }#spacekeyを待つ
def game_start ( event ):
    games [" start "] = True

canvas.bind_all ('<KeyPress -space >', game_start ) # SPACE が押された    

    
id_text = canvas.create_text ( 400 , 200 , text =" Press 'SPACE ' to start ",
                                            font = ('FixedSys ', 16) )


while games [" start "] == False : # ひたすらSPACE を待つ
    tk.update_idletasks ()
    tk.update ()
    time.sleep ( duration )

canvas.delete ( id_text )
tk. update ()
#----------------------------------

def left_paddle(event):
    pad["vx"]=-pad_vx

def right_paddle(event):
    pad["vx"]=pad_vx

def stop_paddle(event):
    pad["vx"]=0


canvas.bind_all('<KeyPress -Left >',left_paddle)
canvas.bind_all('<KeyPress -Right >',right_paddle)
canvas.bind_all('<KeyRelease -Left >',stop_paddle)
canvas.bind_all('<KeyRelease -Right >',stop_paddle)


#----------------------------------
while True:
    move_paddle(pad)#パドルの移動
    move_ball(ball)#ボールの移動
    if ball ["y"] + ball ["d"] + ball ["vy"] >= 600:  # 下に逸らした
        canvas.create_text ( 400 , 200 , text =" Game Over !",font = ('FixedSys ', 16) )
        break
    #ボールがパドルの上に届き、ボールの横幅がパドルの幅に収まっている    
    if (ball["x"]+ball["d"]>=pad["x"] and
        pad["y"]<=ball["y"]<=pad["y"]+pad["h"]):
        change_paddle_color(pad,random.choice(colors))
        ball["vy"]=-ball["vy"]
    #ブロックが存在し、ボールのｙ位置が届き、ｙ位置も範囲内
    for block in blocks:
        if (((ball["x"]<=block["x"]+block["w"]) and (ball["x"]+ball["d"]>=block["x"]))
            and ((ball["y"]==block["y"]+block["h"]) or (ball["y"]+ball["d"]==block["y"]))):
            ball["vy"]=-ball["vy"]#ボールを跳ね返す
            delete_block(block)#ブロックを消す
            blocks.remove(block)#ブロックのリストから削除
            break
    for block in blocks:
        if (((ball["y"]<=block["y"]+block["h"]) and (ball["y"]+ball["d"]>=block["y"]))
            and ((ball["x"]==block["x"]+block["w"]) or (ball["x"]+ball["d"]==block["x"]))):
            ball["vx"]=-ball["vx"]#ボールを跳ね返す
            delete_block(block)#ブロックを消す
            blocks.remove(block)#ブロックのリストから削除
            break
    if ball["x"]+ball["vx"]<=0:#ボールが左端に到着
        ball["vx"]=-ball["vx"]
    if ball["x"]+ball["vx"]>=1000:#ボールが右端に到着
        ball["vx"]=-ball["vx"]
    if ball["y"]+ball["vy"]<=0:#ボールが上端に到着
        ball["vy"]=-ball["vy"]
    if blocks == [] :
        break # blocks リストが空になったら終了
    redraw_paddle(pad)
    redraw_ball(ball)
    tk.update_idletasks()
    tk.update()
    time.sleep(duration)
tk.mainloop()
