import numpy as np
import matplotlib.pyplot as plt

def drop_ratio(layout_x,layout_y,res_x=0.3, res_y=0.1):
    for i,xs in enumerate(layout_x):
        if xs < res_x:
            del layout_x[i]
            del layout_y[i]
    for i,temp in enumerate(layout_y):
        for j,ys in enumerate(temp):
            if ys < res_y:
                del layout_y[i][j]
    return layout_x,layout_y

def generate_ratio():
    #Generate ratio
    split_x = np.random.randint(3)+1
    split_y = np.random.randint(4)+1 

    max_ratio_x = (5*(1/split_x))
    max_ratio_y = (5*(1/split_y))

    layout_x = []
    layout_y = []

    x_ = 0
    y_ = []
    for i in range(split_x):
        x = np.random.randint(5)+1
        x = int(x*max_ratio_x)
        layout_x.append(x)
        x_ += x

        xth_ys = []
        y_t = 0
        for j in range(split_y):
            y = np.random.randint(5)+1
            y = int(y*max_ratio_y)
            xth_ys.append(y)
            y_t += y

        layout_y.append(xth_ys)
        y_.append(y_t)

    for i,xs in enumerate(layout_x):
        layout_x[i] = np.round_(xs/x_,2)

    for i,yc in enumerate(layout_y):
        for j,ys in enumerate(yc):
            layout_y[i][j] = np.round_(ys/y_[i],2)

    layout_x,layout_y = drop_ratio(layout_x,layout_y)
    
    return layout_x,layout_y


def assign_layout(layout_x, layout_y,pad_x=30,pad_y=40):
    #Assign Layout

    pad_x = np.random.randint(10)+pad_x
    pad_y = np.random.randint(10)+pad_y

    pad = {'x':pad_x,'y':pad_y}

    paper = {'x':1500,'y':2400}

    abs_x = [ int(paper['x']*i) for i in layout_x]
    stack = 0
    stack_x = []
    for i in abs_x:
        start_x = stack+pad['x']
        stack += i
        end_x = stack-pad['x']
        stack_x.append([start_x,end_x])

    abs_y = [[int(paper['y']*j) for j in i]for i in layout_y]
    stack_y = []
    for i in abs_y:
        stack = 0
        stack_y_temp = []
        for j in i:
            start_y = stack+pad['y']
            stack += j
            end_y = stack-pad['y']
            stack_y_temp.append([start_y,end_y])
        stack_y.append(stack_y_temp)

    rects = []
    for i,xs in enumerate(stack_x):
        for ys in stack_y[i]:
            rects.append({'x1':xs[0],'x2':xs[1],'y1':ys[0],'y2':ys[1]})

    return rects