# PS 11: Graph optimization, Finding shortest paths through MIT buildings
#
# Name: Peter Bekins
# Date: 5/12/20
#

import string
from graph import *

#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    print "Loading map from file..."
    dataFile = open(mapFilename, 'r')
    map = mapGraph()
    nodes = []
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue

        dataLine = string.split(line)
        src = dataLine[0]
        dest = dataLine[1]
        # If src or dst are not already nodes, create them

        if not src in nodes:
            nodes.append(src)
            map.addNode(Node(src))

        if not dest in nodes:
            nodes.append(dest)
            map.addNode(Node(dest))

        source = map.getNode(src)
        destination = map.getNode(dest)
        weight = (int(dataLine[2]), int(dataLine[3]))

        map.addEdge(mapEdge(source, destination, weight))

    return map

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def allPaths(graph, start, end, maxTotalDist, maxDistOutdoors, path = []):

    """
    This function walks every possible path between start and end. If the
    path meets the constraints (total and outdoor dist) it is added to the list.

    Returns list of all paths that meet constraints.
    """

    path = path + [start]

    if start == end:
        totLength, outLength = pathLength(graph, path)
        if (totLength <= maxTotalDist) and (outLength <= maxDistOutdoors):
            return [path]
    if not (graph.hasNode(start)):
        return []
    paths = []
    for node in graph.childrenOf(start):
        if node[0] not in path:
            #print "current path " + str(path)
            extended_paths = allPaths(graph, node[0], end, maxTotalDist, maxDistOutdoors, path)
            for p in extended_paths:
                paths.append(p)
    return paths

def pathLength(graph, path):

    totLength = 0
    outLength = 0

    for i in range(len(path)-1):
        for node in graph.childrenOf(path[i]):
            if node[0] == path[i+1]:
                totLength += node[1][0]
                outLength += node[1][1]

    return totLength, outLength

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    start_node = digraph.getNode(start)
    end_node = digraph.getNode(end)


    paths = allPaths(digraph, start_node, end_node, maxTotalDist, maxDistOutdoors)

    # 2. Select shortest path under constraints
    shortPath = None
    shortLength = None

    # print "Brute force found " + str(len(paths)) + " paths"
    for path in paths:
        totLength, outLength = pathLength(digraph, path)
        if (shortLength == None) and (totLength <= maxTotalDist) and (outLength <= maxDistOutdoors):
            shortLength = totLength
            shortPath = path
        elif (totLength < shortLength) and (totLength <= maxTotalDist) and (outLength <= maxDistOutdoors):
            shortLength = totLength
            shortPath = path

    if shortPath == None:
        raise ValueError
    else:
        return shortPath

#
# Problem 4: Finding the Shortest Path using Optimized Search Method
#

def dfSearch(graph, start, end, maxTotalDist, maxDistOutdoors, path = [], memo = None):

    """
    This walks every possible path between original start and end.
    Memo keeps track of shortest path.

    If any partial path hits the current shortest length,
    it gives up and backtracks to the next option.

    If any partial path hits maxTotalDist or maxDistOutdoors, it gives up
    and backtracks to the next option.

    returns list of tuples (path, length)
    """

    # Initialize memo each time search function is first called
    if memo == None:
        memo = {}

    path = path + [start]

    if start == end:
        # Reached the destination
        length, outdoor = pathLength(graph, path)
        key = 'shortest'
        # set shortest length for AE in memo
        if key in memo:
            shortest = memo[key]
            if (length < shortest) and (length <= maxTotalDist) and (outdoor <= maxDistOutdoors):
                memo[key] = length
        else:
            memo[key] = length

        if (length <= maxTotalDist) and (outdoor <= maxDistOutdoors):
            return [path]

    if not (graph.hasNode(start)):
        return []

    short = None
    paths = []
    for node in graph.childrenOf(start):
        if node[0] not in path:
            # Check shortest length to give up on path
            length, outdoor = pathLength(graph, path)
            if 'shortest' in memo:
                short = memo['shortest']
            if (short != None and length >= short) or (outdoor > maxDistOutdoors) or (length > maxTotalDist):
                continue
            else:
                newPath = dfSearch(graph, node[0], end, maxTotalDist, maxDistOutdoors, path, memo)
                for p in newPath:
                    paths.append(p)

    return paths

def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """

    start_node = digraph.getNode(start)
    end_node = digraph.getNode(end)

    # 1. Call dfSearch to find all possible paths that fit constraints

    paths = dfSearch(digraph, start_node, end_node, maxTotalDist, maxDistOutdoors)

    # 2. Select shortest path under constraints
    shortPath = None
    shortLength = None

    # print "DFS found " + str(len(paths)) + " paths"

    for path in paths:
        # print path
        totLength, outLength = pathLength(digraph, path)
        if (shortLength == None):
            shortLength = totLength
            shortPath = path
        elif (totLength < shortLength):
            shortLength = totLength
            shortPath = path

    if shortPath == None:
        raise ValueError
    else:
        return shortPath

# Uncomment below when ready to test
if __name__ == '__main__':
    # Test cases
    digraph = load_map("mit_map.txt")

    LARGE_DIST = 1000000

    # Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1

    # Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2

    # Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3

    # Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4

    # Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5

    # Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6

    # Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

    # Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'

    try:
         directedDFS(digraph, '10', '32', 100, LARGE_DIST)
    except ValueError:
         dfsRaisedErr = 'Yes'

    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

