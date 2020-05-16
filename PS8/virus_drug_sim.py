# PS 8: Simulating Virus Population Dynamics 2
#
# Name: Peter Bekins
# Date: 5/8/20




import numpy
import random
import pylab
from virus_sim import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.mutProb = mutProb
        self.resistances = resistances


    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        return self.resistances[drug]


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """

        # 1. Check if resistant to all drugs
        resistant = True
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                resistant = False

        # 2. If resistant then randomly create a child
        if resistant and (random.random() < self.maxBirthProb * (1 - popDensity)):
            child_resistances = {}
            # 2a. Switch all child resistances based on mutProb of parent
            for drug in self.resistances:
                if random.random() < self.mutProb:
                    child_resistances[drug] = not(self.resistances[drug])
                else:
                    child_resistances[drug] = self.resistances[drug]
            # 2b. Child inherits maxBirthProb, clearProb, and mutProb
            return ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)
        else:
            raise NoChildException

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """

        # should not allow one drug being added to the list multiple times
        if not newDrug in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistPop = 0

        for virus in self.viruses:
            # Assume resistant to all, flip to false if any fail
            resistant = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistant = False
            if resistant == True:
                resistPop += 1

        return resistPop

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """

        # 1. Determine if each virus survives using doesClear
        survived_viruses = []
        for virus in self.viruses:
            if not (virus.doesClear()):
                survived_viruses.append(virus)

        # 2. Calculate current population density
        self.viruses = survived_viruses
        pop_density = self.getTotalPop() / float(self.maxPop)

        # 3. Determine if each virus reproduces using reproduce
        new_viruses = []
        for virus in self.viruses:
            try:
                new_viruses.append(virus.reproduce(pop_density, self.drugs))
            except NoChildException:
                pass

        self.viruses.extend(new_viruses)

        return self.getTotalPop()



#
# PROBLEM 2
#

def getTrialAverage(data, numSteps, numTrials):
    """
    Helper function to convert lists of data from each trial to one list of avg data
    """
    avgData = []
    for i in xrange(0, numSteps):
        total = 0
        for d in data:
            total += d[i]
        avg = total / float(numTrials)
        avgData.append(avg)
    return avgData

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numSteps, delay, numTrials):

    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    print "Simulating with drug"
    allData1 = []
    allData2 = []
    # 1. Run Trials
    for i in xrange(0, numTrials):
        print "Trial " + str(i)
        data1, data2 = runSimulation1(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numSteps, delay)
        allData1.append(data1)
        allData2.append(data2)

    # 2. Get averages at each time step
    popData = getTrialAverage(allData1, numSteps, numTrials)
    resistData = getTrialAverage(allData2, numSteps, numTrials)

    pylab.plot(xrange(numSteps), popData, xrange(numSteps), resistData)
    pylab.xlabel("Number of Steps")
    pylab.ylabel("Virus Population")
    pylab.title("Simulation of Virus Population With No Treatment")


#
# PROBLEM 3
#        

def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numTrials):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    print "Simulating delayed treatment"
    delays = [300, 150, 75, 0]
    all_data = []
    # 1. Run Trials
    for delay in delays:
        data = []
        for i in xrange(0, numTrials):
            print "Trial " + str(i)
            final_pop = runSimulation2(numViruses, maxPop, maxBirthProb, clearProb, mutProb, delay + 150, delay)
            data.append(final_pop)
        all_data.append((delay, data))

    for delay in all_data:
        print delay[0], " : ", delay[1]
        pylab.figure()
        pylab.hist(delay[1], bins = (0,50,100,150,200,250,300,350,400,450,500,550,600))
        pylab.title('Final Virus Population When Drug Given at Step ' + str(delay[0]))
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numTrials):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    print "Simulating two drugs with delay"

    delays = [300, 150, 75, 0]
    all_data = []
    # 1. Run Trials
    for delay in delays:
        print "Delay until step " + str(delay)
        data = []
        for i in xrange(0, numTrials):
            print "    Trial " + str(i)
            final_pop = runSimulation3(numViruses, maxPop, maxBirthProb, clearProb, mutProb, delay)
            data.append(final_pop)
        all_data.append((delay, data))

    for delay in all_data:
        print delay[0], " : ", delay[1]
        pylab.figure()
        pylab.hist(delay[1], bins=(0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600))
        pylab.title('Final Virus Population When Drug Given at Step ' + str(delay[0]))

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numTrials, delay):

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """

    print "Simulating two drugs for final virus population"

    allData1 = []
    allData2 = []

    numSteps = delay + 300
    # 1. Run Trials
    for i in xrange(0, numTrials):
        print "Trial " + str(i)
        data1, data2 = runSimulation4(numViruses, maxPop, maxBirthProb, clearProb, mutProb, delay)
        allData1.append(data1)
        allData2.append(data2)

    # 2. Get averages at each time step
    popData = getTrialAverage(allData1, numSteps, numTrials)
    resistData = getTrialAverage(allData2, numSteps, numTrials)

    pylab.plot(xrange(numSteps), popData, xrange(numSteps), resistData)
    pylab.xlabel("Number of Steps")
    pylab.ylabel("Virus Population")
    pylab.title("Simulation of Virus Population With Delayed Treatment")


