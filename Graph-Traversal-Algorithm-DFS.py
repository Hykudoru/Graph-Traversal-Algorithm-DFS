class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def X(self):
        return int(self.x)

    def Y(self):
        return int(self.y)
    
def dot4(vecA, vecB):
    return vecA[0] * vecB[0] + vecA[1] * vecB[1] + vecA[2] * vecB[2] + vecA[3] * vecB[3]

up = [1,0,0,0]
right = [0,1,0,0]
down = [0,0,-1,0]
left = [0,0,0,-1]

symbolVectors = {'*' : [1,1,-1,-1],
          'A' : [1,1,-1,-1],
          'B' : [1,1,-1,-1],
          'C' : [1,1,-1,-1],
          'D' : [1,1,-1,-1],
          'E' : [1,1,-1,-1],
          'F' : [1,1,-1,-1],
          'G' : [1,1,-1,-1],
          'H' : [1,1,-1,-1],
          'I' : [1,1,-1,-1],
          'J' : [1,1,-1,-1],
          'K' : [1,1,-1,-1],
          'L' : [1,1,-1,-1],
          'M' : [1,1,-1,-1],
          'N' : [1,1,-1,-1],
          'O' : [1,1,-1,-1],
          'P' : [1,1,-1,-1],
          'Q' : [1,1,-1,-1],
          'R' : [1,1,-1,-1],
          'S' : [1,1,-1,-1],
          'T' : [1,1,-1,-1],
          'U' : [1,1,-1,-1],
          'V' : [1,1,-1,-1],
          'W' : [1,1,-1,-1],
          'X' : [1,1,-1,-1],
          'Y' : [1,1,-1,-1],
          'Z' : [1,1,-1,-1],
          '═' : [0,1,0,-1],
          '║' : [1,0,-1,0],
          '╔' : [0, 1,-1,0],
          '╗' : [0,0,-1,-1],
          '╚' : [1,1,0,0],
          '╝' : [1,0,0,-1],
          '╠' : [1,1,-1,0],
          '╣' : [1,0,-1,-1],
          '╦' : [0,1,-1,-1],
          '╩' : [1,1,0,-1]
          }

sinks = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
sinksConnected = set()
cells = {}

class Node:
    NodesTraversed = set()
    MaxDepth = 50
    def __init__(self, position, symbol, parent = None):
        self.position = position
        self.symbol = symbol
        self.parent = parent
        if not parent: 
            self.root = self
            self.currentDepth = 0
        else:
            self.root = self.parent.root
            self.currentDepth = self.parent.currentDepth + 1

        Node.NodesTraversed.add(position)

        self.nodes = []
        adjCells = findAdjacentCells(position)
        adjCells = [x for x in adjCells if x != None]
        for cell in adjCells:
            # Make sure cell has not already been traversed (identified by its unique position)
            pos = cell[1]
            if (not pos in Node.NodesTraversed):
                self.traverse(cell)

        # space = "    "*self.currentDepth + "Level: "+str(self.currentDepth)
        # print(space, "Nodes: ",len(self.nodes), self.nodes)
        # print(self.root.symbol)

    def traverse(self, cellData):
            symbol = cellData[0]
            pos = cellData[1]
            relativeDir = cellData[2]
            relativeReverseDir = cellData[3]
            
            # First check if this node can connect in the direction of the other cell
            # Then check if the other cell can also connect in the direction of this node
            # Add new cell as Node if is a connecting node. This will also be recursive when creating a new Node.
            if bool(dot4(symbolVectors[self.symbol], relativeDir)) and bool(dot4(symbolVectors[symbol], relativeReverseDir)):
                if (symbol == "*"):
                    sinksConnected.add(self.root.symbol)
                else:
                    if self.currentDepth < Node.MaxDepth:
                        node = Node(pos, symbol, self)
                        self.nodes.append(node) 

def findAdjacentCells(pos):
    rightOf = None
    leftOf = None
    upOf = None
    downOf = None

    for point, symbol in cells.items():
        if point.X() == pos.X() and point.Y() == pos.Y()+1:
            upOf = [symbol, point, up, down]
        elif point.X() == pos.X()+1 and point.Y() == pos.Y():
            rightOf = [symbol, point, right, left]
        elif point.X() == pos.X() and point.Y() == pos.Y()-1:
            downOf = [symbol, point, down, up]
        elif point.X() == pos.X()-1 and point.Y() == pos.Y():
            leftOf = [symbol, point, left, right]
    
    # return tuple where each directionOf variable = [symbol, point, relativeDirection, reverseRelativeDirection]
    return upOf, rightOf, downOf, leftOf

def findSinksToSource(filePath):
    data = None
    try:
        with open(filePath, encoding='utf-8') as file:
            data = file.read()
    except:
        print(f"[ERROR] Problem reading file")
    else:

        # Create dictionary for cell data
        listData = data.split()
        i = 0
        while i < len(listData):
            symbol = str(listData[i])
            if (i+2 < len(listData)):
                point = Point(listData[i+1], listData[i+2])
                cells[point] = symbol
            i += 3
        
        i = 1
        # Get and create all sink nodes.
        for pos, symbol in cells.items():
            for sink in sinks:
                if (symbol == sink):
                    Node.NodesTraversed.clear()
                    print(sinksConnected)
                    print(symbol, pos.x, pos.y)
                    Node(pos, symbol)
                    print(str(round((i/26)*100))+"%")
                    i += 1
                
        found = list(sinksConnected)
        found.sort()
        return ''.join(found).upper()

print(findSinksToSource("data.txt"))


# My algorithm uses a node like tree structure. Here is the jist of it:
# - Read file and create a dictionary for cell data
# - Get and create all sink nodes.
# - Find adjacent cells (if any).
# - Make sure the cell comparing has not been traversed and somehow looped back to the root node.
# - Check if this cell's edge is open in the direction of the other cell and vice-versa.
# - Add new cell Node if both edges are open. This will also be recursive when creating a new Node.
# - Any root sink node that encounters an '*' will be added to the connected sinks we're tracking. 
# Node MaxDepth can be tweaked to allow longer path traversal.           

# I'm a big fan of matrix math, so I used matrices for each sink and pipe character to compare edge openings.
# How the matrix masking works: 
# If we have an arbitrary adjacent cell say to the right of a sink 'A', we can multiply the 'A' Symbol Matrix by 'Right' matrix [0,1,0,0] to check if the right edge is open.
# Then we do the same with the adjacent cell's Symbol Matrix by the 'Left' Matrix [0,0,0,-1] to ensure this edge is also open.
# If both are open, these 2 cells connect.
# For example: Matrix [1, 1, -1, -1] corresponds to [up, right, down, left] and means all directions are open.
