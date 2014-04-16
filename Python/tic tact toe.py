from Tkinter import *
import sys

#Global variables 
BOT=1
HUM=-1
DRAW=0



class matrix():
    def __init__(self):
        self.mat=[[],[],[]]  #3x3 board
        for  i in range(0,3) :
            for j in range(0,3) :
                self.mat[i].append(0)

    def copy(self,temp):
        for  i in range(0,3) :
            for j in range(0,3) :
                self.mat[i][j]=temp.mat[i][j]


    #CHECK FOR WIN/LOSE/DRAW
    #IF COLUMN/ROW/DIAGONAL SUM IS 15, THEN HUMAN WINS
    #IF COLUMN/SUM/DIAGONAL SUM IS 9,  THEN AI WINS
    def win(self):
        
        #check rows
        for i in range(0,3):
            s=0
            for j in range(0,3):
                s+=self.mat[i][j]
            if(s==15):
                return HUM
            elif(s==9):
                return BOT


        #check columns
        for j in range(0,3):
            s=0
            for i in range(0,3):
                s+=self.mat[i][j]
            if(s==15):
                return HUM
            elif(s==9):
                return BOT

        #check main diagonal
        if(self.mat[0][0]+self.mat[1][1]+self.mat[2][2] == 15):
            return HUM
        elif((self.mat[0][0]+self.mat[1][1]+self.mat[2][2] == 9)):
            return BOT

        #check other diagonal
        if(self.mat[0][2]+self.mat[1][1]+self.mat[2][0] == 15):
            return HUM
        elif(self.mat[0][2]+self.mat[1][1]+self.mat[2][0] == 9):
            return BOT

        #draw
        flag=0;
        for i in range(0,3):
            for j in range(0,3):
                if(self.mat[i][j]==0):
                    flag=1
        if(flag):
            return -2
        else:
            return DRAW


    #DECIDING THE NEXT MOVE / MINIMAX 
    def next_move(self,turn):
        k=self.win()

        if(k==BOT):
            return BOT                 #RETURN VALUE BOT = 1 (BOT WINS)
        elif(k==HUM):
            return HUM                 #RETURN VALUE HUM = -1 (HUMAN WINS)
        elif(k==DRAW):
            return DRAW                #RETURN VALUE DRAW = 0 (DRAW)

        if(turn=='c'):                  #IF AI's TURN
            k=-99                       #INITIALLY SET TO MIN FOR COMPARISON WITH FIRST BRANCH VALUE OF MAX NODE
            for i in range(0,3):
                for j in range(0,3):
                    if(self.mat[i][j]==0):
                        self.mat[i][j]=3
                        temp=self.next_move('h')
                        if( temp > k):
                            k=temp
                        self.mat[i][j]=0
        else:
            k=99                   #INITIALLY SET TO MAX FOR COMPARISON WITH FIRST BRANCH VALUE OF MIN NODE
            for i in range(0,3):
                for j in range(0,3):
                    if(self.mat[i][j]==0):
                        self.mat[i][j]=5
                        temp=self.next_move('c')
                        if(temp < k):
                            k=temp
                        self.mat[i][j]=0
        return k

    def ai_move(self):
        change=matrix()
        k=-99;
        for i in range(0,3):
            for j in range(0,3):
                if(self.mat[i][j]==0):
                    self.mat[i][j]=3              #CHOSE LOCATION FOR COMPUTER MOVE
                    temp=self.next_move('h' )
                    if(temp>k):
                        k=temp
                        change.copy(self)         #STORE IF MOVE CHOSEN
                    self.mat[i][j]=0              #RESET LOCATION
        self.copy(change)                         #APPLY BEST CHOSEN MOVE)
        

#GUI
class grid():
    def __init__(self):
        self.root= Tk()
        self.Game=matrix()
        
        Label(self.root,text="TIC TAC TOE").pack(pady=10,padx=10) #top label

        self.rows=[]                            #Row of Frames

        for i in range(0,3):
            self.rows.append(Frame(self.root,borderwidth=2))
            self.rows[i].pack(side=TOP)
            
        self.resultF=Frame(self.root,borderwidth=2) #Bottom result Frame
        self.resultF.pack(side=BOTTOM)
        
        self.resultL=Label(self.resultF,text=" Game on! ",justify=CENTER) #Bottom result Label
        self.resultL.pack(pady=10,padx=10)
        
        self.restart=Button(self.resultF,text="RESTART",command=self.restart) #Restart Button
        self.restart.pack()
        
        self.matrix=[[],[],[]] #Button matrix
        
        for i in range(0,3):
            
            for j in range(0,3):
                self.matrix[i].append(Button(self.rows[i],text=' ',state=ACTIVE,height=10,\
                                             width=20,\
                                             command=lambda i=i,j=j : self.Click(i*10+j)\
                                             ,padx=2,pady=2))
                self.matrix[i][j].pack(side=LEFT)
                        
        
        self.root.mainloop()

    def Click(self,coords):
        for i in range(0,3):
            for j in range(0,3):
                if(i*10+j == coords):
                    print i,j
                    self.matrix[i][j]['state']='disabled'
                    self.matrix[i][j]['text']='X'
                    self.matrix[i][j]['bg']='yellow'
                    self.Game.mat[i][j]=5
                    
        self.check_game_state()     #check for game status

        self.Game.ai_move()         #AI Turn

        
        for i in range(0,3):        #Update grid with AI move
            for j in range(0,3):
                if(self.Game.mat[i][j]==3):
                    self.matrix[i][j]['state']='disabled'
                    self.matrix[i][j]['text']='O'
                    self.matrix[i][j]['bg']='red'

        self.check_game_state()


    def check_game_state(self):     #To check game status
        if(self.Game.win()==BOT):
            self.resultL['text']='Computer Wins!'
            self.game_over()
        elif( self.Game.win()==HUM):
            self.resultL['text']='You Wins!'
            self.game_over()
        elif( self.Game.win()==DRAW):
            self.resultL['text']='DRAW!'
            self.game_over()

    def restart(self):              #To restart game and reset buttons,variables
        for i in range(0,3):
            for j in range(0,3):
                self.matrix[i][j]['state']='normal'
                self.matrix[i][j]['bg']='gray'
                self.matrix[i][j]['text']=' '
                self.Game.mat[i][j]=0
        self.resultL['text']='Game on!'
        
    def game_over(self):            #Disable buttons at game over
        for i in range(0,3):
            for j in range(0,3):
                self.matrix[i][j]['state']='disabled'
                

grid() #Let's play
