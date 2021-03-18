import xlrd , sys
from routePlanner import *
from tubeMap import *
from datetime import datetime, timedelta



class Node(object):

    def __init__(self, distance=None, next_node=None, next_node_reference=None, prev_node=None, prev_node_reference=None, trainLine=None):
        self.distance = distance
        self.next_node = next_node
        self.next_node_reference = next_node_reference
        self.prev_node = prev_node
        self.prev_node_reference = prev_node_reference
        self.trainLine = trainLine

class DoubleLinkedList(object):

    def __init__(self, head=None, end=None):
        self.head = head
        self.end = end

    def traverse(self):
        curr_node = self.head
        while curr_node != None:
            #print(curr_node.prev_node, curr_node.next_node, curr_node.distance)
            curr_node = curr_node.next_node_reference
        
    def addToGraph(self,graph):
        curr_node = self.head
        while curr_node != None:
            if curr_node.prev_node in graph:
                graph[curr_node.prev_node][curr_node.next_node] = [int(float(curr_node.distance))]
            else:
                graph[curr_node.prev_node] = {}
                graph[curr_node.prev_node][curr_node.next_node] = [int(float(curr_node.distance))]
            curr_node = curr_node.next_node_reference


    def insert(self, trainLine, pNode, nNode,distance):
        if self.head is None:
            new_node = Node(distance, next_node=nNode, prev_node=pNode, trainLine=trainLine)
            self.head = new_node
            return
        n = self.head
        while n.next_node_reference is not None:
            n = n.next_node_reference
        new_node = Node(distance,next_node=nNode, prev_node=pNode, trainLine=trainLine)
        n.next_node_reference = new_node
        new_node.prev_node_reference = n
        self.end = n.next_node_reference

def readfile():
    workbook = xlrd.open_workbook('London Underground data1.xlsx')
    worksheet = workbook.sheet_by_index(0)
    trainLineList = []
    trainLineListCheck = []
    trainLineNum = -1
    n = 0

    for i in range(0,worksheet.nrows):
        if (worksheet.cell(i,0).value not in trainLineList):
            trainLineList.append(worksheet.cell(i,0).value)
            trainLineListCheck.append(worksheet.cell(i,0).value)

    while n != len(trainLineList):
        trainLineList[n] = DoubleLinkedList()
        n+=1

    for i in range(0, worksheet.nrows):
        if worksheet.cell(i,0).value in trainLineListCheck:
            if worksheet.cell(i,0).value == '':
                if worksheet.cell(i-1,0).value == worksheet.cell(i+1,0).value:
                    index = trainLineListCheck.index(worksheet.cell(i-1,0).value)
                    trainLineList[index].insert(worksheet.cell(i-1,0).value, worksheet.cell(i,1).value, worksheet.cell(i,2).value, worksheet.cell(i, 3).value)
                #print("There is a blank space in trainLine column")
            else:
                if (worksheet.cell(i,2).value) == '':
                    pass
                else:
                    index = trainLineListCheck.index(worksheet.cell(i,0).value)
                    trainLineList[index].insert(worksheet.cell(i, 0).value, worksheet.cell(i, 1).value, worksheet.cell(i, 2).value, worksheet.cell(i, 3).value)
        else:
            print("error i believe there is no trainLine of the sort")
    return trainLineList





def dijkstra(graph, start, goal):
    shortest_distance = {}  # records the cost to reach to that node. Going to be
    track_predecessor = {}  # keep track of the path that has Led us to this node
    unseenNodes = graph  # to iterate through the entire graph.
    infinity = 9999999
    track_path = [] # going to trace our journey back to the source node -
    for node in unseenNodes:
        shortest_distance[node] = infinity
        shortest_distance[start] = 0

    while unseenNodes:

       min_distance_node = None
        
       for node in unseenNodes:
             if min_distance_node is None:
                 min_distance_node = node

             elif shortest_distance[node] < shortest_distance[min_distance_node]:
                 min_distance_node = node

       path_options = graph[min_distance_node].items()
       for child_node, weight in path_options:
           try:
                
               if weight[0] + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                   shortest_distance[child_node] = weight[0] + shortest_distance[min_distance_node]
                   track_predecessor[child_node] = min_distance_node
           except KeyError:
               pass


       unseenNodes.pop(min_distance_node)

    currentNode = goal

    while currentNode != start:
        try:
            track_path.insert(0, currentNode)
            currentNode = track_predecessor[currentNode]

        except KeyError:
                print("Path-is-not.reachable")
                break

    track_path.insert(0,start)


    if shortest_distance[goal] != infinity:
               print("Shortest distance is " + str(shortest_distance[goal]))
               print("Optimal path is " + str(track_path))
               return shortest_distance[goal], track_path


class CreateGUI(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.findRouteButton.clicked.connect(self.calcRoute)
        self.tubeMapPopUpButton.clicked.connect(self.openTubeMap)

    def calcRoute(self):
        start = self.startStationEntry.text()
        destination = self.destinationStationEntry.text()
        #timeTaken, path = dijkstra(graph, start, destination)
        ifGUIdoesNotWork(start, destination)
        ETA = datetime.now() + timedelta(minutes=timeTaken)

        

    def openTubeMap(self):
        d = PopUp(self)
        self.dialogs.append(d)
        d.show()

def ifGUIdoesNotWork(start, destination):
    start = input("Start")
    destination = input("Destination")
    timeTaken, path = dijkstra(graph, str(start), str(destination))
    print(Path)
    print("Takes", timeTaken, "Mins")
    ETA = datetime.now() + timedelta(minutes=timeTaken)
    print("Your estimated arrival to ", destination, "is", ETA)

class PopUp():
    def __init__(self, ):
        pass

def main():
    global graph
    graph = {}
    trainLineList = readfile()
    for i in trainLineList:
        i.addToGraph(graph)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CreateGUI(MainWindow)
    MainWindow.show() 
    sys.exit(app.exec_())

main()