def runSimulation1(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numSteps, delay):

    """
    Runs simulation with drug prescribed at step delay
    returns list of tot_pop at each time step
    returns list of resist_pop at each timestep
    """

    viruses = []
    resistances = {"guttagonol": False}

    for n in xrange(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    patient = Patient(viruses, maxPop)
    data1 = []
    data2 = []

    for i in xrange(1, numSteps + 1):
        # Add prescription after t = delay
        if i > delay:
            patient.addPrescription("guttagonol")
        patient.update()
        data1.append(patient.getTotalPop())
        data2.append(patient.getResistPop(["guttagonol"]))

    return data1, data2


def runSimulation2(numViruses, maxPop, maxBirthProb, clearProb, mutProb, numSteps, delay):
    """
    Runs simulation with drug prescribed at step delay
    returns final population of viruses
    """

    viruses = []
    resistances = {"guttagonol": False}

    for n in xrange(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    patient = Patient(viruses, maxPop)

    for i in xrange(1, numSteps + 1):
        # Add prescription after t = delay
        if i > delay:
            patient.addPrescription("guttagonol")
        patient.update()

    return patient.getTotalPop()

def runSimulation3(numViruses, maxPop, maxBirthProb, clearProb, mutProb, delay):
    """
    Runs simulation with two drugs prescribed at step delay
    returns final population of viruses
    """

    viruses = []
    resistances = {"guttagonol": False, "grimpex": False}

    for n in xrange(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    patient = Patient(viruses, maxPop)
    numSteps = delay + 300

    for i in xrange(1, numSteps + 1):
        # Add prescription 1 after t = 150
        if i > 150:
            patient.addPrescription("guttagonol")
        # Add prescription 2 after t = 150 + delay
        if i > 150 + delay:
            patient.addPrescription("grimpex")
        patient.update()

    return patient.getTotalPop()

def runSimulation4(numViruses, maxPop, maxBirthProb, clearProb, mutProb, delay):

    """
    Runs simulation with drug prescribed at step delay
    returns list of tot_pop at each time step
    returns list of resist_pop at each timestep
    """

    viruses = []
    resistances = {"guttagonol": False, "grimpex": False}

    for n in xrange(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    patient = Patient(viruses, maxPop)
    data1 = []
    data2 = []

    numSteps = delay + 300
    for i in xrange(1, numSteps + 1):
        # Add prescription after t = delay
        if i > 150:
            patient.addPrescription("guttagonol")
        # Add prescription 2 after t = 150 + delay
        if i > 150 + delay:
            patient.addPrescription("grimpex")
        patient.update()
        data1.append(patient.getTotalPop())
        data2.append(patient.getResistPop(["guttagonol"]))

    return data1, data2

if __name__ == '__main__':
    simulationWithDrug(100, 1000, 0.1, 0.05, 0.005, 300, 150, 30)
    simulationDelayedTreatment(100, 1000, 0.1, 0.05, 0.005, 30)
    simulationTwoDrugsDelayedTreatment(100, 1000, 0.1, 0.05, 0.005, 30)
    simulationTwoDrugsVirusPopulations(100, 1000, 0.1, 0.05, 0.005, 30, 150)

    pylab.show()