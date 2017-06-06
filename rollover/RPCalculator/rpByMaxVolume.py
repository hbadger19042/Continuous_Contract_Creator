'''
Created on Jun 2, 2017

@author: dongi
'''

from .rpCalculator import RPCalculator

class RPByMaxVolume(RPCalculator):
    def __init__(self, matchingIndex = 1):
        super().__init__(matchingIndex)
        
    def Calculate(self, older_data, newer_data): 
        overlap = []
        olen = len(older_data)
        nlen = len(newer_data)
        new_start_index = 0
        for oi in range(olen):
            old_date = older_data[oi][0]
            if older_data[oi][self.matchingIndex]:
                new_search_range = range(new_start_index, nlen)
                for ni in new_search_range:
                    if old_date < newer_data[ni][0]:
                        new_start_index = ni
                        break
                    elif old_date == newer_data[ni][0]:
                        new_start_index = ni + 1
                        if newer_data[ni][self.matchingIndex]:
                            overlap.append( [oi, ni, newer_data[ni][0], newer_data[ni][5]] )  
                        break
        if not overlap:
            return
        max_couple = max(overlap, key=lambda item:item[3])    
        return max_couple[:3]          
