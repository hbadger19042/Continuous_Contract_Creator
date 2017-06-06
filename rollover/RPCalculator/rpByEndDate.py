'''
Created on Jun 2, 2017

@author: dongi
'''
from .rpCalculator import RPCalculator

class RPByEndDate(RPCalculator):
    def __init__(self, matchingIndex=1):
        super().__init__(matchingIndex)
    
    
    def Calculate(self, older_data, newer_data):
        new_start_index = len(newer_data) -1
        for oi in reversed(range(len(older_data))):
            old_date = older_data[oi][0]
            if older_data[oi][self.matchingIndex]:
                new_search_range = range(new_start_index, -1, -1)
                for ni in new_search_range:
                    if old_date > newer_data[ni][0]:
                        new_start_index = ni
                        break
                    elif old_date == newer_data[ni][0]:
                        new_start_index = ni -1
                        if newer_data[ni][self.matchingIndex]:
                            return [oi] + [ni] + [old_date]