# PS 10: Clustering
#
# Name: Peter Bekins
# Date: 5/10/20
#

import pylab, random, string, copy, math

class Point(object):

    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs

    def dimensionality(self):
        return len(self.attrs)

    def getAttrs(self):
        return self.attrs

    def getOriginalAttrs(self):
        return self.unNormalized

    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5

    def getName(self):
        return self.name

    def toStr(self):
        return self.name + str(self.attrs)

    def __str__(self):
        return self.name

class County(Point):

    def __init__(self, name, originalAttrs, normalizedAttrs=None):
        """
        I have modified the class to be able to set weights for
        feature selection
        """
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs
        self.weights = pylab.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    def setWeights(self, weights):
        self.weights = weights
    # this is a list of weights for each of the 14 features when clustering
    # weights = pylab.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    
    # Override Point.distance to use self.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(self.weights * difference * difference) ** 0.5
    
class Cluster(object):

    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()

    def getCentroid(self):
        return self.centroid

    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
        totVals/float(len(self.points)),
        totVals/float(len(self.points)))
        return meanPoint

    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0

    def getPoints(self):
        return self.points

    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False

    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]

    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]

def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """

    # adjust feature vectors for selection
    # Uses random initial centroids
    initialCentroids = random.sample(points,k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        #print "Starting iteration " + str(numIters)
        newClusters = []
        for c in clusters:
            newClusters.append([])
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)

        biggestChange = 0.0
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print 'Iteration count =', numIters
    maxDist = 0.0
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    #print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    #print biggestChange
    return clusters, maxDist

def readCountyData(fName, numEntries = 14):
    """
    Function to read county census data. Returns a list of county names
    in the format STATE+COUNTY, a list of feature vectors for each county,
    and a list of maxVals for each feature used in normalization
    """
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = pylab.array([0.0]*numEntries)
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line)
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals
    
def buildCountyPoints(fName):
    """
    Given an input filename, reads county data and returns list of County objects
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = pylab.array(featureList[i])
        normalizedAttrs = originalAttrs/pylab.array(maxVals)
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).
    
    l: The list to split
    p: The probability that an element of l will be in the first partition
    
    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)


def getAvgProperty(cluster, dimension):
    """
    Given a Cluster object and a dimension, finds the average value of the
    dimension field over the members of that cluster.

    cluster: the Cluster object to check
    dimension: index of the dimension within the feature vector

    Returns: a float representing the computed average income value
    """
    tot = 0.0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[dimension]

    return float(tot) / len(cluster.getPoints())

def featureSelection(points, weights):
    """
    Given a list of counties, sets the weight property that
    is to adjust the feature vector
    """
    for point in points:
        point.setWeights(weights)

def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAvgProperty(clusters[i], 1))

    pylab.hist(incomes)
    pylab.xlabel('Ave. Income')
    pylab.ylabel('Number of Clusters')

def findTrainingErr(clusters):
    """
    Helper function to calculate the total error in the training data.
    Error is defined as the sum of the square of the distance of
    each point in a cluster from the centroid of the cluster
    """
    error = 0
    for cluster in clusters:
        points = cluster.getPoints()
        centroid = cluster.getCentroid()
        for point in points:
            dist = point.distance(centroid) ** 2
            error += dist
            # print dist
    return error

def findHoldoutErr(points, clusters):
    """
    Helper function to find error in holdout data.
    Each point is grouped with the nearest cluster from the
    training data, then error is calculated as above.
    """
    error = 0
    for p in points:
        smallestDistance = p.distance(clusters[0].getCentroid())
        for i in range(len(clusters)):
            distance = p.distance(clusters[i].getCentroid())
            if distance < smallestDistance:
                smallestDistance = distance

        error += smallestDistance ** 2

    return error

