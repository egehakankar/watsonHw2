# coding=utf-8
# This is the submission of the project group named WATSON for Homework 2.
# To run normally: python main.py

# Members:
#           Mehmet Berk Şahin (CONTACT)
#           Balaj Saleem
#           Mehmet Alper Genç
#           Ege Hakan Karaağaç
#           Fırat Yönak

import random
import sys
import plotly.graph_objects as go
import plotly.offline as pyo
import plotly as py

def random15PuzGenerator(goal):
    randomizeCount = 20



def printPuzzle(puz, puzName):
    fig = go.Figure(data=[go.Table(
        header = dict(
        values = [[puzName],
                  ['0'],
                  ['1'],
                  ['2'],
                  ['3']],
                  fill_color='royalblue',
                  line_color='darkslategray',
                  font=dict(color='white')),
                 cells=dict(values=[
                  [0, 1, 2, 3],
                  [puz[0][0], puz[1][0], puz[2][0], puz[3][0]],
                  [puz[0][1], puz[1][1], puz[2][1], puz[3][1]],
                  [puz[0][2], puz[1][2], puz[2][2], puz[3][2]],
                  [puz[0][3], puz[1][3], puz[2][3], puz[3][3]]],
                  fill=dict(color=['royalblue', 'white', 'white', 'white', 'white']),
                  line_color='darkslategray',
                  font=dict(color=['white', 'black', 'black', 'black', 'black'])))
                     ])
    fig.update_layout(width=500, height=600)
    return fig

def goalStateGenerater():
    w = 4
    goal = [[0 for x in range(w)] for y in range(w)] 
    goal[0][0] = 1
    goal[0][1], goal[1][0], goal[2][3], goal[3][2] = 2,2,2,2
    goal[0][2], goal[1][1], goal[1][3], goal[2][0], goal[2][2], goal[3][1] = 3,3,3,3,3,3
    goal[0][3], goal[1][2], goal[2][1], goal[3][0] = 4,4,4,4
    return goal

goal = goalStateGenerater()
print("Goal State:")
goal1 = printPuzzle(goal, "Goal")
goal2 = printPuzzle(goal, "Init")

allPlots = []
allPlots.append(goal1)
allPlots.append(goal2)

layout = html.Div(
        [html.Div(allPlots[i], style=col_style[i]) for i in range(len(allPlots))],
        style = {'margin-right': '0px'}
    )

app.layout = layout
app.run_server(port=8052)

"""with open('p_graph.html', 'a') as f:
    f.write(goal1.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(goal2.to_html(full_html=False, include_plotlyjs='cdn'))"""


"""
S1 = random15PuzGenerator(goal)
S2 = random15PuzGenerator(goal)
S3 = random15PuzGenerator(goal)
"""
exit(0)
