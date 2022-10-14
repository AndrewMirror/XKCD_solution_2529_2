from random import *
from matplotlib import pyplot as plt
import time
start = time.time()

N = 5

G_limit = 200
Step_limit = 1000


def Game(N,Step_limit):
    Grid = [[0 for i in range(G_limit)] for i in range(G_limit)]

    Player_pos = [100,100]

    N = N

    #x1 = [int(Player_pos[0])] #For graphs per game
    #y1 = [int(Player_pos[1])]

    #x2 = [int(Player_pos[0])]
    #y2 = [int(Player_pos[1])]

    Grid[Player_pos[0]][Player_pos[1]] = 2
    ct1=0
    ct2=0

    steps_to_marble = N-1
    points = [(Player_pos[0],Player_pos[1])]
    for Step in range(Step_limit+50):

        if  Grid[Player_pos[0]+1][Player_pos[1]] > 0 and Grid[Player_pos[0]][Player_pos[1]+1] > 0 and Grid[Player_pos[0]-1][Player_pos[1]] > 0 and Grid[Player_pos[0]][Player_pos[1]-1] > 0:
            break
    
        step_taken = False
    
        luck = getrandbits(2)
        #luck = randrange(4)
        #luck = randint(0,3)
        #luck = 1
        
        if luck == 0:
            if Grid[Player_pos[0]+1][Player_pos[1]] == 0:
                Player_pos[0] += 1
                step_taken = True
        if luck == 1:
            if Grid[Player_pos[0]][Player_pos[1]+1] == 0:
                Player_pos[1] += 1
                step_taken = True
        if luck == 2:
            if Grid[Player_pos[0]-1][Player_pos[1]] == 0:
                Player_pos[0] -= 1
                step_taken = True
        if luck == 3:
            if Grid[Player_pos[0]][Player_pos[1]-1] == 0:
                Player_pos[1] -= 1
                step_taken = True
            
        
        if step_taken and Player_pos[0]<=G_limit and Player_pos[1]<=G_limit:
            Grid[Player_pos[0]][Player_pos[1]] += 1
            if steps_to_marble == 0:
                steps_to_marble = N
                Grid[Player_pos[0]][Player_pos[1]] += 1
                points.append((Player_pos[0],Player_pos[1]))

                #x2.append(int(Player_pos[0]))
                #y2.append(int(Player_pos[1]))
            steps_to_marble -= 1
            #x1.append(int(Player_pos[0]))
            #y1.append(int(Player_pos[1]))
        if step_taken:
            ct1+=1
        if not step_taken:
            ct2+=1
        if ct1 >= Step_limit:
            break
    
    #print(ct2)
    #plt.scatter(x2,y2,color='green')
    #plt.plot(x1,y1)
    #plt.show()
    
    #points = Extract_Marbles(Grid)

    if Step_limit > 1:
        maxct = 2
    else:
        maxct = 1
    ct=1
    lin_ok = True
    #print(points)
    for i in range(len(points)-2):
        for j in range(len(points)-i-1):
            ct=0
            if (points[j+i][0]-points[i][0]) != 0:
                lin_ok = True
                k = (points[j+i][1]-points[i][1])/(points[j+i][0]-points[i][0])
            else:
                lin_ok = False
                k=0
            b = points[i][1] - k*points[i][0]
            for m in range(len(points)-i-j):
                if lin_ok:
                    if Linear(k,b,points[m][0])==points[m][1]:
                        ct += 1
                else:
                    if points[m][0] == points[i][0]:
                        ct += 1
                if ct>maxct:
                        maxct = ct
    #print('points:', len(points))
    #print('max marbles on line:', maxct)
    #print('turns:',ct1)
    return maxct, ct1#Return what we actually need
    #return ct1 #Return how many turns

def Linear(k,b,x):
    y = k*x + b
    return y

''' #Obsolete idiotic idea
def Extract_Marbles(Grid):
    points = []
    for i in range(len(Grid)):
        for j in range(len(Grid[i])):
            if Grid[i][j] == 2:
                points.append((i,j))
    return points
'''


one_game_est = 0.000622

number_of_games = 200
K = 50
N = 20
ct = 0

est_time = one_game_est*K*N*number_of_games
if est_time > 60:
    print("estimated time: ", round(est_time/60,2),'min')
else:
    print("estimated time: ", round(est_time),'s')

import numpy as np
#from mpl_toolkits.mplot3d import Axes3D

x_K = [i for i in range(K)]
y_N = [i for i in range(N)]

X,Y = np.meshgrid(x_K,y_N)

Z = X+Y

for k in x_K:
    print(k)
    for n in y_N:
        if n>k:
            Z[n][k] = 1
            continue
        ct=0
        ct1=0
        #ctfails=0
        for i in range(number_of_games):
            game = Game(n,k)
            maxct = game[0]
            turns = game[1]
            if turns < k: 
                #ctfails+=1
                continue
            ct1+=1
            ct+=maxct
        #print('=',ctfails)
        if ct1==0:
            ct1=1
        av = ct/ct1
        #print('average for N =',n)
        #print('is',av)
        Z[n][k] = av

#Z[8][1] = 2
#plt.scatter(x_N,y_N)
#plt.show()


#fig = plt.figure()
#ax = plt.axes(projection='3d')
#ax.plot_wireframe(X, Y, Z, color='black')

fig,ax=plt.subplots(1,1)
cp = ax.contourf(X, Y, Z)
fig.colorbar(cp)

act_time = time.time()-start
if act_time > 60:
    print("elapsed time: ", round(act_time/60,2),'min')
else:
    print("elapsed time: ", round(act_time),'s')

print('estimation accuracy:',round(100*(time.time()-start)/est_time,2),'%')
plt.show()



'''





length_x = [i for i in range(400)]
length_y = [0 for i in range(400)]

#Code for part 1 finding how long a game is
number_of_games = 100
ct=0
SD = 0

for i in range(number_of_games):
    game = Game(1,100)[1]
    ct += game
    if game<400:
        length_y[int(game)]+=1
    else:
        length_y[int(399)]+=1
        
av=ct/number_of_games

for i in range(300):
    SD += ((length_x[i]-av)**2)*length_y[i]
SD /= 299
print(SD**0.5)

print(av)

plt.scatter(length_x,length_y)
plt.show()



'''
