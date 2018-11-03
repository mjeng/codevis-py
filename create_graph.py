
import networkx as nx
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import sys

'''
    input: dictionary connections
        key = function name
        values = set of names of functions that it calls
'''
def draw(connections):
    im_size = 1000
    g = nx.DiGraph()        # directed graph with self-loops
    g.add_nodes_from(connections.keys())

    for key in connections:
        edges = [(key, dest) for dest in connections[key]]
        g.add_edges_from(edges)

    im = Image.new('RGB', (im_size, im_size), color="white")
    draw = ImageDraw.Draw(im)
    num_nodes = len(connections.keys())
    x_spacing = range(50, im_size - 50, int((im_size - 100) / (num_nodes - 1)) )
    x_spacing = list(x_spacing)
    x_spacing.append(im_size - 50)
    keys = list(connections.keys())
    for i in range(len(keys)):
        draw_circle(draw, x_spacing[i], 50, 30, keys[i])


    del draw
    im.save("test.png", format="PNG")

def draw_circle(im, x, y, rad, label):
    im.ellipse((x - rad - 1, y - rad - 1, x + rad + 1, y + rad + 1), fill=(0, 0, 0))
    im.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(255, 255, 255))
    im.text((x - rad + 5, y - rad + 5), label, font=ImageFont.load_default(), fill="black")

def draw_edge(im, x_1, y_1, x_2, y_2):
    im.line(((x_1, y_1), (x_2, y_2)), fill="black", width=1)
    # im.polygon( ((x_2 - 3, find_y(perp_slope, x_2, x_2 - 3, y_2)), (x_2 + 3, find_y(perp_slope, x_2, x_2 + 3, y_2)), (find_x(slope, x_2 - 3, ))),

def draw_arrow(im, x_1, y_1, x_2, y_2):
    slope = (y_2 - y_1) / (x_2 - x_1)
    perp_slope = (-1) / slope
    point = ()

def find_y(slope, x_1, x_2, y_1):
    return slope * (x_2 - x_1) + y_2

def find_x(slope, x_1, y_1, y_2):
    return ((y_2 - y_1) / m) + x_1


def main():
    test = {}
    test["one"] = set(["two", "three", "five"])
    test["two"] = set(["two", "one"])
    test["three"] = set()
    test["four"] = set(["one"])
    test["five"] = set(["one"])
    draw(test)

if __name__ == "__main__":
    main()