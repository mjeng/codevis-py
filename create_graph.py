
import networkx as nx
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import sys
import parse_file

'''
    input: connections = list of CallData objects
'''

def draw(connections):
    im_size = 1000
    g = nx.DiGraph()        # directed graph with self-loops
    num_nodes = len(connections)
    files = {}
    locations = {}
    stretch = {}
    nodes = [f.func_name for f in connections]
    font = ImageFont.truetype("arial.ttf", size=12)

    im = Image.new('RGB', (im_size, im_size), color="white")
    draw = ImageDraw.Draw(im)

    for i in range(len(connections)):
        if (connections[i].src_file in files):
            files[connections[i].src_file].append(connections[i].func_name)
        else:
            files[connections[i].src_file] = [connections[i].func_name]

    file_list = list(files.keys())
    x_spacing = {}
    for file in file_list:
        if (len(files[file]) == 0):
            x_spacing[file] = [500]
        else:
            x_spacing[file] = list(range(100, im_size - 100, int( (im_size - 200) / (len(files[file]) - 1))))
        x_spacing[file].append(im_size - 100)
    y_spacing = list(range(100, im_size - 100, int( (im_size - 200) / len(file_list))))

    # draw file divisions
    for i in range(len(y_spacing) - 1):
        chunk_mid = (y_spacing[i] + y_spacing[i + 1]) / 2
        for j in range(1000):
            if (j % 10 < 5):
               draw.point((j, chunk_mid), fill="blue")
    # get locations of nodes in (x, y) coordinates spread out across image
    for i in range(len(nodes)):
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
    # draw the nodes after drawing edges
    for i in range(len(nodes)):
        node = locations[connections[i].func_name]
        stretch[connections[i].func_name] = draw_circle(draw, node[0], node[1], 30, connections[i].func_name, connections[i].times_called, font)
    # draw the arrows on the edges
    for i in range(len(nodes)):
        for dest in connections[i].call_list:
            start = connections[i].func_name
            draw_arrow(draw, locations[dest][0], locations[dest][1], locations[start][0], locations[start][1], 35 + stretch[connections[i].func_name])
    #draw.arc((20, 40, 100, 500), 90, 270, 'black')
    nx.draw(g, with_labels=True, pos=locations, node_size=700)
    # plt.show()
    del draw
    im.save("test.png", format="PNG")

def draw_circle(im, x, y, rad, label, times_called, font):
    stretch = len(label) * 1.2
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
        # im.rectangle((x_1 - 70, y_1 - 30, x_1 - 30, y_2 + 30), outline="black")
    elif (x_1 == x_2):
        # same column
        im.arc((x_1 - 80, min(y_1 - 5, y_2 + 5), x_1, max(y_1 - 5, y_2 + 5)), 80, 280, 'black')
        #im.rectangle((x_1 - 70, y_1, x_1, y_2), outline="black")
    elif (y_1 == y_2):
        # same row
        im.arc((min(x_1, x_2) + 5, y_2 - 60, max(x_1, x_2) + 5, y_2), 180, 0, 'black')
        # im.rectangle((x_1, y_1 - 10, x_2, y_2 - 60), outline="black")
    else:
        im.line(((x_1, y_1), (x_2, y_2)), fill="black", width=2)

def draw_arrow(im, x_1, y_1, x_2, y_2, r):
    if ((x_1 == x_2) and (y_1 == y_2)):
        return
    dist = ((x_1 - x_2)**2 + (y_1 - y_2)**2)**.5
    x_a = x_1 - (r * (x_1 - x_2) / dist)
    y_a = y_1 - (r * (y_1 - y_2) / dist)
    im.ellipse((x_a - 5, y_a - 5, x_a + 5, y_a + 5), fill=(0, 0, 0))


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
