###########################
# 6.0002 Problem Set 1b: Space Change

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs.
    Assumes there is an infinite supply of eggs of each weight, and there is
    always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest
    to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to 
    use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """

    possible_weights = []
    for weight in egg_weights:
        possible_weights.append(weight)
    
    def make_weight(possible_weights, target_weight):
        if possible_weights == [] or target_weight == 0:
            return 0
            #if there are no possible weights we can use, or if we have 
            #reached the target weight... return zero
        
        if target_weight - possible_weights[-1] < 0:
            return make_weight(possible_weights[:-1], target_weight)
            #if the heaviest eggs brings us over the target weight,
            #perform this function with all possible weights except heaviest
            #don't add an egg to result
    
        else:
            weightused = possible_weights[-1]
            target_weight -= weightused
            return 1 + make_weight(possible_weights, target_weight)
            #use the heaviest egg, subtract that weight from target weight
            #Return 1 egg, plus the result of performing this function again

    return make_weight(possible_weights, target_weight)

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()