import numpy as np
import time

def copy_map(chess_map):
    copy_map = list()
    for i in range(len(chess_map)):
        temp = list()
        for j in range(len(chess_map[i])):
            temp.append(chess_map[i][j])
        copy_map.append(temp)
    return copy_map


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
    
    def update(self,x,y,player):
        if(self.chess_map[y][x]==0):
            self.chess_map[y][x] = player             
            self.steps+=1
        else:
            print('error,have chess')
            return None,None
    
    def check_winner(self,chess_map,x,y,player):
        def check_straight(x,y,player):
            for i in range(self.height+1-5):
                win = True
                for j in range(5):
                    if(chess_map[i+j][x]!=player):
                        win = False
                        break
                if(win==True):
                    return 1,player
            return -1,0
                     
        def check_line(x,y,player):
            for i in range(self.width+1-5):
                win = True
                for j in range(5):
                    if(chess_map[y][i+j]!=player):
                        win = False
                        break
                if(win==True):
                    return 1,player
            
            return -1,0
        
        def check_lr_oblique(x,y,player):
            left = min(x,y)
            right = min(self.width-1-x,self.height-1-y)
            if(left+right+1<5):
                return -1,0
            else:
                for i in range(left+right+1-4):
                    win = True
                    for j in range(5):
                        if(chess_map[y-1-left+i+j][x-1-left+i+j]!=player):
                            win = False
                            break
                    if(win==True):
                        return 1,player
                return -1,0
                        
        def check_rl_oblique(x,y,player):
            right = min(self.width-1-x,y)
            left = min(x,self.height-1-y)
            if(left+right+1<5):
                return -1,0
            else:
                for i in range(left+right+1-4):
                    win = True
                    for j in range(5):
                        if(chess_map[y-right+i+j][x+right-i-j]!=player):
                            win = False
                            break
                    if(win==True):
                        return 1,player
                return -1,0
        
        a_state,a_winner = check_straight(x,y,player)
        b_state,b_winner = check_line(x,y,player)
        c_state,c_winner = check_lr_oblique(x,y,player)
        d_state,d_winner = check_rl_oblique(x,y,player)
        if(a_state==1 or b_state==1 or c_state==1 or d_state==1): 
            return 1,player
        else:
            return -1,0
        
    def show_chess_map(self,chess_map):
        print(' ',[i for i in range(self.height)])
        for i in range(self.height):
            print(i,chess_map[i])
        print()
    
    def out_map(self,x,y):
        if(x==-1 or y==-1 or self.board.width<=x or self.board.height<=y):
            return False
        return True

class Tree:
    def __init__(self,root,node,alpha,beta,x,y,deep,is_win=0):
        self.x = x
        self.y = y
        self.deep = deep
        self.point = None
        self.alpha = alpha
        self.beta = beta
        self.root = root
        self.node = []
        self.is_win = is_win
    
    def add_node(self,node):
        self.node.append(node)
    
    def add_root(self,root):
        self.root = root
    
    def show_node(self,node):
        for i in range(len(node.node)):
            self.show_node(node.node[i])
        print(node.x,node.y,node.deep,node.alpha,node.beta,node.point)
            

