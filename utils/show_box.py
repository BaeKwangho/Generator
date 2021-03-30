import matplotlib.patches as patches
import matplotlib.pyplot as plt
import PIL.Image as Image

def show_box(output_path, sentences):
    palette = Image.open(output_path)
    
    def calc_point(points,pad=0):
        box = points['box']
        if pad:
            diff_x = box['x2']-box['x1']+pad*2
            diff_y = box['y2']-box['y1']+pad*2
        else:
            diff_x = box['x2']-box['x1']
            diff_y = box['y2']-box['y1']
        point = [box['x1'],box['y1']]
        return diff_x, diff_y, point


    fig, ax = plt.subplots(figsize=(30,30))
    ax.imshow(palette)
    for i in sentences:
        diff_x,diff_y,point = calc_point(i,1)
        bounding_box = patches.Rectangle(point,diff_x,diff_y,facecolor='none', linewidth=1, edgecolor='g')
        ax.add_patch(bounding_box)
        for j in i['words']:
            diff_x,diff_y,point = calc_point(j)
            bounding_box = patches.Rectangle(point,diff_x,diff_y,facecolor='none', linewidth=1, edgecolor='r')
            ax.add_patch(bounding_box)
    plt.show()