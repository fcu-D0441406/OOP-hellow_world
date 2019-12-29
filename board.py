import numpy as np
import copy

class board:
    chess_map = list()
    steps = 0
    width,height = None,None
    def __init__(self,width,height):
        self.width,self.height = width,height
        for i in range(height):
            temp = list()
            for j in range(width):
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
            for i in range(self.height+1-5):
                win = True
                for j in range(5):
                    if(self.chess_map[i+j][width]!=player):
                        win = False
                        break
                if(win==True):
                    return 1,player
            return -1,0
                     
        def check_line(width,height,player):
            for i in range(self.width+1-5):
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
            right = min(self.width-1-width,self.height-1-height)
            if(left+right<5):
                return -1,0
            else:
                for i in range(left+right+1-5):
                    win = True
                    for j in range(5):
                        if(self.chess_map[height-left+i+j][width-left+i+j]!=player):
                            win = False
                            break
                    if(win==True):
                        return 1,player
                return -1,0
                        
        def check_rl_oblique(width,height,player):
            right = min(self.width-1-width,height)
            left = min(width,self.height-1-height)
            if(left+right<5):
                return -1,0
            else:
                for i in range(left+right+1-5):
                    win = True
                    for j in range(5):
                        if(self.chess_map[height-right-i+j][width+right+i-j]!=player):
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

class Tree:
    def __init__(self,root,node,val,x,y,deep):
        self.x = x
        self.y = y
        self.deep = deep
        self.alpha = -1000000
        self.beta = 10000000
        self.root = root
        self.node = []
    
    def add_node(self,node):
        self.node.append(node)
    
    def add_root(self,root):
        self.root = root
            
    

class ai_chess:
    
    def __init__(self,player,deep,board):
        self.mine = player
        self.deep = deep
        self.board = board
        
    def select(self,chess_map):
        root_node = Tree(None,None,0,None,None)
        for i in range(height):
            for j in range(width):
                AI.search(chess_map,root_node,1,0,j,i)
    
    def minimax(self,chess_map):
        
    '''
    def select_max_node(self,node,max_node):
        if(len(node.node)==0):
            if(max_node[0]<node.val):
                max_node[0] = node.val
                max_node[1] = node.root_x
                max_node[2] = node.root_y
        for i in range(len(node.node)):
            self.select_max_node(node.node[i],max_node)
    '''        
    def search(self,chess_map,root,player,deep,x,y):
        
        state = copy.deepcopy(chess_map)
        if(state[y][x]==0 and deep<self.deep):
            state[y][x] = player
            point_node = Tree(root,None,0,x,y,deep)
            root.add_node(point_node)
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if(deep%2==1):
                        self.search(copy.deepcopy(state),point_node,1,deep+1,j,i)
                    else:
                        self.search(copy.deepcopy(state),point_node,2,deep+1,j,i)
    
    
    def evaluate(self,chess_board,player):
        if(player==1):
            return 1
        else:
            return -1
    
    def search_recursive(self,chess_board):
        pass
                
   
width,height = 7,7

bb = board(width,height)
AI = ai_chess(1,2,bb)
#AI_choice = AI.select(bb.chess_map)
'''
while(True):
    step = bb.steps
    print(step)
    if(step%2==1):
        x,y = input().split()
        a,b = bb.update(int(x),int(y),2)
    else:
        AI_choice = AI.select(bb.chess_map)
        a,b = bb.update(AI_choice[1],AI_choice[2],1)
    bb.show_chess_map()
    if(a==1):
        print('winner',b)
        break
'''    

for i in range(5):
    a,b = bb.update(5-i,i,1)
    bb.show_chess_map()
    print(a,b)
