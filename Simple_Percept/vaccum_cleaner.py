import random

grid = [
    [0, -1, 1],
    [1, 0, -1],
    [1, 1, 0]
]

charger = (2,2)

class agent:
    def __init__(self,x,y,battery = 5):
        self.x = x
        self.y = y
        self.battery = 5
    
    def percieve(self,grid):
        return grid[self.x][self.y]
    
    def decide(self,percept):
        if(self.battery<=1):
            return "go_to_charger"
        if(percept==1):
            return "clean"
        return "move"
    
    def action(self,grid):
        percept = self.percieve(grid)
        action = self.decide(percept)

        if(action=='clean'):
            print(f"Cleaning tile at{self.x}, {self.y}")
            grid[self.x][self.y] = 0

        elif(action=='go_to_charger'):
            print("Went to charger")
            self.x,self.y = 2,2

        elif(action=='move'):
            print("moving")
            self.move(grid)

        self.battery-=1
        print(f"Battery left {self.battery}")
        print()

    def move(self,grid):
        moves=[(1,0),(0,1),(-1,0),(0,-1)]
        random.shuffle(moves)

        for dx,dy in moves:
            nx,ny = self.x+dx, self.y+dy
            if(0<=nx<len(grid) and 0<=ny<len(grid)):
                if(grid[nx][ny]!=-1):
                    self.x,self.y = nx,ny
                    print(f"Moved to {self.x},{self.y}")
                    return
        
        print("No valid movement!")


agent = agent(0,0)

for step in range(10):
    print(f"Step at {step+1} agent is at {agent.x},{agent.y}")
    agent.action(grid)