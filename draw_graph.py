from time import sleep
from graphics import *

class draw_graph():
    def __init__(self,s_names):
        self.count = 0 
        self.s_names = s_names
        for s in self.s_names:
            self.count += 1

        # count of column and row of points
        
        # self.circles_space = 50
        if self.count <= 10:
            self.row = 2
            self.column = 5
            self.radius = 30
            self.circles_space = 150

        elif self.count > 10 and self.count <= 20:
            self.row = 2
            self.column = 10
            self.radius = 20
            self.circles_space = 100

        
        elif self.count > 20 and self.count <= 30:
            self.row = 3
            self.column = 15
            self.radius = 15
            self.circles_space = 80
        else:
            self.row = 4
            self.column = 20
            self.radius = 10
            self.circles_space = 50



        # s is the start point of each row.
        self.s = 0

        # offset is the frequenci of point in each line.
        self.offset = 1

        # flag is sying that if we are adding 1 or 3 ; True
        self.flag = True

        self.points = []
        self.win = GraphWin('first graphic', 1200, 600)
        self.circles = {}
        self.lines = {}

    def creat_points(self):
        for j in range(self.row):
            x = 0
            y = self.s

            temp_offset = self.offset
            
            for i in range(self.column):
                self.points.append(Point(((x*self.circles_space)+50),((y*self.circles_space)+50)))
                # print("[{},{}]".format(x,y))
                x += 1
                y += temp_offset
                temp_offset = -(temp_offset)
            
            if self.flag == True:
                self.s += 3
            else:
                self.s += 1

            x = 0
            
            # print("="*20)
            
            self.flag = not self.flag
            # print(self.flag)

            self.offset = -(self.offset)
            # print(self.offset)
            # print(self.points)


    def creat_circles(self):
        counter = 0
        for p in self.points:
            c = Circle(p,self.radius)
            cname = self.s_names[counter]

            cc = c.getCenter()
            ct = Text(cc, cname)
            ct.setSize(20)
            # ct.setTextColor('green')
            self.circles[cname] = c , ct
            counter += 1

            if counter == self.count:
                break

        # for c in self.circles:
        #     print(c,end=" : ")
        #     print(self.circles[c])

    def get_circles(self):
        return self.circles

    def creat_lines(self,lines):
        for l in lines:
            # print(l)
            lname = 'L'+str(l[0])+','+str(l[1])
            p1 = self.circles[l[0]][0].getCenter()
            p2 = self.circles[l[1]][0].getCenter()
            line = Line(p1,p2)
            
            lc = line.getCenter()
            t = l[2]
            lt = Text(lc, t)
            lt.setSize(20)
            lt.setTextColor('red')
            line.setWidth('2')
            self.lines[lname] = line , lt

        # for l in self.lines:
            # print(self.lines[l])



    def draw_graph(self):
        for c in self.circles:
            self.circles[c][0].draw(self.win)
            self.circles[c][1].draw(self.win)
            

        for l in self.lines:
            self.lines[l][0].setArrow('last')
            self.lines[l][0].draw(self.win)
            self.lines[l][1].draw(self.win)
            # sleep(0.5)
            # self.lines[l][0].undraw()
            # self.lines[l][1].undraw()



    def change_circle_colore(self,obj_name,color):
        self.circles[obj_name][0].setFill(color)


    def change_line_colore(self,obj_name,color):
        self.lines[obj_name][0].setFill(color)
        

# lines = [['q1', 'q3', 'a'], ['q1', 'q2', 'b'], ['q2', 'q3', 'b']]
# states_names =  ['q1', 'q3', 'q2']

# task_number = 10
# s_names = [i for i in range(1,task_number+1)]
# lines = [[1, 2, ''], [1, 5, ''], [1, 6, ''], [1, 7, ''], [2, 3, ''], [3, 8, ''], [4, 7, ''], [5, 3, ''], [5, 10, ''], [6, 3, ''], [6, 10, ''], [7, 9, ''], [10, 8, '']]
# best_topo_sort = [1, 4, 5, 6, 7, 2, 3, 9, 10, 8]


# G = draw_graph(s_names)
# G.creat_points()
# G.creat_circles()
# G.creat_lines(lines)
# G.draw_graph()


# for a in best_topo_sort:
#     G.change_circle_colore(a,'blue')
#     sleep(1)

# input()



    