class ai_chess:
    
    def __init__(self,player,enemy,deep,board):
        self.mine = player
        self.enemy = enemy
        self.deep = deep
        self.board = board
        
    def select(self,chess_map):
        def get_best_node(node):
            for i in range(len(node.node)):
                if(node.node[i].is_win==1):
                    node.x = node.node[i].x
                    node.y = node.node[i].y
                    break
                if(node.node[i].point==node.alpha):
                    node.x = node.node[i].x
                    node.y = node.node[i].y
                    
        root_node = Tree(None,None,-100000,100000,None,None,0)
        
        for i in range(self.board.height):
            for j in range(self.board.width):
                if(self.near_chess(chess_map,j,i)==True):
                    self.alpha_beta_cut(chess_map,root_node,1,1,j,i)
        
        #root_node.show_node(root_node)
        get_best_node(root_node)
        print(root_node.x,root_node.y,root_node.alpha,root_node.beta,root_node.point)
        #print('best node',root_node.x,root_node.y,root_node.alpha,root_node.beta)
        return root_node.x,root_node.y
    
      
    def alpha_beta_cut(self,chess_map,root,player,deep,x,y):
        if(root.alpha>root.beta or chess_map[y][x]!=0):
            return
        
        state = copy_map(chess_map)
        state[y][x] = player
        is_win,_ = self.board.check_winner(state,x,y,player)
        node = Tree(root,None,root.alpha,root.beta,x,y,deep)
        root.add_node(node)
        node.add_root(root)
        
        if(is_win==1):
            if(deep%2==1):
                root.alpha = 10000
                node.point = 10000
            else:
                root.beta = -10000
                node.point = -10000
            return
        
        if(deep<self.deep):
            for i in range(self.board.height):
                for j in range(self.board.width):
                    if(self.near_chess(state,j,i)==True):
                        if(deep%2==0):
                            self.alpha_beta_cut(state,node,self.mine,deep+1,j,i)
                        else:
                            self.alpha_beta_cut(state,node,self.enemy,deep+1,j,i)
                    if(node.alpha>node.beta):
                        return
            
        if(deep==self.deep):
            
            is_win1,mine_point = self.evaluate(state,self.mine,self.enemy)
            is_win2,enemy_point = self.evaluate(state,self.enemy,self.mine)
            point = 0
            if(is_win1==1):
                point = 10000
                node.point = 10000
            elif(is_win2==1):
                point = -10000
                node.point = -10000
            else:
                point = mine_point+enemy_point
                #print(mine_point,enemy_point)
                node.point = point
            
            if(deep%2==0):
                if(point<root.beta):
                    print(x,y,point,deep)
                    self.board.show_chess_map(state)
                    root.beta = point
                    root.point = point
            else:
                if(point>root.alpha):
                    print(x,y,'point',point,'root_alpha',root.alpha,deep)
                    self.board.show_chess_map(state)
                    root.alpha = point
                    root.point = point
        else:
            if(deep%2==0):
                if(node.alpha<root.beta):
                    print(x,y,node.alpha,deep)
                    self.board.show_chess_map(state)
                    root.beta = node.alpha
                    root.point = node.alpha
            else:
                if(node.beta>root.alpha):
                    print(x,y,node.beta,deep)
                    self.board.show_chess_map(state)
                    root.alpha = node.beta
                    root.point = node.alpha
            
            
    def near_chess(self,chess_map,x,y):
        def out_map(chess_map,x,y):
            if(x<0 or y<0 or x>=self.board.width or y>=self.board.height):
                return False
            return True
        
        for i in range(y-1,y+2):
            for j in range(x-1,x+2):
                if(out_map(chess_map,j,i)==True):
                    if(chess_map[i][j]!=0):
                        return True
        return False
    
    def evaluate(self,chess_map,mine,enemy):
        five = [[mine,mine,mine,mine,mine]]
        life_four = [[0,mine,mine,mine,mine,0]]
        dead_four = [[0,mine,mine,mine,mine,enemy],[enemy,mine,mine,mine,mine,0],[mine,0,mine,mine,mine],
                     [mine,mine,0,mine,mine],[mine,mine,mine,0,mine]]
        life_three = [[0,mine,mine,mine,0],[0,mine,mine,0,mine,0]]
        dead_three = [[enemy,mine,mine,mine,0],[0,mine,mine,mine,enemy],[enemy,0,mine,mine,mine,0,enemy],[mine,0,mine,0,mine,0],[0,mine,0,mine,0,mine],[enemy,mine,mine,0,mine,0],
                      [0,mine,mine,0,mine,enemy],[enemy,mine,0,mine,mine,0],[0,mine,0,mine,mine,enemy],[0,mine,0,0,mine,mine,0],[0,mine,mine,0,0,mine,0]]
        life_two = [[0,mine,mine,0],[0,mine,0,mine,0],[0,mine,0,0,mine,0]]
        dead_two = [[0,mine,mine,enemy],[enemy,mine,mine,0],[0,enemy,mine,mine,0]]
        
        def is_five(chess_map):
            five_num = 0
            for i in range(len(five)):
                for j in range(len(chess_map)-len(five[i])+1):
                    if(five[i] in [chess_map[j:j+len(five[i])]]):
                        print('is_wi')
                        five_num+=1
            return five_num
        
        def is_life_four(chess_map):
            life_four_num = 0
            for i in range(len(life_four)):
                for j in range(len(chess_map)-len(life_four[i])+1):
                    if(life_four[i] in [chess_map[j:j+len(life_four[i])]]):
                        life_four_num+=1
            return life_four_num
        
        def is_dead_four(chess_map):
            dead_four_num = 0
            for i in range(len(dead_four)):
                for j in range(len(chess_map)-len(dead_four[i])+1):
                    if(dead_four[i] in [chess_map[j:j+len(dead_four[i])]]):
                        dead_four_num+=1
            return dead_four_num
        
        def is_life_three(chess_map):
            life_three_num = 0
            for i in range(len(life_three)):
                for j in range(len(chess_map)-len(life_three[i])+1):
                    if(life_three[i] in [chess_map[j:j+len(life_three[i])]]):
                        life_three_num+=1
            return life_three_num
        
        def is_dead_three(chess_map):
            dead_three_num = 0
            for i in range(len(dead_three)):
                for j in range(len(chess_map)-len(dead_three[i])+1):
                    if(dead_three[i] in [chess_map[j:j+len(dead_three[i])]]):
                        dead_three_num+=1
            return dead_three_num
        
        def is_life_two(chess_map):
            life_two_num = 0
            for i in range(len(life_two)):
                for j in range(len(chess_map)-len(life_two[i])+1):
                    if(life_two[i] in [chess_map[j:j+len(life_two[i])]]):
                        life_two_num+=1
            return life_two_num
        
        def is_dead_two(chess_map):
            dead_two_num = 0
            record = np.zeros([len(chess_map)])
            for i in range(len(dead_two)):
                for j in range(len(chess_map)-len(dead_two[i])+1):
                    if(dead_two[i] in [chess_map[j:j+len(dead_two[i])]]):
                        record[j:j+len(dead_two[i])] = 1
                        dead_two_num+=1
            return dead_two_num
        
        def evaluate_stratege_point(chess_map):
            if(sum(chess_map)==0):
                return [0,0,0,0,0,0,0]
            five_num = is_five(chess_map)
            life_four_num = is_life_four(chess_map)
            dead_four_num = is_dead_four(chess_map)
            life_three_num = is_life_three(chess_map)
            dead_three_num = is_dead_three(chess_map)
            life_two_num = is_life_two(chess_map)
            dead_two_num = is_dead_two(chess_map)
            
            return [five_num,life_four_num,dead_four_num,life_three_num,dead_three_num,life_two_num,dead_two_num]
        
        def evaluate_straight_chess(chess_map):
            stratege = [0,0,0,0,0,0,0]
            a = 0
            for i in range(self.board.width):
                s = evaluate_stratege_point([chess_map[j][i] for j in range(self.board.height)])
                for j in range(len(stratege)):
                    stratege[j]+=s[j]
                    a+=s[j]
            return stratege
        
        
        def evaluate_line_chess(chess_map):
            stratege = [0,0,0,0,0,0,0]
            a = 0
            for i in range(self.board.height):
                s = evaluate_stratege_point([chess_map[i][j] for j in range(self.board.height)])
                for j in range(len(stratege)):
                    stratege[j]+=s[j]
                    a+=s[j]
            return stratege
        
        def evaluate_lr_chess(chess_map):
            stratege = [0,0,0,0,0,0,0]
            a = 0
            for i in range(0,self.board.width-4):
                if(i==0):
                    s = evaluate_stratege_point([chess_map[i+j][j] for j in range(i,self.board.width)])
                    for j in range(len(stratege)):
                        stratege[j]+=s[j]
                        a+=s[j]
                else:
                    s = evaluate_stratege_point([chess_map[i+j][j] for j in range(0,self.board.width-i)])
                    s2 = evaluate_stratege_point([chess_map[j][i+j] for j in range(0,self.board.width-i)])
                    for j in range(len(stratege)):
                        stratege[j]+=s[j]+s2[j]
                        a+=s[j]
            return stratege
        
        def evaluate_rl_chess(chess_map):
            stratege = [0,0,0,0,0,0,0]
            a = 0
            for i in range(0,self.board.width-5):
                if(i==0):
                    s = evaluate_stratege_point([chess_map[self.board.width-1-i-j][j] for j in range(i,self.board.width)])
                    for j in range(len(stratege)):
                        stratege[j]+=s[j]
                        a+=s[j]
                else:
                    s = evaluate_stratege_point([chess_map[i+j][self.board.width-j-1] for j in range(0,self.board.width-i)])
                    #print()
                    s2 = evaluate_stratege_point([chess_map[j][self.board.width-i-j-1] for j in range(0,self.board.width-i)])
                    for j in range(len(stratege)):
                        stratege[j]+=s[j]+s2[j]
                        a+=s[j]
            return stratege
        
        def cal_point(stratege,player):
            bonus = 0
            if(player==self.enemy):
                bonus = 9000
            if(stratege[0]>=1):
                return 1,10000+bonus
            if(stratege[1]>=1 or stratege[2]>=2):
                return 0,9900+bonus
            elif(stratege[2]>=1 and stratege[3]>=1):
                return 0,9800+bonus
            elif(stratege[3]>=2):
                return 0,8000+bonus
            elif(stratege[2]==1):
                return 0,2000+bonus
            elif(stratege[3]==1):
                return 0,1000+bonus
            else:
                return 0,10*stratege[6]+30*stratege[5]+50*stratege[4]
            
        
        if(mine==self.mine):
            stratege = evaluate_straight_chess(chess_map)
            stratege2 = evaluate_line_chess(chess_map)
            stratege3 = evaluate_lr_chess(chess_map)
            stratege4 = evaluate_rl_chess(chess_map)
            all_stratege = [stratege[j]+stratege2[j]+stratege3[j]+stratege4[j] for j in range(len(stratege))]
            is_win,point = cal_point(all_stratege,mine)
            #print(all_stratege)
            return is_win,point-10
        elif(mine==self.enemy):
            stratege = evaluate_straight_chess(chess_map)
            stratege2 = evaluate_line_chess(chess_map)
            stratege3 = evaluate_lr_chess(chess_map)
            stratege4 = evaluate_rl_chess(chess_map)
            all_stratege = [stratege[j]+stratege2[j]+stratege3[j]+stratege4[j] for j in range(len(stratege))]
            is_win,point = cal_point(all_stratege,mine)
            #print(all_stratege)
            return is_win,-1*point
    
                
   
