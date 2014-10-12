import numpy as np
import os

def itera_f(num, start, steps):
    ''' All possible portfolio configurations. BETTER IMPLEMENTATION??
        steps = (int) Size of the steps. Input 100 would be interpreted as 1.
                                Input 10, 0.1. Input 1, 0.01.
        '''    
    if num[start]-steps >= 0:
        array_ones = []
        for itera in range(int(num[start]/steps)):
            print '|',
            num[start] -= steps
            num[start+1] = 100+steps
            for i in range(int(num[start+1]/steps)):
                num[start+1] -= steps
                if sum(num) == 100:
                    array_ones = np.append(array_ones, num, axis=0)
                elif (sum(num) < 100) and (start < len(num)-2):
                    num[start+1] += steps
                    new_row = itera_f(num, start+1, steps)
                    if type(new_row) == np.ndarray:
                        array_ones = np.append(array_ones, new_row, axis=0)
        return array_ones
    else:
        return None

    

def permutes_f(steps, length):
    ''' steps = (float) Up to two decimal points. Size of the steps for possible allocations.
        length = number of objects/items to check allocations for '''

    savecsv = 'S'+str(int(steps*100))+'L'+str(length)+'.csv'
    
    # 1. Check if a Matrix has already been generated
    if os.path.isfile(savecsv):
        array_num = np.genfromtxt(savecsv, delimiter=',')
        print 'A matrix of all possible allocations with 0.1 steps has been found'

    # 2. If it has not, generate and save
    else:
        print 'Creating a matrix of all possible allocations with 0.1 steps'
        start = 0
        steps *= 100

        num = np.zeros(length)
        num[0] = 100+steps
        
        array_num = np.array(itera_f(num, start, steps))
        array_num /= 100
        array_num.resize((len(array_num)/len(num), len(num)))
        
        print
        print
        print 'Saving matrix...'
        np.savetxt(savecsv, array_num, delimiter=',')
        print
        print 'Matrix saved!'
        
    # 3. Return the array
    return array_num



#np.savetxt('matrix.txt', permutes_f(0.1, 4))

#print permutes_f(0.1, 10)


