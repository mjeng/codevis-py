
import networkx as nx
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import sys
import parse_file
import math

'''
    input: connections = list of CallData objects
'''

def draw(connections):
    g = nx.DiGraph()        # directed graph with self-loops
    num_nodes = len(connections)
    files = {}
    locations = {}
    stretch = {}
    nodes = [f.func_name for f in connections]
    font = ImageFont.truetype("arial.ttf", size=12)

    for i in range(len(connections)):
        if (connections[i].src_file in files):
            files[connections[i].src_file].append(connections[i].func_name)
        else:
            files[connections[i].src_file] = [connections[i].func_name]
    im_size = max(1000, len(files.keys()) * 100 , max([len(lst) for lst in files.values()]) * 80)

    im = Image.new('RGB', (im_size, im_size), color="white")
    draw = ImageDraw.Draw(im)

    file_list = list(files.keys())
    x_spacing = {}
    for file in file_list:
        if (len(files[file]) == 1):
            x_spacing[file] = [im_size / 2]
        else:
            x_spacing[file] = list(range(100, im_size - 100, int( (im_size - 200) / (len(files[file]) - 1))))
            x_spacing[file].append(im_size - 100)
    if (len(files) == 1):
        y_spacing = [im_size / 2]
    else:
        y_spacing = list(range(100, im_size - 100, int( (im_size - 200) / (len(file_list) - 1))))
        y_spacing.append(y_spacing[0])

    # draw file divisions and function names
    for i in range(len(y_spacing) - 1):
        chunk_mid = (y_spacing[i] + y_spacing[i + 1]) / 2
        for j in range(im_size):
            if (j % 10 < 5):
               draw.point((j, chunk_mid), fill="blue")
    draw.text((im_size - 100, im_size - 100), file_list[-1], font=font, fill="black")
    # get locations of nodes in (x, y) coordinates spread out across image
    for i in range(len(nodes)):
        stretch[connections[i].func_name] = len(connections[i].func_name) * 1.2
        node_index = files[connections[i].src_file].index(connections[i].func_name)
        node_x = x_spacing[connections[i].src_file][node_index]
        node_y = y_spacing[file_list.index(connections[i].src_file)]
        locations[connections[i].func_name] = (node_x, node_y)
        g.add_node(connections[i].func_name, pos=locations[connections[i].func_name])
    # add the edges to the drawing based on saved (x,y) of each function
    for i in range(len(nodes)):
        for dest in connections[i].call_list:
            start = connections[i].func_name
            draw_edge(draw, locations[start][0], locations[start][1], locations[dest][0], locations[dest][1])
            g.add_edge(start, dest)
    # draw the arrows on the edges
    for i in range(len(nodes)):
        for dest in connections[i].call_list:
            start = connections[i].func_name
            if ((locations[dest][0] == locations[start][0]) or (locations[dest][1] == locations[start][1])):
                draw_arrow_arc(draw, locations[dest][0], locations[dest][1], locations[start][0], locations[start][1])
            else:
                draw_arrow(draw, locations[dest][0], locations[dest][1], locations[start][0], locations[start][1], 35 + stretch[connections[i].func_name])
    # draw the nodes after drawing edges
    for i in range(len(nodes)):
        node = locations[connections[i].func_name]
        draw_circle(draw, node[0], node[1], 30, connections[i].func_name, connections[i].times_called, font, stretch[connections[i].func_name])

    for i in range(len(y_spacing) - 1):
        chunk_mid = (y_spacing[i] + y_spacing[i + 1]) / 2
        draw.text((im_size - 100, chunk_mid - 20), file_list[i], font=font, fill="black")
    #draw.arc((20, 40, 100, 500), 90, 270, 'black')
    nx.draw(g, with_labels=True, pos=locations, node_size=700)
    # plt.show()
    del draw
    # im.save("test.png", format="PNG")
    return im

def draw_circle(im, x, y, rad, label, times_called, font, stretch):
    im.ellipse((x - rad - stretch - 1, y - rad - 1, x + rad + stretch + 1, y + rad + 1), fill=(0, 0, 0))
    intensity = max(255 - (15 * times_called), 0)
    im.ellipse((x - rad - stretch, y - rad, x + rad + stretch, y + rad), fill=(intensity, intensity, 255))
    len(label)
    im.text((x - (len(label) * 2.75), y - 5), label, font=font, fill="black")
    return stretch