def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values of k.
    For details see Problem 1.
    """
    tr_error = []
    ho_error = []

    # 1. split points into training (80%) and holdout (20%)
    training, holdout = randomPartition(points, 0.8)

    for k in kvals:

        # 2. Run k-means on training data
        tr_clusters, tr_maxSmallest = kmeans(training, k, cutoff, County)

        # 3. Calculate removed error for training data
        tr_error.append(findTrainingErr(tr_clusters))

        # 4. For each point in holdout data, measure distance to nearest centroid from training data
        ho_error.append(findHoldoutErr(holdout, tr_clusters))

    ratios = []
    for i in range(len(tr_error)):
        ratios.append(tr_error[i]/ho_error[i])

    # Plot training and holdout error for each k value
    pylab.figure()
    pylab.plot(kvals, tr_error, kvals, ho_error)
    pylab.xlabel('k')
    pylab.ylabel('Error')
    # Plot ratio of training to holdout eror for each k value
    pylab.figure()
    pylab.plot(kvals, ratios)
    pylab.xlabel('k')
    pylab.ylabel('Error')

def findPredictionErr(training, holdout, dimension, k, cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """

    # A. Run k-means on training data
    tr_clusters, tr_maxSmallest = kmeans(training, k, cutoff, County)

    # B. Find nearest cluster for each point in holdout data
    #    calculate average poverty for cluster
    #    guess holdout point.poverty based on average
    error = 0
    for h in holdout:
        # initialize cluster[0] as nearest
        smallestDistance = h.distance(tr_clusters[0].getCentroid())
        nearest_cluster = tr_clusters[0]
        # iterate through remaining clusters to find nearest
        for i in range(1, len(tr_clusters)):
            distance = h.distance(tr_clusters[i].getCentroid())
            if distance < smallestDistance:
                smallestDistance = distance
                nearest_cluster = tr_clusters[i]
        pred = getAvgProperty(nearest_cluster, dimension)
        act = h.getOriginalAttrs()[dimension]
        error += (act-pred) ** 2

    return error

def graphPredictionErr(points, dimension, weights, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """
    # 1. Adjust weights for feature selection
    featureSelection(points, weights)

    # 2. split points into training (80%) and holdout (20%)
    training, holdout = randomPartition(points, 0.8)

    # 3. Run prediction model  for each value of k
    errors = []
    for k in kvals:
        # find prediction error for k
        error = findPredictionErr(training, holdout, dimension, k, cutoff = 0.1)
        errors.append(error)

    print errors
    pylab.figure()
    pylab.plot(kvals, errors)
    pylab.xlabel('k')
    pylab.ylabel('Error')

def improvePredictionErr(points, dimension, weights, k, cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """
    # 1. split points into training (80%) and holdout (20%)
    training, holdout = randomPartition(points, 0.8)

    for weight in weights:
        # 2. Adjust weights for feature selection
        featureSelection(training, weight)
        featureSelection(holdout, weight)
        error = findPredictionErr(training, holdout, dimension, k)
        print weight
        print error

def homeCounty(county):
    """
    Function to find cluster that contains home county
    """
    homeClusters = []
    for trial in xrange(3):
        clusters, maxSmallest = kmeans(points, 50, 0.1, County, minIters=3, maxIters=100, toPrint=False)
        for c in clusters:
            if c.contains(county):
                homeClusters.append(c)
    return homeClusters

if __name__ == '__main__':
    ## Problem 0: Load data and test data structures
    points = buildCountyPoints('counties.txt')
    testPoints = random.sample(points, len(points) / 10)
    # test(testPoints)
    #random.seed(123)

    ## Problem 1: Graph the error in the training and holdout sets versus k
    #graphRemovedErr(points, cutoff = 0.1)

    ## Problem 2: Run k-means 3x with k = 50, note which cluster your home county clusters with
    #homeClusters = homeCounty('OHHamilton')
    #for cluster in homeClusters:
    #    print cluster

    # Problem 3: Graph the prediction error using k-means clustering to predict poverty rate
    # A. Set weight = 0 for Poverty (at index 2 in feature vector)
    # weights = pylab.array([1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    # B. Run k-means clustering to predict poverty rate and graph error
    # graphPredictionErr(testPoints, 2, weights)

    # Problem 4: Apply feature selection to decrease error in prediction
    testWeights = []
    # Set 1 is 3 pure economic indicators
    testWeights.append(pylab.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))
    # Set 2 is 6 pure demographic indicators
    testWeights.append(pylab.array([0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]))
    # Set 3 is income + education + unemployment
    testWeights.append(pylab.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]))
    # Set 4 is combo of 1 and 3
    testWeights.append(pylab.array([0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0]))

    improvePredictionErr(points, 2, testWeights, 75)

    pylab.show()



