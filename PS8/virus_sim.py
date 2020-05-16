# PS 7: Simulating the Spread of Disease and Virus Population Dynamics
# Name: Peter Bekins
# Date: 5/7/20


import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        return (random.random() < self.clearProb)

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        if (random.random() < self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # 1. Determine if each virus survives using doesClear
        survived_viruses = []
        for virus in self.viruses:
            if not(virus.doesClear()):
                survived_viruses.append(virus)

        # 2. Calculate current population density
        self.viruses = survived_viruses
        pop_density = self.getTotalPop()/float(self.maxPop)

        # 3. Determine if each virus reproduces using reproduce()
        new_viruses = []
        for virus in self.viruses:
            try:
                new_viruses.append(virus.reproduce(pop_density))
            except NoChildException:
                pass
        self.viruses.extend(new_viruses)

        return self.getTotalPop()



#
# PROBLEM 2
#
def simulationWithoutDrug(numSteps, numViruses, maxPop, maxBirthProb, clearProb):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """

    numSims = 10
    allData = []

    # 1. Run model x numSims, store data as list
    for sim in range(numSims):
        viruses = []

        for n in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))

        patient = SimplePatient(viruses, maxPop)

        data = []
        data.append(patient.getTotalPop())

        for i in xrange(1, numSteps + 1):
            patient.update()
            data.append(patient.getTotalPop())

        allData.append(data)

    # 2. Get averages at each time step
    avgData = []
    for j in xrange(0, numSteps + 1):
        total = 0
        for data in allData:
            total += data[j]
        avg = total/float(numSims)
        avgData.append(avg)

    pylab.plot(range(numSteps + 1), avgData)
    pylab.xlabel("Number of Steps")
    pylab.ylabel("Virus Population")
    pylab.title("Simulation of Virus Population With No Treatment")


if __name__ == '__main__':
    simulationWithoutDrug(300, 100, 1000, 0.1, 0.05)
    pylab.show()