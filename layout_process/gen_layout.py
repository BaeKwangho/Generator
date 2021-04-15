# -*- coding: utf-8 -*-
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
    split_x = np.random.randint(2) + 1
    split_ys = [np.random.randint(4) + 1 for _ in range(split_x)]
    
    layout_x = []
    layout_y = []

    x_ = 0
    y_ = []
    for i in range(split_x):
        x = np.random.randint(3) + 3 # 3~5
        layout_x.append(x)
        x_ += x

        xth_ys = []
        y_t = 0
        for _ in range(split_ys[i]):
            y = np.random.randint(5) + 1 # 1~5
            xth_ys.append(y)
            y_t += y

        layout_y.append(xth_ys)
        y_.append(y_t)

    for i,xs in enumerate(layout_x):
        layout_x[i] = np.round_(xs / x_, 2)

    for i,yc in enumerate(layout_y):
        for j,ys in enumerate(yc):
            layout_y[i][j] = np.round_(ys / y_[i], 2)

    layout_x, layout_y = drop_ratio(layout_x, layout_y)
    
    return layout_x, layout_y


def assign_layout(layout_x, layout_y,pad_x=30,pad_y=40):
    #Assign Layout

    pad_x = np.random.randint(10) + pad_x
    pad_y = np.random.randint(10) + pad_y

    pad = {'x':pad_x,'y':pad_y}
    paper = {'x':1500,'y':2400}
    margin = {"up":0.25, "side":0.2, "down":0.1}

    margin_area = {"x":int(paper["x"]*(1-margin["side"])), "y":int(paper["y"]*(1-(margin["up"]+margin["down"])))}
    margin_start_x = int(paper["x"] * margin["side"]/2)
    margin_start_y = int(paper["y"] * margin["up"])
    
    abs_x = [int(margin_area['x']*i) for i in layout_x] # 문서 크기를 비율로 나누기
    stack = 0
    stack_x = []
    for i in abs_x:
        start_x = margin_start_x + stack + pad['x'] # 문단 시작 x
        stack += i
        end_x = margin_start_x + stack - pad['x'] # 문단 끝 x
        stack_x.append([start_x, end_x])

    abs_y = [[int(margin_area['y']*j) for j in i]for i in layout_y]
    stack_y = []
    for i in abs_y:
        stack = 0
        stack_y_temp = []
        for j in i:
            start_y = margin_start_y + stack + pad['y']
            stack += j
            end_y = margin_start_y + stack - pad['y']
            stack_y_temp.append([start_y, end_y])
        stack_y.append(stack_y_temp)

    rects = []
    for i,xs in enumerate(stack_x):
        for ys in stack_y[i]:
            rects.append({'x1':xs[0],'x2':xs[1],'y1':ys[0],'y2':ys[1]})

    ## 제목은 랜덤
    isTitle = np.random.randint(5) # 타이틀 확률 랜덤 값 확률은 5분의 1!
    if(isTitle == 3):
        # title_area : 제목이 포함될 영역(제목 영역 아님)
        title_area_w = margin_area["x"]
        title_area_h = margin_start_y
        title_area_start_ = margin_start_x

        # title : 제목 영역
        title_w = np.random.randint(title_area_w // 3) + title_area_w // 3
        title_h = np.random.randint(10) + 50

        # 제목 좌표
        title_start_x = title_area_start_ + int((title_area_w - title_w) / 2)
        title_start_y = int((title_area_h - title_h) / 2)
        title_end_x = title_start_x + title_w
        title_end_y = title_start_y + title_h

        title = {"x1" : title_start_x, "x2" : title_end_x, "y1" : title_start_y, "y2" : title_end_y}
    else:
        title = None
        
    return rects, title

def gen_layout(pad_x=30, pad_y=40):
    layout_x, layout_y = generate_ratio()
    rects, title = assign_layout(layout_x, layout_y, pad_x, pad_y)
    
    return rects, title
