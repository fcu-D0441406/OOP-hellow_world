import numpy as np


class board:
    chess_map = list()
    steps = 0
    width,height = None,None
    def __init__(self,width,height):
        self.width,self.height = width,height
        for i in range(height+1):
            temp = list()
            for j in range(width+1):
                temp.append(0)
            self.chess_map.append(temp)
    
    def update(self,width,height,player):
        if(self.chess_map[height][width]==0):
            self.chess_map[height][width] = player
            is_winner,player = self.check_winner(width,height,player)                
            self.steps+=1
            return is_winner,player
        else:
            print('error,have chess')
            return None,None
    
    def check_winner(self,width,height,player):
        def check_straight(width,height,player):
            for i in range(self.height-5):
                win = True
                for j in range(5):
                    if(self.chess_map[i+j][width]!=player):
                        win = False
                        break
                if(win==True):
                    return 1,player
            return -1,0
                     
        def check_line(width,height,player):
            for i in range(self.width-5):
                win = True
                for j in range(5):
                    if(self.chess_map[height][i+j]!=player):
                        win = False
                        break
                if(win==True):
                    return 1,player
            
            return -1,0
        
        def check_lr_oblique(width,height,player):
            left = min(width,height)
            right = min(self.width-width,self.height-height)
            #print(self.width,self.height,width,height,left,right)
            if(left+right<5):
                return -1,0
            else:
                for i in range(left+right):
                    win = True
                    for j in range(5):
                        if(self.chess_map[height-left+i+j][width-left+i+j]!=player):
                            win = False
                            break
                    if(win==True):
                        return 1,player
                return -1,0
                        
        def check_rl_oblique(width,height,player):
            left = min(width,self.height-height)
            right = min(self.width-width,height)
            if(left+right<5):
                return -1,0
            else:
                for i in range(left+right):
                    win = True
                    for j in range(5):
                        if(self.chess_map[height-right+i+j][width+right-i-j]!=player):
                            win = False
                            break
                    if(win==True):
                        return 1,player
                return -1,0
        
        a_state,a_winner = check_straight(width,height,player)
        b_state,b_winner = check_line(width,height,player)
        c_state,c_winner = check_lr_oblique(width,height,player)
        d_state,d_winner = check_rl_oblique(width,height,player)
        if(a_state==1 or b_state==1 or c_state==1 or d_state==1):
            return 1,player
        else:
            return -1,0
    def show_chess_map(self):
        for i in range(self.height):
            print(self.chess_map[i])

bb = board(9,9)
for i in range(5):
    a,b = bb.update(i+2,5-i,1)
    bb.show_chess_map()
    print(a,b)
            
            
            
    
    
