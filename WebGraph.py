import sys
import codecs
import queue
import time
import pickle
import os
import collections


def parseNameToID():
    sites = codecs.open(sys.argv[2], 'r', encoding='iso-8859-1')
    dict = {}
    for line in sites.readlines():
        split_line = line.split()
        dict[split_line[0]] = split_line[1]
    return dict

def parseIDToName():
    sites = codecs.open(sys.argv[2], 'r', encoding='iso-8859-1')
    dict = {}
    for line in sites.readlines():
        split_line = line.split()
        dict[split_line[1]] = split_line[0]
    return dict

def buildOutboundAdjacencyList():
    edges = codecs.open(sys.argv[3], 'r', encoding='iso-8859-1')
    dict = {}
    for line in edges.readlines():
        split_line = line.split()
        if split_line[0] not in dict:
            dict[split_line[0]] = [split_line[1]]
        else:
            dict[split_line[0]].append(split_line[1])
    return dict

def buildInboundAdjacencyList():
    edges = codecs.open(sys.argv[3], 'r', encoding='iso-8859-1')
    dict = {}
    for line in edges.readlines():
        split_line = line.split()
        if split_line[1] not in dict:
            dict[split_line[1]] = [split_line[0]]
        else:
            dict[split_line[1]].append(split_line[0])
    return dict

def buildGoodList(dictionary):
    ls = []
    for key in dictionary:
        if len(dictionary[key]) >= int(sys.argv[5]):
            ls.append(key)
    return ls

def buildShitList(graph, start):
    visited = set()
    #q = queue.Queue()
    #q.put(start)
    q = collections.deque()
    q.append(start)
    depth = 0
    timeToDepthIncrease = 1
    #lastTime = time.time()
    while len(q) > 0:
        if depth == int(sys.argv[5]) + 1:
            return visited
        node = q.popleft()
        timeToDepthIncrease = timeToDepthIncrease - 1
        #if timeToDepthIncrease % 1000 == 0:
            #print(timeToDepthIncrease)
            #print(time.time() - lastTime)
            #lastTime = time.time()
        if node not in visited:
            visited.add(node)
            if node in graph:
                unvisited = set(graph[node]) - visited
                for child in unvisited:
                    q.append(child)
        if timeToDepthIncrease == 0:
            depth = depth + 1
            timeToDepthIncrease = len(q)
    return visited

def findShortestPath(graph, start, destination):
    visited = set()
    q = queue.Queue()
    q.put((start, [start]))
    while not q.empty():
        pair = q.get()
        node = pair[0]
        path = pair[1]
        if node == destination:
            return path
        if node not in visited:
            visited.add(node)
            if node in graph:
                unvisited = set(graph[node]) - visited
                for child in unvisited:
                    q.put((child, path + [child]))

def prune():
    inDict = {}
    if not os.path.isfile('cereal'):
        inDict = buildInboundAdjacencyList()
        pickle_out = open("cereal", 'wb')
        pickle.dump(inDict, pickle_out, protocol=4)
        pickle_out.close()
    else:
        pickle_in = open("cereal", 'rb')
        inDict = pickle.load(pickle_in)
        pickle_in.close()
    goodList = buildGoodList(inDict)
    f = open(sys.argv[4], 'w')
    for key in inDict:
        if key in goodList:
            for entry in inDict[key]:
                if entry in goodList:
                    f.write(entry + "\t" + key + "\n")  #Reverse key and entry positions depending on how it's tested
    f.close()

def path():
    NameToIDDict = parseNameToID()
    IDToNameDict = parseIDToName()
    startID = NameToIDDict[sys.argv[5]]
    destID = NameToIDDict[sys.argv[6]]
    outDict = buildOutboundAdjacencyList()
    path = findShortestPath(outDict, startID, destID)
    f = open(sys.argv[4], 'w')
    for i in range(0, len(path)-1):
        f.write(IDToNameDict[path[i]] + "\t" + IDToNameDict[path[i+1]] + "\n")
    f.close()

def cover():
    NameToIDDict = parseNameToID()
    urlID = NameToIDDict[sys.argv[6]]
    inDict = {}
    if not os.path.isfile('cereal'):
        inDict = buildInboundAdjacencyList()
        pickle_out = open("cereal", 'wb')
        pickle.dump(inDict, pickle_out, protocol=4)
        pickle_out.close()
    else:
        pickle_in = open("cereal", 'rb')
        inDict = pickle.load(pickle_in)
        pickle_in.close()
    shitList = buildShitList(inDict, urlID)
    f = open(sys.argv[4], 'w')
    for key in inDict:
        if key not in shitList:
            for entry in inDict[key]:
                if entry not in shitList:
                    f.write(entry + "\t" + key + "\n") #Reverse if needed
    f.close()

if __name__ == "__main__":
    startTime = time.time()
    if sys.argv[1] == "-prune":
        prune()
        print(time.time() - startTime)
    if sys.argv[1] == "-path":
        path()
        print(time.time() - startTime)
    if sys.argv[1] == "-cover":
        cover()
        print(time.time() - startTime)