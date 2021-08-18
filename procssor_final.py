import matplotlib.pyplot as plt
import random
import time
from graphics import *
from time import sleep
import draw_graph as dg
import tkinter
from tkinter.filedialog import askopenfilename

all_stacks = []
file_path = ''
root = tkinter.Tk()

def file_path_finder():
    global root
    global file_path
    file_path = askopenfilename(filetypes = (("Text file" , "*.txt") , ("All Files" , "*.*")))
    root.quit()
    root.destroy()

def tkinter_win():
    global root
    tkwin_t = tkinter.Label(root,text='Please Choose the test case path',font=('mitra', 15 , 'bold')).pack()
    
    btn = tkinter.Button(root,text='Open File',command=file_path_finder,width=50,height=10,font=10,bd=10)
    btn.pack()
    tkinter.mainloop()

def get_inputs(file_path):
    test_case = open('{}'.format(file_path),"r")

    graph = []
    # print('inputs: ')
    c = 0
    for l in test_case.readlines():
        if c==0:
            task_number = int(l)

        elif c== task_number + 1:
            tasks_size = l.split()

        elif c== task_number + 2:
            processor_number = int(l)
        
        elif c == task_number + 3:
            processors = l.split()

        else:
            graph.append(l.split())        
        c+=1

    # print('task_number:',task_number)
    # print(graph)
    # print('task_size: ', tasks_size)
    # print('processor_number: ', processor_number)
    # print('processors: ', processors)

    return task_number , graph , tasks_size , processor_number , processors

class graph():
    # set the self.graph to a dictionary.
    def __init__(self, task_number):
        self.graph = {}
        for i in range(task_number):
            self.graph[i+1] = []


    # create a function to add node'to the graph
    def addnode(self,u,v):

        self.graph[u].append(v)        


    def get_graph(self):
        return self.graph

    #  funcion to print the graph.
    def print_graph(self):
        print(self.graph)
        for node in self.graph:
            print(node,'-->',self.graph[node])
    
    # the main function to this programm that will
    # visit all the node's(you read tent's) and 
    # find their maximum size of soldier in them.

    def topologicalSort(self, tasks):
        def dfs(sorted_tasks, visited, start):
            visited[start - 1] = True

            for v in self.graph[start]:
                if visited[v - 1] == False:
                    dfs(sorted_tasks, visited, v)

            sorted_tasks.insert(0, tasks[start-1])

        sorted_tasks = []

        visited = [False] * len(self.graph)
        for v in self.graph:
            if visited[v - 1] == False:
                dfs(sorted_tasks, visited, v)

        return sorted_tasks

def draw_graph_func(task_number, arr_for_draw_graph, best_topo):
    nodes_name = [i for i in range(1,task_number+1)]
    print(arr_for_draw_graph)

    G = dg.draw_graph(nodes_name)
    G.creat_points()
    G.creat_circles()
    G.creat_lines(arr_for_draw_graph)
    G.draw_graph()

    for a in best_topo:
        sleep(1)
        G.change_circle_colore(a,'blue')

def to_processors(T_sort, task_size, processors,goten_graph):
    
    processor_ft = [0 for i in range(len(processors))]
    # print('processor_ft:',processor_ft)
    
    tasks_finish_time = [0 for i in range(1, len(task_size)+1)]

    tasks_start_time = [0 for i in range(1, len(task_size)+1)]


    processor_graph = {}
    for i in range(len(processors)):
        processor_graph[i] = []

    for t in range(len(T_sort)):
        # print("task #{}".format(T_sort[t]))
        max_dep_ft = 0
        dep_nodes = []
        least_Pfinish_time = float('inf')
        least_Pstart_time = float('inf')

        for i in goten_graph:
            for j in goten_graph[i]:
                if T_sort[t] == j:
                    dep_nodes.append(i) 
                    # print(T_sort[t] ,'dep -->', i)
            

        # print('dep nodes: ', dep_nodes )

        for i in dep_nodes:
            max_dep_ft_raw =  tasks_finish_time[i-1]
            # print('\nmax_dep_ft_raw: ',max_dep_ft_raw)
            if max_dep_ft_raw > max_dep_ft:
                max_dep_ft = max_dep_ft_raw
            

        # print("\nmax dep ft: ", max_dep_ft)
        # print()
        for p in range(len(processors)):
            
            current_task_size = float(task_size[T_sort[t]-1])

            current_processor_power = float(processors[p])
            
            
            least_Pstart_time_raw = max(processor_ft [p], max_dep_ft)

            least_Pfinish_time_raw =  current_task_size / current_processor_power + least_Pstart_time_raw


            if least_Pfinish_time_raw <= least_Pfinish_time and least_Pstart_time_raw <= least_Pstart_time :
                least_Pstart_time = least_Pstart_time_raw
                least_Pfinish_time = least_Pfinish_time_raw
                selected_processor = p
                # least_task_start_time = max(processor_ft[p] , max_dep_ft)
        
        # print('least_Pfinish_time : ', least_Pfinish_time)
        # print('task {} to  #{}'.format(T_sort[t],selected_processor))
        processor_graph[selected_processor].append(T_sort[t])
        tasks_finish_time[T_sort[t]-1] = least_Pfinish_time
        tasks_start_time[T_sort[t]-1] = least_Pstart_time

        processor_ft[selected_processor] = least_Pfinish_time
        
    # print('finish time: ',tasks_finish_time)
    # print('\nprocessors_finish time:',processor_ft) 

    # # print()
    # for i in processor_graph:
    #     # print("processor #{} :".format(i), processor_graph[i])
    #     pass
    
    ans_graph = {}
    for i in range(len(T_sort)):
        for p in processor_graph:
            for task in processor_graph[p]:
                if task == i+1:
                    # print("process #{} is in processor #{} ".format(i+1,p))
                    task_processor = p
                    # print(task_processor)
                    break

        ans_graph[i+1] = [task_processor,tasks_start_time[i],tasks_finish_time[i]]
        # print('start time of task #{} : '.format(i+1) , tasks_start_time[i])
        # print('finish time of task #{} : '.format(i+1), tasks_finish_time[i])
        # print("-"*10)


    # print('final answer is: \n')
    # print(ans_graph)

    # for i in processor_ft
    max_makespan = max(processor_ft)    
    # print(processor_ft)
    print('max makespan: ',max_makespan)
    
    return max_makespan , ans_graph , processor_graph

    # print('put {} in processor ?'.format(T_sort[t]))


