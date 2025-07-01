import random

colors= [
    (255, 250, 129),
    (255, 237, 81),
    (191, 228, 117),
    (145, 210, 144),
    (72, 181, 163),
    (154, 206, 223),
    (191, 213, 232),
    (117, 137, 191),
    (251, 182, 209),
    (249, 140, 182),
    (165, 137, 193),
    (252, 169, 133),
]

class Shape:
    x=0
    y=0

    # The following lists are the shapes that are used in the game, with their rotations described by
    # the positions in a 4X4 matix :
    #  0   1    2    3
    #  4   5    6    7
    #  8   9    10   11
    #  12  13   14   15


    shape_I=[[1, 5, 9, 13], [4, 5, 6, 7]]
    shape_J=[[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]]
    shape_L=[[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]]
    shape_T=[[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]]
    shape_Q=[[1, 2, 5, 6]]
    shape_S=[[1, 2, 4, 5], [1, 5, 6, 10]]
    shape_Z=[[0, 1, 5, 6], [2, 5, 6, 9]]
    shape_plus=[[1,4,5,6,9]]
    shape_U=[[0,2,4,5,6],[0,1,5,8,9,],[0,1,2,4,6],[0,1,4,8,9]]
    shape_hill=[[0,4,5,8,9,10],[2,5,6,8,9,10],[0,1,2,5,6,10],[0,1,2,4,5,8]]
    shapes=[shape_I, shape_J, shape_L, shape_T, shape_Q, shape_S, shape_Z, shape_plus, shape_U, shape_hill]


    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.type=random.randint(0,len(self.shapes)-1)
        self.color=random.randint(1,len(colors)-1)
        self.rotation=0
    

    def image(self):
        return self.shapes[self.type][self.rotation]
    
    def rotate(self):
        self.rotation=(self.rotation + 1) % len(self.shapes[self.type])
