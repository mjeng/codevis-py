
import networkx as nx
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import sys
from parse_file import CallData 

'''
    input: connections = list of CallData objects
'''

def draw(connections):
    im_size = 1000
    g = nx.DiGraph()        # directed graph with self-loops
    num_nodes = len(connections)
    files = {}
    locations = {}
    nodes = [f.func_name for f in connections]

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
        x_spacing[file] = list(range(50, im_size - 50, int( (im_size - 100) / (len(files[file]) - 1))))
        x_spacing[file].append(im_size - 100)
    y_spacing = list(range(50, im_size - 50, int( (im_size - 100) / len(file_list))))

    for i in range(len(nodes)):
        node_index = files[connections[i].src_file].index(connections[i].func_name)
        node_x = x_spacing[connections[i].src_file][node_index]
        node_y = y_spacing[file_list.index(connections[i].src_file)]
        locations[connections[i].func_name] = (node_x, node_y)
        g.add_node(connections[i].func_name, pos=locations[connections[i].func_name])

    for i in range(len(nodes)):
        for dest in connections[i].call_list:
            start = connections[i].func_name
            draw_edge(draw, locations[start][0], locations[start][1], locations[dest][0], locations[dest][1])
            g.add_edge(start, dest)
            if(start != dest):
                draw_arrow(draw, locations[dest][0], locations[dest][1], locations[start][0], locations[start][1])

    for i in range(len(nodes)):
        node = locations[connections[i].func_name]
        draw_circle(draw, node[0], node[1], 30, connections[i].func_name, connections[i].times_called)

    # edge_trace = go.Scatter(
    #     x=[],
    #     y=[],
    #     line=dict(width=0.5,color='#888'),
    #     hoverinfo='none',
    #     mode='lines'
    #     )

    # for edge in g.edges():
    #     x0, y0 = g.node[edge[0]]['pos']
    #     x1, y1 = g.node[edge[1]]['pos']
    #     edge_trace['x'] += tuple([x0, x1, None])
    #     edge_trace['y'] += tuple([y0, y1, None])

    # node_trace = go.Scatter(
    # x=[],
    # y=[],
    # text=[],
    # mode='markers',
    # hoverinfo='text',
    # marker=dict(
    #     showscale=True,
    #     colorscale='Earth',
    #     reversescale=True,
    #     color=[],
    #     size=10,
    #     colorbar=dict(
    #         thickness=15,
    #         title='Node Connections',
    #         xanchor='left',
    #         titleside='right'
    #     ),
    #     line=dict(width=2)))

    # for node in g.nodes():
    #     x, y = g.node[node]['pos']
    #     node_trace['x'] += tuple([x])
    #     node_trace['y'] += tuple([y])

    # fig = go.Figure(data=[edge_trace, node_trace],
    #     layout=go.Layout(
    #         title='<br>Network graph made with Python',
    #         titlefont=dict(size=16),
    #         showlegend=False,
    #         hovermode='closest',
    #         margin=dict(b=20,l=5,r=5,t=40),
    #         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    # plotly.offline.plot(fig, filename='networkx')

    nx.draw(g, with_labels=True, pos=locations, node_size=700)
    plt.show()
    del draw
    im.save("test.png", format="PNG")

def draw_circle(im, x, y, rad, label, times_called):
    if (times_called > 1):
        print("MANY TIMES")
        rad = rad * times_called
        print(rad, label)
    im.ellipse((x - rad - 1, y - rad - 1, x + rad + 1, y + rad + 1), fill=(0, 0, 0))
    im.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(255, 255, 255))
    im.text((x - rad + 15, y - rad + 15), label, font=ImageFont.load_default(), fill="black")

def draw_edge(im, x_1, y_1, x_2, y_2):
    im.line(((x_1, y_1), (x_2, y_2)), fill="black", width=1)

def draw_arrow(im, x_1, y_1, x_2, y_2):
   dist = ((x_1 - x_2)**2 + (y_1 - y_2)**2)**.5
   x_a = x_1 - (35 * (x_1 - x_2) / dist)
   y_a = y_1 - (35 * (y_1 - y_2) / dist)
   im.ellipse((x_a - 5, y_a - 5, x_a + 5, y_a + 5), fill=(0, 0, 0))


def main():
    t1 = CallData("one", "f1", ["one", "two", "four"])
    t2 = CallData("two", "f1", ["three", "four"])
    t5 = CallData("five", "f1", ["two"])
    t3 = CallData("three", "f2", ["one"])
    t4 = CallData("four", "f2", ["one"])
    test = [t1, t2, t3, t4, t5]
    draw(test)

if __name__ == "__main__":
    main()