def allTopologicalSorts(graph):
    visited = [False] * len(graph)

    indegree = [0] * len(graph)

    for i in graph:
        for j in graph[i]:
            indegree[j - 1] += 1
    
    stack = []

    allTopologicalSortsUtil(graph, visited, indegree, stack)


def allTopologicalSortsUtil(graph, visited, indegree, stack):
    flag = False

    for i in graph:
        if visited[i - 1] == False and indegree[i - 1] == 0:
            visited[i - 1] = True
            stack.append(i)
            for j in graph[i]:
                indegree[j - 1] -= 1
            allTopologicalSortsUtil(graph, visited, indegree, stack)

            visited[i - 1] = False
            stack.pop()
            for j in graph[i]:
                indegree[j - 1] += 1
            
            flag = True
    
    if flag == False:
        all_stacks.append(stack.copy())
        print(stack)


def draw_graph(processor_num,ans,max_makespan):
    # processor_num = 3

    # max_makespan = 19.7

    # ans = [[2, 0, 1.3333333333333333],
    # [1, 10.0, 14.0],
    # [2, 14.333333333333334, 17.333333333333336],
    # [1, 0, 6.666666666666667],
    # [2, 1.3333333333333333, 14.333333333333334],
    # [0, 1.3333333333333333, 10.933333333333334],
    # [1, 6.666666666666667, 10.0],
    # [2, 17.333333333333336, 19.733333333333334],
    # [0, 10.933333333333334, 16.933333333333334],
    # [1, 14.333333333333334, 17.333333333333336]]

    fig, ax = plt.subplots()

    colores = ['blue','red','green']


    # ax.broken_barh(  [(11, 2), (15, 4)]  , (10, 8), facecolors='tab:blue')
    # ax.broken_barh([(1, 5), (10, 2), (13, 1)], (20, 8), facecolors=('tab:orange', 'tab:green', 'tab:red'))
    # ax.broken_barh(  [(11, 2), (15, 4)]  , (30, 8), facecolors='tab:blue')

    ax.set_ylim(5, (15*processor_num))
    ax.set_xlim(0, max_makespan)

    ax.set_xlabel('Time')

    yticks = []
    yticks_label = []
    for y in range(1,processor_num+1):
        yticks.append(y*10+2.5)
        yticks_label.append('processor #{}'.format(y-1))

    ax.set_yticks(yticks)

    ax.set_yticklabels(yticks_label)

    ax.grid(True)

    for a in ans:
        bar = [(a[1],a[2]-a[1])]
        col = colores.pop()
        colores.insert(0,col)
        ax.broken_barh(bar , ((a[0]+1)*10,5),facecolors='tab:{}'.format(col))

    plt.show()


