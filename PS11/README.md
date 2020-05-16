This project demonstrates optimization (shortest path) for a weighted digraph. The data for the graph concists of a set 
of buildings on the MIT campus (the nodes) and paths between buildings (the edges) weighted for both total distance and 
distance spent outdoors. Optimizations are run on a vaiety of constraints related to the max total distance and the max
distance spent outdoors.

Note that the problem set required the use of a depth-first search, but depth-first does not seem to be a good choice
for finding the shortest path with a weighted graph (an internet search shows that the Dijkstra algorithm is preferred).
My main problem was finding a way to remember the shortest path while recursing through the nodes. I ended up storing this
value in a dict that was passed each time the shortest path function was called. This seems to be a bit janky, but it works.
No solution was posted with this problem set, so I am not sure what the expected solution was.