width,height = 13,13

bb = board(width,height)
#a,b = bb.update(width//2,height//2,2)
AI = ai_chess(1,2,3,bb)
'''
#####
bb.update(4,4,2)
AI_choice_x,AI_choice_y = AI.select(bb.chess_map)
bb.update(AI_choice_x,AI_choice_y,1)
#print('1',AI.evaluate(bb.chess_map,1,2))
#print('2',AI.evaluate(bb.chess_map,2,1))
bb.show_chess_map(bb.chess_map)
bb.update(4,5,2)
AI_choice_x,AI_choice_y = AI.select(bb.chess_map)
bb.update(AI_choice_x,AI_choice_y,1)
#print('1',AI.evaluate(bb.chess_map,1,2))
#print('2',AI.evaluate(bb.chess_map,2,1))
bb.show_chess_map(bb.chess_map)
#####
'''
'''
while(True):
    step = bb.steps
    print(step)
    if(step%2==0):
        x,y = input().split()
        bb.update(int(x),int(y),1)
    else:
        x,y = input().split()
        bb.update(int(x),int(y),2)
    bb.show_chess_map(bb.chess_map)
    print('1',AI.evaluate(bb.chess_map,1,2))
    
    print('2',AI.evaluate(bb.chess_map,2,1))
'''


while(True):
    step = bb.steps
    print(step)
    if(step%2==0):
        x,y = input().split()
        bb.update(int(x),int(y),2)
        is_winner,player = bb.check_winner(bb.chess_map,int(x),int(y),2)  
    else:
        AI_choice_x,AI_choice_y = AI.select(bb.chess_map)
        bb.update(AI_choice_x,AI_choice_y,1)
        is_winner,player = bb.check_winner(bb.chess_map,AI_choice_x,AI_choice_y,1)   
    bb.show_chess_map(bb.chess_map)
    if(is_winner==1):
        print('winner',player)
        break

