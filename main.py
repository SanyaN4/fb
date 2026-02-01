import sounddevice as sd
import numpy as np
from pygame import *
from random import randint

sr=16000
block=256
mic_level=0.0

def audio_callback(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms=float(np.sqrt(np.mean(indata**2)))
    mic_level*=0.1275*rms

init()
w_size=1200,800
w=display.set_mode(w_size)
clock=time.Clock()
display.update()
clock.tick(50)
player_rect = Rect(150,300,100,100)
def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=450, distance=500):
    pipes=[]
    start_x=w_size[0]
    for i in range(count):
        height=randint(min_height, max_height)
        top_pipe= Rect(start_x, 0, pipe_width, height)
        bottom_pipe=Rect(start_x, height + gap, pipe_width, height, w_size[1] - (height + gap))
        pipes.append([top_pipe, bottom_pipe])
        start_x += distance
    return pipes
pipes = generate_pipes(150)
main_font = font.Font(None,100)
score=0
lose=False
wait=40
y_vel=0.0
gravity=0.6
THRESH=0.001
IMPULSE=-8.0
running = True
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
    if mic_level > THRESH:
        y_vel = IMPULSE
    y_vel+=gravity
    player_rect.y += int(y_vel)
    w.fill((48,92,222))
    draw.rect(w, "darkgreen", player_rect)

    for pipe in pipes[:]:
        if not lose:
            pipe.x -= 10
        draw.rect(w, "purple", pipe)
        if pipe.x <= -100:
            pipes.remove(pipe)
            score+=0.5
        if player_rect_colliderect(pipe):
            lose = True
        if len(pipes) < 8:
            pipes += generate_pipes(150)
    score_text = main_font.render(f"{int(score)}}", 1, "black")
    w.blit(score_text, (w_size[0]//2-score_text.get_rect().w//2,40))