def draw_edge(im, x_1, y_1, x_2, y_2):
    if ((x_1 == x_2) and (y_1 == y_2)):
        # recursive self-loop
        im.arc((x_1 - 75, y_1 - 30, x_1 - 20, y_2 + 30), 30, 330, 'black')
        im.arc((x_1 - 74, y_1 - 30, x_1 - 19, y_2 + 30), 30, 330, 'black')
        #im.rectangle((x_1 - 75, y_1 - 30, x_1 - 20, y_2 + 30), outline="black")
    elif (x_1 == x_2):
        # same column
        im.arc((x_1 - 80, min(y_1, y_2) + 20, x_1 + 20, max(y_1, y_2) - 20), 90, 270, 'black')
        im.arc((x_1 - 79, min(y_1, y_2) + 20, x_1 + 19, max(y_1, y_2) - 20), 90, 270, 'black')
        #im.rectangle((x_1 - 80, min(y_1, y_2) + 20, x_1 + 20, max(y_1, y_2) - 20), outline="black")
    elif (y_1 == y_2):
        # same row
        im.arc((min(x_1, x_2) + 20, y_2 - 80, max(x_1, x_2) - 20, y_2 + 30), 180, 0, 'black')
        im.arc((min(x_1, x_2) + 20, y_2 - 79, max(x_1, x_2) - 20, y_2 + 29), 180, 0, 'black')
        # im.rectangle((x_1, y_1 - 10, x_2, y_2 - 60), outline="black")
    else:
        im.line(((x_1, y_1), (x_2, y_2)), fill="black", width=2)

def draw_arrow(im, x_1, y_1, x_2, y_2, r):
    if ((x_1 == x_2) and (y_1 == y_2)):
        return
    dist = ((x_1 - x_2)**2 + (y_1 - y_2)**2)**.5
    x_a = x_1 - (r * (x_1 - x_2) / dist)
    y_a = y_1 - (r * (y_1 - y_2) / dist)
    t = math.tan(math.pi/6)
    target = 150
    x_a1 = ((x_a-x_2)*math.cos(t) - (y_a-y_2)*math.sin(t))
    y_a1 = ((y_a-y_2)*math.cos(t) + (x_a-x_2)*math.sin(t))
    d1 = x_a1**2 + y_a1**2
    x_a2 = ((x_a-x_2)*math.cos(-t) - (y_a-y_2)*math.sin(-t))
    y_a2 = ((y_a-y_2)*math.cos(-t) + (x_a-x_2)*math.sin(-t))
    d2 = x_a2**2 + y_a2**2
    x_l = x_a - x_a1*((target/d1)**0.5)
    y_l = y_a - y_a1*((target/d1)**0.5)
    x_r = x_a - x_a2*((target/d2)**0.5)
    y_r = y_a - y_a2*((target/d2)**0.5)
    im.line(((x_l, y_l), (x_a, y_a)), fill="black", width=3)
    im.line(((x_r, y_r), (x_a, y_a)), fill="black", width=3)

def draw_arrow_arc(im, x_1, y_1, x_2, y_2):
    #same column, also includes recursive and should route to left side
    if (x_1 == x_2 and y_1 == y_2):
        draw_arrow(im, x_1 - 75, (y_1 + y_2)/2, x_1-75, y_2 + 30, 0)
    elif (x_1 == x_2):
        draw_arrow(im, x_1 - 80, (y_1 + y_2) / 2, x_1 - 80, max(y_1, y_2) - 20, 0)
    else:
        draw_arrow(im, (x_1 + x_2) / 2, y_2 - 80, max(x_1, x_2) - 20, y_2 - 80, 0)






def main():
    t1 = parse_file.CallData("one", "f1", ["one", "two", "four"], 10)
    t2 = parse_file.CallData("two", "f1", ["three", "four"], 7)
    t5 = parse_file.CallData("five", "f1", ["two"], 4)
    t3 = parse_file.CallData("three", "f2", ["one"], 2)
    t4 = parse_file.CallData("four", "f2", ["one"], 1)
    test = [t1, t2, t3, t4, t5]
    draw(test)

if __name__ == "__main__":
    main()
