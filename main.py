import json
import math

def length(u):
    return (u[0]**2 + u[1]**2)**0.5

def angle(u, v):
    scalar = u[0] * v[0] + u[1] * v[1]
    return math.acos(scalar/ (length(u) * length(v)))

def dist(p1, p2):
    return ( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )**0.5

def add(p1, p2):
    return ( p1[0]+p2[0], p1[1]+p2[1] )

def sub(p1, p2):
    return ( p1[0]-p2[0], p1[1]-p2[1] )


p_size = 50

class Unit():
    def __init__(self, obj, mine):
        self.pos = (obj.get('X'), obj.get('Y'))
        self.sdist =  dist(add(mine.pos, mine.speed) , self.pos)
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
        self.me = Player()
        self.path = [
            (self.w/step, self.h/step),
            (self.w/step * (step-1), self.h/step),
            (self.w/step * (step-1) , self.h/step * (step-1)),
            (self.w/step, self.h/step* (step-1))
            ]

        self.target = None
        while True:
            data = json.loads(input())
            cmd = self.on_tick(data, config)
            print(json.dumps(cmd))

    def food_is_availible(self, obj):
        pos = (obj.get('X'), obj.get('Y'))
        return pos[0] > self.me.radius and pos[0] < self.w - self.me.radius and pos[1] > self.me.radius and pos[1] < self.h - self.me.radius

    def parse(self, objects):
        f, e, v = [], [], []
        for obj in objects:
            t = obj.get('T')
            if t == 'F':
                if self.food_is_availible(obj):
                    f.append(Unit(obj, self.me))
            if t == 'V':
                v.append(Unit(obj, self.me))
            if t == 'P':
                e.append(Unit(obj, self.me))
        return f, e, v

    # def save(self, data):
    #     with open('data.txt', 'w') as d:
    #         json.dump(data, d)
            
    def on_tick(self, data, config):
        mine, objects = data.get('Mine'), data.get('Objects')
        
        if mine:
            mine = mine[0]
            self.me = Player(mine)


            foods, enemies, viruses = self.parse(objects)
            
            e = min(enemies, default =None, key=lambda o: o.sdist)
            if e:
                if  self.me.mass / e.mass > 1.25:
                    if (self.me.mass/2) / e.mass > 1.25:
                        if angle(sub(e.pos, self.me.pos), self.me.speed) < 0.2:
                            return {'X': e.pos[0], 'Y': e.pos[1], "Split": True}                
                    return {'X': e.pos[0], 'Y': e.pos[1]}            
                else:
                    return {'X': self.me.pos[0]*2 - e.pos[0], 'Y':  self.me.pos[1]*2 - e.pos[1]} 

            f = min(foods, default =None, key=lambda o: o.sdist)
            if f:
                return {'X': f.pos[0], 'Y': f.pos[1]}

            # v = min(viruses, default =None, key=lambda o: o.sdist)
            # if v:
            #     return {'X': self.me.pos[0]*2- v.pos[0], 'Y':  self.me.pos[1]*2 - v.pos[1]}         

            if not self.target:
                self.target = min(self.path, key = lambda p: dist(p, self.me.pos))
            else:
                if (self.target[0]-p_size < self.me.pos[0] <  self.target[0]+p_size) and (self.target[1]-p_size < self.me.pos[1] <  self.target[1]+p_size):
                    index = self.path.index(self.target)
                    index+=1
                    if index>3: index = 0
                    self.target = self.path[index]                            
                
                return {'X': self.target[0], 'Y': self.target[1]}
        return {'X': 300, 'Y': 300}

if __name__ == '__main__':
    Strategy().run()