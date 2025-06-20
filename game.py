import customtkinter as ctk
from random import randint
from time import sleep, time
from threading import Thread, Event

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

root = ctk.CTk()
root.geometry('600x600')
root.title('PLAY')

stop_event = Event()

def end_game():
    for btn in grids:
        btn.configure(command=None, fg_color='green', hover_color='green')
    start_button.configure(text="RESTART", command=start_game, fg_color='green',hover_color='darkgreen', font=("Arial", 20))
    score_board.configure(text_color='red')

def timer(sec):
    t1 = time()
    while not stop_event.is_set():
        sleep(0.1)
        t2 = time()
        elapsed = t2-t1
        # print(f"\r{(t2-t1):.1f} sec", end="")
        time_board.configure(text=f"{(elapsed):.1f} sec")
        if elapsed >=sec:
            time_board.configure(text=f"Time Over!")
            stop_event.set()
            end_game()
            break

def start_game():
    stop_event.clear()

    global curr, next, score, runTimer
    score = 0
    score_board.configure(text=f'Current Score : {score}', text_color='white')
    timerthread = Thread(target=timer, args=(int(time_limit_option.get()),), daemon=True)
    timerthread.start()
    # runTimer = True
    def whack():
        # print('whacked')
        global curr, next, score
        score += 1
        score_board.configure(text=f'Current Score : {score}')
        grids[curr].configure(fg_color='green', command = None, hover_color='green')
        grids[next].configure(fg_color='red',hover_color='yellow', command = whack)
        curr = next
        next = randint(0,35)
        while next == curr:
            next = randint(0,35)
    
    start_button.configure(command=None, fg_color = 'gray') # disable start button once begun
    grids[curr].configure(fg_color='red',hover_color='yellow', command=whack) 
    # score = 0



start_button = ctk.CTkButton(root, text='START', command=start_game, fg_color='green',hover_color='darkgreen', font=("Arial", 20))
start_button.pack(padx=10, pady=50)

time_limit_label = ctk.CTkLabel(root, text='Time Limit: ', font=("Arial", 20))
time_limit_label.pack(pady=5)
time_limit_option = ctk.CTkOptionMenu(root, values=['2','5','10','15','20'], font=("Arial", 20))
time_limit_option.pack(pady=5)
time_limit_option.set('15')

score_frame = ctk.CTkFrame(root)
score_frame.pack(pady=20)
score_board = ctk.CTkLabel(score_frame, text='Current Score : 0', font=('Arial', 20, 'bold'))
score_board.pack(pady=5, padx=15)
time_board = ctk.CTkLabel(score_frame, text='', font=("Arial", 20))
time_board.pack(pady=5, padx=15)

game_scene = ctk.CTkFrame(root, height=300, width = 300)
game_scene.pack(padx=10, pady=10, fill='x', side='bottom')

grids = [] # have 6*6 grids
for r in range(6):
    for c in range(6):
        btn = ctk.CTkButton(game_scene, fg_color='green', text='', hover_color='green')
        grids.append(btn)
        btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
for i in range(6):
    game_scene.grid_rowconfigure(i, weight=1)
    game_scene.grid_columnconfigure(i, weight=1)


# main
score  = 0
runTimer = True
curr = randint(0,35)
next = randint(0,35)
while next == curr:
    next = randint(0,35)


root.mainloop()