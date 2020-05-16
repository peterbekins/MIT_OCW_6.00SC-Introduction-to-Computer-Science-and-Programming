# PS 9: Intelligent Course Advisor
#
# Name: Peter Bekins
# Date: 5/9/20
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    output = {}
    for line in inputFile:
        data = line.rstrip().split(',')
        name = data[0]
        value = int(data[1])
        work = int(data[2])
        output[name] = (value, work)

        # print data

    return output

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    ratio1 = subInfo1[0]/float(subInfo1[1])
    ratio2 = subInfo2[0]/float(subInfo2[1])
    return ratio1 > ratio2

def dictSort(keys, dict, comp):
    """
    Helper function to sort keys based on comparator applied to values.
    Assumes that keys is a list of keys for dict. Sorts keys based on
    values by applying pairwise comparator comp. Final list of keys will
    be in order of best to worst.
    """
    for i in range(len(keys) - 1):
        minIndx = i
        minVal = keys[i]
        j = i + 1
        while j < len(keys):
            if comp(dict[keys[j]], dict[minVal]):
                minIndx = j
                minVal = keys[j]
            j += 1

        temp = keys[i]
        keys[i] = keys[minIndx]
        keys[minIndx] = temp

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    #print "In greedy advisor"
    # 1. Sort course keys by comparator
    keys = subjects.keys()
    dictSort(keys, subjects, comparator)

    # 2. Take best while <= max work
    totalWork = 0
    best_subjects = {}
    # a. Iterate through sorted keys
    for key in keys:
        newWork = subjects[key][1]
        # b. If newWork will not push totalWork over the limit
        #    add the course and update totalWork
        if totalWork + newWork <= maxWork:
            best_subjects[key] = subjects[key]
            totalWork += newWork

    return best_subjects
#
# Problem 3: Subject Selection By Brute Force
#

def dToB(n, numDigits):
    """
    Convert decimal number to a binary string where n is decimal number
    to convert and numDigits pads with zeros. Creates bit mask used to build Pset.
    """
    bStr = ''
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n//2
    while numDigits - len(bStr) > 0:
        bStr = '0' + bStr
    return bStr

def genPset(Items):
    """
    Generate a list of lists representing the power set of Items
    """
    numSubsets = 2**len(Items)
    templates = []
    for i in range(numSubsets):
        templates.append(dToB(i, len(Items)))
    pset = []
    for t in templates:
        elem = []
        for j in range(len(t)):
            if t[j] == '1':
                elem.append(Items[j])
        pset.append(elem)
    return pset

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    best_subjects = {}
    # 1. Generate Pset of keys
    keys = subjects.keys()
    Pset = genPset(keys)

    # 2. Calculate value + work for each set
    bestValue = 0
    bestSet = None
    for set in Pset:
         value = 0
         work = 0
         for key in set:
             value += subjects[key][0]
             work += subjects[key][1]
         if value > bestValue and work <= maxWork:
             #print set, value, work
             bestValue = value
             bestSet = set

    # 3. Convert list of keys to dict
    for key in bestSet:
        best_subjects[key] = subjects[key]

    return best_subjects

if __name__ == '__main__':
    # Short Subjects can be used for testing purposes
    #subjects = loadSubjects(SUBJECT_FILENAME)
    subjects = loadSubjects(SHORT_SUBJECT_FILENAME)

    # Compare methods with max work of 10; Greedy will sort based on value
    bestGreedySubjects = greedyAdvisor(subjects, 12, cmpValue)
    bestBFSubjects = bruteForceAdvisor(subjects, 12)
    printSubjects(bestGreedySubjects)
    printSubjects(bestBFSubjects)