def draw_porocessor_sc(processor_number, max_makespan, task_sc, best_topo):
    # best_topo = [1, 4, 5, 6, 7, 2, 3, 9, 10, 8]
    # task_sc = [[2, 0, 1.3333333333333333], [1, 0, 6.666666666666667], [2, 1.3333333333333333, 14.333333333333334], [0, 1.3333333333333333, 10.933333333333334], [1, 6.666666666666667, 10.0], [1, 10.0, 14.0], [2, 14.333333333333334, 17.333333333333336], [0, 10.933333333333334, 16.933333333333334], [1, 14.333333333333334, 17.333333333333336], [2, 17.333333333333336, 19.733333333333334]]
    # processor_number = 3
    # max_makespan = 20

    win = GraphWin('Answer Barh',1000,600)

    # start points
    x_0 = Point(150,500)
    x_max = Point(900,500)
    x_size = int(x_max.getX() - x_0.getX())
    print('x_size: ',x_size)
    
    y_0 = Point(150,20)
    y_max = Point(150,500)
    y_size = int(y_max.getY() - y_0.getY())

    # barh lines
    x_barh = Line(x_0, x_max)
    x_barh.setArrow('last')
    y_barh = Line(y_max,y_0)
    y_barh.setArrow('last')


    processor_y =  [0 for i in range(processor_number)]


    # find and draw porcessors Y
    for i in range(processor_number):    
        processor_y[i] = (y_size / (processor_number+1)) * (i+1)
        p1 = Point(150,processor_y[i])
        p2 = Point(145,processor_y[i])
        l = Line(p1,p2).draw(win)
        t = Text(Point(60 ,processor_y[i]),'Processor #{}'.format(i))
        t.draw(win)

    # segmenting X Line
    barh_segment_number = 10
    for i in range(barh_segment_number):
        x = ( ( x_size) / barh_segment_number) * (i+1) + x_0.getX()
        p1 = Point(x,500)
        p2 = Point(x,510)
        l = Line(p1,p2)
        t = Text(Point(x,530),str(int((max_makespan / barh_segment_number) * (i+1))))
        l.draw(win)
        t.draw(win)    


    x_barh.draw(win)
    y_barh.draw(win)


    # draw tasks in graph
    counter = 0
    for task in task_sc:
        sleep(0.8)
        p1 = Point((task[1]*(x_size/max_makespan))+x_0.getX(),  processor_y[int(task[0])])
        p2 = Point(((task[2])*(x_size/max_makespan))+x_0.getX(),  processor_y[int(task[0])])
        l = Line(p1,p2)
        l.setWidth(20)
        l.setFill('grey')
        l.draw(win)
        


        t = Text(l.getCenter(),'T #{}'.format(best_topo[counter]))
        t.draw(win)

        lf1 = Line(p2 , Point( (task[2]*(x_size/max_makespan))+x_0.getX(),processor_y[int(task[0])]-10 ) )
        lf1.setFill('blue')
        lf1.setWidth(5)
        lf2 = Line(p2 , Point( (task[2]*(x_size/max_makespan))+x_0.getX(),processor_y[int(task[0])]+10 ) )
        lf2.setFill('blue')
        lf2.setWidth(5)

        lf1.draw(win)
        lf2.draw(win)


        counter += 1
    makespan_t = Text(Point(450,10),'max_makespan: '+ str(max_makespan))
    makespan_t.draw(win)
    exit_t = Text(Point(900,10),'Click To Exit...')
    exit_t.draw(win)
    win.getMouse()



tkinter_win()


task_number , dep_graph , tasks_size , processor_number , processors = get_inputs(file_path)


G = graph(task_number)


arr_for_draw_graph = []
# convert 2D matrix to graph
for r in range(len(dep_graph)):
    for c in range(len(dep_graph[r])):
        if dep_graph[r][c]== '1':
            arr_for_draw_graph.append([r+1,c+1,''])
            G.addnode(r+1,c+1)
            

goten_graph = G.get_graph()

# print("the given graph: ")
G.print_graph()

tasks = [i for i in range(1,task_number+1)]

allTopologicalSorts(goten_graph)

# print(all_stacks)
min_makespan = 1000
all_max_makespan = []

for stack in all_stacks:
    # print(stack)
    min_makespan_raw , task_sc_raw , processor_graph_raw = to_processors(stack,tasks_size,processors,goten_graph)
    print(min_makespan_raw)
    if min_makespan > min_makespan_raw:
        min_makespan = min_makespan_raw
        processor_graph = processor_graph_raw
        task_sc = task_sc_raw
        best_topo = stack

print('best_topo: ', best_topo)

print('tasks schedules: ')
task_sc_for_graph = []
for i in task_sc:
    print('task #{}'.format(i), end=" : ")
    print(task_sc[i])
    task_sc_for_graph.append(task_sc[i])

# # print("*************", task_sc_for_graph)
# print('\nProcessor schedule: ')
# print(processor_graph)

# print('\nmax makespan: ')
# print(min_makespan)


task_sc_for_my_garph = []
for t in best_topo:
    task_sc_for_my_garph.append(task_sc_for_graph[t-1])


# draw_graph(processor_number,task_sc_for_graph,min_makespan)

draw_graph_func(task_number,arr_for_draw_graph,best_topo)

draw_porocessor_sc(processor_number,min_makespan,task_sc_for_my_garph,best_topo)





# print(task_sc_for_my_garph)
# print(min(all_max_makespan))

# input()
print("\n\nit's topological sort: ")
T_sort = G.topologicalSort(tasks)
print(to_processors(T_sort,tasks_size,processors,goten_graph))
print(T_sort)
# print()
