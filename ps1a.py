###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cowdata1 = open(filename,'r')
    cowdictionary = {}
    for line in cowdata1:
        line = line.strip('\n')
        line = line.split(',')
        cowdictionary[line[0]] = int(line[1])
    cowdata1.close()
    return cowdictionary

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow
       that will fit to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cows_copy = sorted(cows, key=cows.get, reverse = True)
    #cows.get applies to all keys
    totaltrips = []        
    while len(cows_copy) > 0:
        totalWeight = 0
        currenttrip = []
        """
        need to use index otherwise was skipping index position 1
        we are removing the first element typically with each loop below
        so index position 1 becomes position 0, which we already did,
        so python skips over it
        """        
        for name in cows_copy[0:]:
            if cows[name] + totalWeight <= limit:
                currenttrip.append(name)
                totalWeight += cows[name]
                cows_copy.remove(name)
            elif cows[name] > limit:
                cows_copy.remove(name)
        totaltrips.append(currenttrip)
    return totaltrips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following
    method:

    1. Enumerate all possible ways that the cows can be divided into separate
       trips. Use the given get_partitions function in ps1_partition.py!
    2. Select the allocation that minimizes the number of trips without making
       any trip that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    answer = []
    cowlist = []
    for name in cows:
        cowlist.append(name)
    for partition in get_partitions(cowlist):
        overlimit = 0
        for trip in partition:
            tripweight = 0
            for cow in trip:
                tripweight += cows[cow]
            if tripweight > limit:
                overlimit += 1
                break
        if overlimit == 0:
            answer = partition
            break
    return answer

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cowfile1 = "ps1_cow_data.txt"
    cows = load_cows(cowfile1)
    
    print('Test greedy algorithm')
    start = time.time()
    print(greedy_cow_transport(cows,limit=10))
    end = time.time()
    print(end - start)
    
    print('***************')
    
    print('Test brute algorithm:')
    start = time.time()
    print(brute_force_cow_transport(cows,limit=10))
    end = time.time()
    print (end - start)
    
    return 0

compare_cow_transport_algorithms()