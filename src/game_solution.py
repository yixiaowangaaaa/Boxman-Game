import tkinter as tk
import copy
from tkinter.messagebox import showinfo
import datetime
from tkinter import ttk
import pickle
"""
The Boxman game is implemented using the Tkinter library in Python. 
The player interacts with the game through keyboard inputs to move the Boxman character and solve puzzles.

Screen resolution: 1280 x 720


Code using original images: 
index.png from the itch.io .
Dataset source: https://itch.io/jam/gbjam-7/rate/470668
load.png from CLKER.com
Dataset source:http://www.clker.com/clipart-load-all-button.html
save.png from Clker.com
Dataset source:http://www.clker.com/clipart-save-button-png-4.html
pause.png from deposite photos
https://depositphotos.com/cn/vector/exposure-photo-camera-icons-set-79726132.html
unpaese.png from freepik
https://www.freepik.com/icon/fast-forward_162353
star1.png from aseprite
https://community.aseprite.org/t/how-to-make-buttons/10584

"""


#create a game map to display a general structure
game_map=[
 [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
 [0, 1, 1, 1, 0, 0, 0, 4, 1, 0],
 [1, 1, 0, 0, 0, 0, 3, 0, 1, 1],
 [1, 4, 0, 0, 1, 0, 0, 0, 2, 1],
 [1, 4, 0, 0, 0, 3, 0, 3, 0, 1],
 [1, 4, 4, 0, 3, 0, 1, 0, 0, 1],
 [1, 1, 4, 0, 0, 1, 0, 0, 1, 1],
 [1,1,0,0,3,0,3,0,1,1],
 [1,1,1,0,0,0,0,1,1,1],
 [1,1,1,1,1,1,1,1,1,1]
 ]

class Boxman():
    """ Boxman game """
    def __init__(self):
        """ game parameter settings """  
        global elapsed_time,is_running,leaderboard_data    
        self.canvas_bg  = '#d7d7d7'         # backgroundcolor of game
        self.cell_size  = 78                # size of cells
        self.cell_gap   = 1                 # size of cell gaps
        self.frame_x    = 25                # horizontal margin
        self.frame_y    = 25                # vertical margin
        self.max_cells  = 10                # maxmum cell numbers 
        self.win_w_plus = 270               # extra lenth of window 
        self.canvas_w   = len(game_map[0]) * self.cell_size + self.frame_x*2 #set the width for canvas
        self.canvas_h   = len(game_map) * self.cell_size + self.frame_y*2     #set the height for canvas
        self.win_w_size = self.canvas_w + self.win_w_plus                    #the width of window
        self.win_h_size = self.canvas_h                                      #the height of window
        self.pausetime_list=[]
        self.total_pausetime=None                                           #check if the function has been called
        leaderboard_data = []
        
        
    
    def boxman_xy(self):
        """ capture boxman coordinates """
        global boxman_x, boxman_y
        xy = []
        for i in range(0,len(game_map)):
            try: 
                x = game_map[i].index(2) + 1
            except:
                x = 0
            xy.append(x)
        boxman_x = max(xy)
        boxman_y = xy.index(boxman_x)
        boxman_x = boxman_x - 1 

        if boxman_x == -1: # value is not 2,so boxman is at end value is 6
            xy = []
            for i in range(0,len(game_map)):
                try:
                    x  = game_map[i].index(6) + 1
                except:
                    x = 0
                xy.append(x)
            boxman_x = max(xy)
            boxman_y = xy.index(boxman_x)
            boxman_x = boxman_x - 1
    
    
    def window_open(self):
        '''open main game window'''
        global window,px,py,man_gif,moves,moves_label,is_paused,pause_button,unpause_button,save_button,start_time,timer_label,elapsed_time,starttime,total_pause
        window = tk.Tk()
        window.focus_force()
        window.title('Boxman')
          # Center the window using the Boxman class method
        Boxman().window_center(window,self.win_w_size,self.win_h_size) 
        man_gif = 0
        moves = 0
        is_paused = False
        total_pause = False
        


        
        starttime=datetime.datetime.now()
        # Create a frame within the window
        frame = tk.Frame(window)
        frame.grid(row=0,column=1, sticky="e")
        # Pause button and associated text
        pause_text=tk.Label(frame,text='Pause: ',font=('Arial', 15,'bold'),anchor="center", justify="right",fg="#7bcf7d")
        pause_text.grid(row=3,column=0, sticky="sw")
        pause_btn= tk.PhotoImage(file='pause.png')
        pause_button = tk.Button(frame, image=pause_btn, command=self.toggle_pause)
        pause_button.grid(row=4,column=0, sticky="sw")
         # Unpause button and associated text
        unpause_text=tk.Label(frame,text='Unpause: ',font=('Arial', 15,'bold'),anchor="center", justify="right",fg="#7bcf7d")
        unpause_text.grid(row=3,column=0, sticky="se")
        unpause_btn= tk.PhotoImage(file='unpause.png')
        unpause_button = tk.Button(frame, image=unpause_btn, command=self.toggle_unpause,font=('Arial', 15),anchor="center", justify="right",fg="black",bg="#E791A9")
        unpause_button.grid(row=4,column=0, sticky="se")
        # Save button and associated text
        save_text=tk.Label(frame,text='Save: ',font=('Arial', 15,'bold'),anchor="center", justify="right",fg="#7bcf7d")
        save_text.grid(row=7,column=0, sticky="sw")
        save_btn= tk.PhotoImage(file='save2.png')
        save_button = tk.Button(frame, image=save_btn, command=self.save_game,border=None)
        save_button.grid(row=8,column=0, sticky="sw")
        # Load button and associated text
        load_text=tk.Label(frame,text='Load: ',font=('Arial', 15,'bold'),anchor="center", justify="right",fg="#7bcf7d")
        load_text.grid(row=7,column=0, sticky="se")
        load_btn= tk.PhotoImage(file='load.png')
        load_button = tk.Button(frame, image=load_btn, command=self.load_game)
        load_button.grid(row=8,column=0, sticky="se")
         # Label to display the number of moves
        moves_label=tk.Label(frame,text="Moves: 0",font=('Arial', 30,'bold'),anchor="center", justify="right",fg="#ff4c78")
        moves_label.grid(row=0,column=0,sticky='n')
        #game instructions
        text_label=tk.Label(frame,text='\n'
                                        +'\n'
                                        +'White cells are empty spaces'
                                        +'\n'
                                        +'\n Grey cells are walls'
                                        +'\n'
                                        +'\n Green cells are boxes'
                                        +'\n'
                                        +'\n Pink cells are the end points'
                                        +'\n'
                                        +'\n Red cells are the completed boxes'
                                        +'\n'
                                        +'\n Press letters ADSW or arrow \n keys  to move'
                                        +'\n'
                                        +'\n Press letter R/r to undo the step'
                                        +'\n'
                                        +'\n Press letter C/c to cheat'
                                        +'\n'
                                        +'\n Press letter B/b when  your boss \n comes'
                                        +"\n"
                                        +'\n'
                                        +'\n'
                             ,
                             font=('Arial', 15),fg='#008080',anchor="ne", justify="left")
        text_label.grid(row=1,column=0,sticky='n')
        Boxman().boxman_xy()  
        Boxman().create_game_cells()
        # Bind the move_action method to key events
        window.bind('<Key>', Boxman().move_action)
        window.mainloop()
        
    def game_loop(self):
        global loop

        canvas.delete('all') 
        Boxman().create_game_cells()
        loop = window.after(100, Boxman().game_loop)


    
    def create_game_cells(self): 
        """ create game cells """  # Draw the map using the game_map list,
                                #corresponding to the colors in the dictionary color_dict
        global man_gif,pic_dict,canvas
        
        man_2 = ["2.png","22.png"] # picture when boxman in white spaces
        man_6 = ["6.png","66.png"] # picture when boxman in end points
         
         # Update the boxman picture based on the current frame    
        man_gif = man_gif + 1
        if man_gif > 1:
            man_gif = 0
            
        man_2[0] = man_2[man_gif]
        man_6[0] = man_6[man_gif]
         # Create a dictionary mapping cell values to PhotoImage objects
        pic_dict = {0: tk.PhotoImage(file =  '0.png'),
                    1: tk.PhotoImage(file =  '1.png'),
                    2: tk.PhotoImage(file = man_2[0]),
                    3: tk.PhotoImage(file =  '3.png'),
                    4: tk.PhotoImage(file =  '4.png'),
                    5: tk.PhotoImage(file =  '5.png'),
                    6: tk.PhotoImage(file = man_6[0])
                    }
        canvas = tk.Canvas(window, 
                           bg=self.canvas_bg, 
                           height=self.canvas_h,
                           width=self.canvas_w)
        for y in range(0,len(game_map)):
            for x in range(0,len(game_map[0])): 
                n = game_map[y][x] 
                canvas.create_image(self.frame_x*2 + self.cell_size*x + x*self.cell_gap, 
                                    self.frame_y*2 + self.cell_size*y + y*self.cell_gap,
                                    image = pic_dict[n],anchor="w") 
        canvas.grid(row=0,column=0)
    
    def toggle_pause(self):
        '''Press the button to pause the game'''
        global is_paused,pausetime,total_pause
        # Set flags to indicate that the game is paused
        total_pause=True
        is_paused = True
        pausetime=datetime.datetime.now()
    
    def toggle_unpause(self):
        '''Press the button to unpause the game'''
        global is_paused,unpausetime,total_pausetime,total_pause
        total_pause = True
        is_paused = False
        unpausetime=datetime.datetime.now()
        # Calculate the time gap during which the game was paused and update the total paused time
        pausetime_gap=unpausetime-pausetime
        self.pausetime_list.append(pausetime_gap)
        total_pausetime=sum(self.pausetime_list,datetime.timedelta())


    def save_game(self):
        """ Save the current game state to a file """
        global game_map, moves
        #save game data to the dictionary
        save_data = {'game_map': copy.copy(game_map), 'moves': moves,'boxman_x':copy.copy(boxman_x),'boxman_y':copy.copy(boxman_y)}
         # Use pickle to serialize and save the data to a file
        with open('save_game.pkl', 'wb') as file:
            pickle.dump(save_data, file)
        print("Game saved!")

    def load_game(self):
        """ Load the saved game state from a file """
        global game_map, moves,boxman_x,boxman_y
        try:
             # Attempt to load saved data from the file
            with open('save_game.pkl', 'rb') as file:
                save_data = pickle.load(file)
             # Update game state with the loaded data
            game_map = save_data['game_map']
            moves = save_data['moves']
            boxman_x=save_data['boxman_x']
            boxman_y=save_data['boxman_y']
            print("Game loaded!")
        except FileNotFoundError:
            print("No saved game found.")
            # Update moves label and redraw the game cells
        moves_label.config(text="Moves: {}".format(moves//12))
        Boxman().create_game_cells()

    def boss_key(self):
        """ Boss key action: flip to a work-related image """
        global boss_win,window, canvas, game_map, backup_map, record_list,moves
        #open a work_related window when press the button

        boss_win = tk.Toplevel()
        boss_win.focus_force()
        boss_win.title('Excel')
        Boxman().window_center(boss_win,2560,1664)


        bg = tk.PhotoImage(file = "work2.png")
        canvas1 = tk.Canvas( boss_win, width = 1500, height = 975)  
        canvas1.pack() 
        canvas1.create_image( 0, 0, image = bg, anchor = "nw") 
        boss_win.mainloop()
        # After the boss key action, redraw the original game cells
        Boxman().create_game_cells()

    def move_action(self,event): 
        """ control keys """
        global is_paused,boss_win,total_pause,leaderboard_data
        if(is_paused==False):
            
            def Boxman_move(event,key,x,y):
                    """ control boxman """
                    # 0:white space,  1:walls,  2:boxman,  3:boxes,  4:end points,  5:boxes on end points,  6:boxman standing on end points
                    global moves,moves_label
                    def operation_forward_none(f1,f2,f3,f4,f5):
                        """ the front are open spaces or end points """
                        if          game_map[boxman_y + y*1][boxman_x + x*1] == f1: ### the front are white space or end points
                            if      game_map[boxman_y + y*0][boxman_x + x*0] == 2:  #   boxman standing on white spaces
                                    game_map[boxman_y + y*0][boxman_x + x*0]  = f2  ### white spaces when boxman left
                                    game_map[boxman_y + y*1][boxman_x + x*1]  = f3  ### the front are white spaces or end points
                            else:                                                                         #   boxman standing on end points
                                    game_map[boxman_y + y*0][boxman_x + x*0]  = f4  ### the back are end points
                                    game_map[boxman_y + y*1][boxman_x + x*1]  = f5  ### the front are white spaces or end points

                    def operation_forward_box(f1,f2,f3,f4,f5,f6,f7):
                        """ the front are completed boxes """
                        if             game_map[boxman_y + y*1][boxman_x + x*1] == f1: ### the front are boxes on white spaces or end points
                            if         game_map[boxman_y + y*0][boxman_x + x*0] == 2:  #   boxman standing on white spaces
                                if     game_map[boxman_y + y*2][boxman_x + x*2] == f2: ### the front are white spaces or end points
                                    game_map[boxman_y + y*0][boxman_x + x*0]  = 0   #   white spaces when boxman left
                                    game_map[boxman_y + y*1][boxman_x + x*1]  = f3  ### the front are white spaces or end points
                                    game_map[boxman_y + y*2][boxman_x + x*2]  = f4  ### the front are boxes on white spaces or end points
                            else:                                                                         ### boxman on end points
                                if     game_map[boxman_y + y*2][boxman_x + x*2] == f5: 
                                    game_map[boxman_y + y*0][boxman_x + x*0]  = 4   
                                    game_map[boxman_y + y*1][boxman_x + x*1]  = f6  
                                    game_map[boxman_y + y*2][boxman_x + x*2]  = f7 

                    direction = event.keysym
                    if(direction == key):
                        operation_forward_none(0,0,2,4,2)
                        operation_forward_none(4,0,6,4,6)
                        operation_forward_box(3,0,2,3,0,2,3)
                        operation_forward_box(3,4,2,5,4,2,5)
                        operation_forward_box(5,0,6,3,0,6,3)
                        operation_forward_box(5,4,6,5,4,6,5)
                        
                        Boxman().boxman_xy()   # refresh coordinates
                        
                        temp = [] # record steps, used for undo steps
                        temp.append(boxman_y) # save boxman coordinates
                        temp.append(boxman_x) 
                        temp.append(game_map[boxman_y + 0][boxman_x + 0])
                        temp.append(game_map[boxman_y - 1][boxman_x + 0])
                        temp.append(game_map[boxman_y + 1][boxman_x + 0])
                        temp.append(game_map[boxman_y + 0][boxman_x - 1])
                        temp.append(game_map[boxman_y + 0][boxman_x + 1])
                        temp.append(game_map[boxman_y + y][boxman_x + x])
                        
                        record_list.append(temp)
                        
                        if len(record_list) > 1:
                            if record_list[-1] == record_list[-2]:
                                del record_list[-1]   # delete same data
                    if direction == 'Up' or direction == 'Down' or direction == 'Left' or direction == 'Right' or direction == 'w' or direction == 'W' or direction == 'a' or direction == 'A' or direction == 's' or direction == 'S' or direction == 'd' or direction == 'D' or direction == 'c' or direction == 'C':    
                         moves+= 1                    
                    moves_label.config(text="Moves: {}".format(moves//12))
            
            def cheat_code(event,key):
                """ Cheat code to complete the level instantly """
                global game_map, moves
                direction=event.keysym
                if direction == key:
                    for y in range(len(game_map)):
                        for x in range(len(game_map[0])):
                            if game_map[y][x] == 3:
                                # Move all boxes to their goal positions
                                game_map[y][x] = 0  # Empty space
                            elif game_map[y][x] == 5:
                                # Move completed boxes to their goal positions
                                game_map[y][x] = 4  # Goal position

                    moves += 1  # Increment moves counter (you may adjust this based on your game logic)
             # 0:white space,  1:walls,  2:boxman,  3:boxes,  4:end points,  5:boxes on end points,  6:boxman standing on end points       
            def key_handler(event,key):
                '''Toggle between boss key and game window'''
                global boss_win
                direction = event.keysym
                #check if the key pressed matches the specific key
                if direction == key:
                    Boxman().boss_key()
                    
            def restore_stage(event,key):
                """ restore steps """
                direction = event.keysym
                if(direction == key): 
                    def restore(): 
                    
                        m = game_map
                         # Variables to store values before and after a move
                        before_forward = 0                   
                        
                        before_stand   = record_list[-2][2]  
                        now_stand      = record_list[-1][2]  
                        now_forward    = record_list[-1][7] 

                        before_x       = record_list[-2][1]  
                        before_y       = record_list[-2][0]  
                        now_x          = record_list[-1][1]  
                        now_y          = record_list[-1][0]  
                        
                        b_up           = record_list[-2][3] 
                        b_dw           = record_list[-2][4]  
                        b_lf           = record_list[-2][5]  
                        b_rg           = record_list[-2][6] 

                        #  Extrapolates the value of the cell you previously faced
                        if     before_x         > now_x:
                            next_x           = now_x - 1
                            before_forward   = b_lf
                        elif   before_x         < now_x:
                            next_x           = now_x + 1
                            before_forward   = b_rg
                        else:
                            next_x           = now_x
                                
                        if     before_y         > now_y:
                            next_y           = now_y - 1
                            before_forward   = b_up
                        elif   before_y         < now_y:
                            next_y           = now_y + 1
                            before_forward   = b_dw
                        else:
                            next_y           = now_y
                        
                        
                        m[before_y][before_x] = before_stand 
                        m[   now_y][   now_x] = before_forward
                       
                        if                      before_forward == 3:
                            if                     now_forward == 3:
                                if                   now_stand == 2:
                                            m[next_y][next_x]  = 0
                                elif                 now_stand == 6:
                                            m[next_y][next_x]  = 0
                            elif                   now_forward == 5:
                                if                   now_stand == 2:
                                            m[next_y][next_x]  = 4
                                elif                 now_stand == 6:
                                            m[next_y][next_x]  = 0 
                                            
                        elif                    before_forward == 5:
                            if                     now_forward == 3:
                                if                   now_stand == 2:
                                            m[next_y][next_x]  = 0
                                elif                 now_stand == 6:
                                            m[next_y][next_x]  = 0
                            elif                   now_forward == 5:
                                if                   now_stand == 2:
                                            m[next_y][next_x]  = 0
                                elif                 now_stand == 6:
                                            m[next_y][next_x]  = 4
                    restore()
                    
                    del record_list[-1]  # Delete the last step from the record list


            

            def game_pass(): 
                """ if the number of boxes is 0,pass """
                global pausetime_gap,usertime,total_pause
                xy = []
                # Count the number of boxes in each row and sum them up
                for i in range(0,len(game_map)):
                    x = game_map[i].count(3)
                    xy.append(x)
                box_number = sum(xy)
                # If there are no boxes remaining, the game is won
                if box_number == 0:
                    
                    endtime = datetime.datetime.now()
                    # Check if the game was paused during play
                    if total_pause == True:
                        usertime=endtime-starttime-total_pausetime
                    else:
                        usertime=endtime-starttime
                    # Update the canvas, then call the pass_win function
                    canvas.update()
                    pass_win()
                

            def pass_win():
                """ show game pass message """
                global game_map,leaderboard_data
                # Show a message box congratulating the player
                showinfo('','Congrats! You win the game! \n'+'Time spent: '+str(usertime.total_seconds())+' s\n'+' You reached the goal in {} moves!'.format(moves//12))
                window.destroy()
                game_map = copy.deepcopy(backup_map)
                 # Ask the player for their name to update the leaderboard
                Boxman().ask_name()
                       

            #specity keys to move boxes
            Boxman_move(event,    'w',  0, -1)
            Boxman_move(event,    's',  0,  1)
            Boxman_move(event,    'a', -1,  0)
            Boxman_move(event,    'd',  1,  0)

            Boxman_move(event,    'W',  0, -1)
            Boxman_move(event,    'S',  0,  1)
            Boxman_move(event,    'A', -1,  0)
            Boxman_move(event,    'D',  1,  0)

            Boxman_move(event,   'Up',  0, -1)
            Boxman_move(event, 'Down',  0,  1)
            Boxman_move(event, 'Left', -1,  0)
            Boxman_move(event,'Right',  1,  0)
                

                
            restore_stage(event, 'r')
            restore_stage(event, 'R')
            
            cheat_code(event, 'c')
            cheat_code(event, 'C')

            key_handler(event,'B')
            key_handler(event,'b')

            canvas.delete('all')
            Boxman().create_game_cells()
            Boxman().boxman_xy() 
            
            game_pass()

    
        

    def window_center(self,window,w_size,h_size):
        """ center the window """
        screenWidth  =  window.winfo_screenwidth()  # capture width
        screenHeight = window.winfo_screenheight()  # capture height
         # Calculate the left and top coordinates to center the window
        left =  (screenWidth - w_size) // 2
        top  = (screenHeight - h_size) // 2
         # Set the window geometry to position it at the center of the screen
        window.geometry("%dx%d+%d+%d" % (w_size, h_size, left, top))
    
    def ask_name(self):
        '''ask username'''
        global nameget,ask_name_win,ask_canvas,player_name1,leaderboard_button
        ask_name_win=tk.Tk()
        ask_name_win.title("Enter Username")
        # Center the window on the screen using a method named 'window_center' (not provided in the code)
        Boxman().window_center(ask_name_win,1280,720)
        ask_canvas = tk.Canvas(ask_name_win,height=720,width=1280)
        ask_canvas.pack()
        photo = tk.PhotoImage(file="leaderboard.png")
        ask_canvas.create_image( 640, 360, image=photo)
        name_label=tk.PhotoImage(file="username2.png")
        ask_canvas.create_image((380,300), anchor="nw", image=name_label)
         # Create a text message on the canvas
        ask_canvas.create_text(620,100,font=('Purisa',30,'bold'),fill='#065535',text="Please Enter Your Name")
         # Create an Entry widget for entering the username
        nameget = tk.Entry(ask_name_win,width=30,font=('Arial 24'),fg='#87b8ea') 
        ask_canvas.create_window(480, 300,anchor='nw', window=nameget)
        # Create a button for accessing the leaderboard
        leaderboard_button = tk.Button(ask_canvas, text='Leaderboard', command=self.get_entry,fg='green',bg='#126577',font=('Arial 20 bold'))
        leaderboard_button.configure(bg="#126577", fg="green")
        ask_canvas.create_window(600, 500, anchor='nw', window=leaderboard_button)
        
        ask_name_win.mainloop()
    
    def get_entry(self):
        #get playername from entrybox
        player_name=[]
        name=nameget.get()
        if name=="":
            player_name.append("Anonymous")
        else:
            player_name.append(name)
             # Close the ask_name_win and update leaderboard
        ask_name_win.destroy()
        Boxman().update_leaderboard(player_name, moves // 12, usertime.total_seconds())
        Boxman().display_leaderboard()
    
    def to_game_start(self):
                  # Destroy canvas and index_win, then run the game
                 canvas.destroy()
                 index_win.destroy()
                 Boxman().run_game()

    def index_game(self):
        """ index page """  
        
        global index_win,canvas
        index_win = tk.Tk()
        
        index_win.title('Welcome to Boxman Game')
        Boxman().window_center(index_win,1000,600)
        canvas = tk.Canvas(index_win, width=1000, height=600)
        canvas.pack()
        #create a background image
        photo = tk.PhotoImage(file="index.png")
        canvas.create_image( 500, 300, image=photo)
        #create a button to start the game
        click_btn= tk.PhotoImage(file='start1.png')
        start = tk.Button(canvas,image=click_btn, borderwidth=0, command=self.to_game_start,activebackground='green')
        canvas.create_window(430, 500, anchor='nw', window=start)
        index_win.mainloop()
    
    def run_game(self):
        '''Run Game '''
        global backup_map,record_list,player_name
        #initialize variables
        record_list = [] 
        backup_map = []  
        backup_map = copy.deepcopy(game_map)  
        Boxman().window_open()

    def update_leaderboard(self, player_name, moves, time_spent):
        '''update leaderboard data every time when playing game'''
        global leaderboard_data
         # Extract data from function arguments
        name=player_name
        Move=moves
        Time=time_spent
       # Create a list representing the leaderboard entry
        leaderboard_data=[name,Move,Time]
        # Append the leaderboard entry to the 'leaderboard.txt' file
        with open('leaderboard.txt', 'a') as file:
                file.write(str(leaderboard_data[0])+" "+ \
                           str(leaderboard_data[1])+" "+ \
                           str(leaderboard_data[2])+"\n")

    def display_leaderboard(self): 
        '''show leaderboard window''' 
        global leaderboard_window  
        leaderboard_window= tk.Tk()
        leaderboard_window.title('Leaderboard')
        Boxman().window_center(leaderboard_window,1280,720)
        leaderboard_canvas=tk.Canvas(leaderboard_window,width=1280,height=720)
        #leaderboard background image
        photo = tk.PhotoImage(file="leaderboard.png")
        leaderboard_canvas.create_image(640,360,image=photo)
        leaderboard_canvas.create_text(640,100,font=('Purisa',30,'bold'),fill='black',text="LEADERBOARD")
        #create treeview to show names and scores
        style=ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background='#b0e7ff',
                        foreground='black',
                        rowheight=30,
                        fieldbackground='b0e7ff',
                        font=('Purisa',20,'bold'),
                        anchor='center'
                        )
        leaderboard_tree = ttk.Treeview(leaderboard_canvas,columns=('Name',"Moves","Time"),show="headings")
        leaderboard_tree.heading("Name",text="Name")
        leaderboard_tree.heading("Moves",text="Moves")
        leaderboard_tree.heading("Time",text="Time(s)")
         # Read data from the 'leaderboard.txt' file
        leaderboard_data=[]
        fhand = open('leaderboard.txt', 'r').readlines()
        for line in fhand:
             x=line.split()
             leaderboard_data.append([x[0], int(x[1]), float(x[2])])
        # Sort and display the top 6 entries
        sorted_leaderboard_data=sorted(leaderboard_data,key=lambda x: (x[1], x[2]),reverse=False)
        sorted_leaderboard_data=sorted_leaderboard_data[:6]
        for data in sorted_leaderboard_data:
             leaderboard_tree.insert("","end",values=(data[0][2:-2],data[1],data[2]))
        leaderboard_tree.place(x=330,y=200)
        #add a button to end the game
        leader_button = tk.Button(leaderboard_canvas, text='End Game', command=self.end_game,fg='green',bg='#126577',font=('Arial 20 bold'))
        leader_button.place(x=600,y=600)
        leaderboard_canvas.pack()
        leaderboard_window.mainloop()
    
    def end_game(self):
        '''Destroy the leaderboard_window'''
        leaderboard_window.destroy()


if __name__ == '__main__':
    Boxman().index_game()