import json
import math
# from drawer import Drawer
# drawer = Drawer()

def length(u):
    return (u[0]**2 + u[1]**2)**0.5

def angle(u, v):
    scalar = u[0] * v[0] + u[1] * v[1]
    l = length(u) * length(v)
    if l==0:
        return 0
    return math.acos(scalar / l)

def dist(p1, p2):
    return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )**0.5

def add(p1, p2):
    return ( p1[0]+p2[0], p1[1]+p2[1] )

def sub(p1, p2):
    return ( p1[0]-p2[0], p1[1]-p2[1] )

p_size = 50

class Unit():
    def __init__(self, obj):
        self.pos = (obj.get('X'), obj.get('Y'))
        self.radius = obj.get('R')
        self.mass = obj.get('M')

class Player():
    def __init__(self, mine = None):
        if mine:
            self.pos = (mine.get('X'), mine.get('Y'))
            self.speed = (mine.get('SX'), mine.get('SY'))
            self.radius = mine.get('R')
            self.mass = mine.get('M')

class Strategy:
    def run(self):
        config = json.loads(input())
        step = 4
        self.w, self.h =  config.get('GAME_WIDTH'), config.get('GAME_HEIGHT')

        #drawer.init(self.w, self.h, config.get('VIRUS_RADIUS'))

        self.me = Player()
        self.path = [
            (self.w/step, self.h/step),
            (self.w/step * (step-1), self.h/step),
            (self.w/step * (step-1) , self.h/step * (step-1)),
            (self.w/step, self.h/step* (step-1)),   
            (self.w/step * (step-1), self.h/step),
            (self.w/step, self.h/step),
            (self.w/step * (step-1) , self.h/step * (step-1)),
            (self.w/step, self.h/step* (step-1)),   
        ]

        self.corners = [
            (0, self.h),
            (self.w, self.h),
            (self.w, 0),
            (0,0)
        ]

        self.target = None
        while True:
            data = json.loads(input())
            cmd = self.on_tick(data, config)
            print(json.dumps(cmd))

    def food_is_availible(self, obj):
        pos = (obj.get('X'), obj.get('Y'))
        return pos[0] > 50 and pos[0] < self.w - 50 and pos[1] >50 and pos[1] < self.h - 50

    def parse(self, objects):
        f, e, v = [], [], []
        for obj in objects:
            t = obj.get('T')
            if t == 'F':
                if self.food_is_availible(obj):
                    f.append(Unit(obj))
            if t == 'V':
                v.append(Unit(obj))
            if t == 'P':
                e.append(Unit(obj))
        return f, e, v

    # def save(self, data):
    #     with open('data.txt', 'w') as d:
    #         json.dump(data, d)
            
    def on_tick(self, data, config):
      #  try:
            mine, objects = data.get('Mine'), data.get('Objects')
            
            if mine:
                players = []
                for fragment in mine:
                    players.append(Player(fragment))
                
                foods, enemies, viruses = self.parse(objects)     
                self.me = None
                enemy = None
                danger_enemies = []

                if len(players)==0:
                    return
                self.me = max(players, key = lambda p: p.mass)

                if len(enemies)>0:
                    danger = []
                    for e in enemies:
                        if e.mass / self.me.mass >= 1.19:
                            danger.append(e)
                    e = min(danger, default=None, key = lambda d: dist(d.pos, self.me.pos))
                    if e:
                        min_value = 99999
                        escape_point = (self.w/2, self.h/2)
                        r = int(self.me.radius)
                        for x in range(-r, r, r):
                            for y in range(-r, r, r):
                                if x==0 and y==0:
                                    continue
                                point = add((x,y), self.me.pos)                                
                                value = (min( (dist(corner, point) for corner in self.corners) )  + dist(e.pos, point)
                                if value< min_value:
                                    escape_point = point
                                    min_value = value
                        return {'X': int( escape_point[0] ), 'Y': int(  escape_point[1]), 'Debug': 'escape to '+str(escape_point)} 
                        

                # if len(danger_enemies)>0:
                #     r = self.me.radius*1.5
                #     cells = dict()
                #     max_min_dist = 0
                #     escape_point = ()
                #     alfa =0
                #     while alfa<=math.pi*2:
                #         x = self.me.pos[0]+r*math.cos(alfa)
                #         y = self.me.pos[1]+ r*math.sin(alfa)

                #         drawer.add(x,y, 5)
                #         min_dist = dist(min(danger_enemies, key=lambda e: dist(e.pos, (x,y))).pos, (x,y))
                #         if min_dist>max_min_dist:
                #             escape_point = (x,y)
                #             max_min_dist = min_dist
                #         alfa+=math.pi/4   
                #     return {'X':escape_point[0], 'Y':escape_point[1]}

                e = min(enemies, default =None, key=lambda e:  dist(e.pos, self.me.pos))
                if e:
                    if self.me.mass / e.mass > 1.25:
                        if (self.me.mass/2) / e.mass > 1.25:
                            if angle(sub(e.pos, self.me.pos), self.me.speed) < 0.2:
                                return {'X': e.pos[0], 'Y': e.pos[1], "Split": True}                
                        return {'X': e.pos[0], 'Y': e.pos[1]}  

                food = min(foods, default =None, key=lambda f: dist(self.me.pos, f.pos))
                if food:
                    return {'X': food.pos[0], 'Y':food.pos[1]}

                # v = min(viruses, default =None, key=lambda o: o.sdist)
                # if v:
                #     return {'X': self.me.pos[0]*2- v.pos[0], 'Y':  self.me.pos[1]*2 - v.pos[1]}         
                
                if not self.target:
                    self.target = min(self.path, key = lambda p: dist(p, self.me.pos))
                    self.index = self.path.index(self.target)
                else:
                    if (self.target[0]-p_size < self.me.pos[0] <  self.target[0]+p_size) and (self.target[1]-p_size < self.me.pos[1] <  self.target[1]+p_size):
                        self.index+=1
                        if self.index>len(self.path)-1: 
                            self.index = 0
                        self.target = self.path[self.index]                            
                    
                    return {'X': self.target[0], 'Y': self.target[1]}
            return {'X': 300, 'Y': 300}
        # except Exception as inst:
        #     with open("Output.txt", "w") as text_file:
        #         print(inst.args, file=text_file)
            
            #json.dump(data, d)


if __name__ == '__main__':
    Strategy().run()
