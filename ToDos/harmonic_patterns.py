import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from utils import Utils

class Harmonic_Patterns():

    def __init__(self) -> None:

        self.result_df = pd.DataFrame(columns=['Function', 'Signal', 'Relevance'])
        
        # Bullish Gartly
        self.b_g_signal = None
        self.b_g_relevence = None
    
    def peak_detect(self, close, order=10):
        '''
        This function find the peaks of a timeframe    
        '''

        max_idx = list(argrelextrema(close, comparator=np.greater, order=order)[0])
        min_idx = list(argrelextrema(close, comparator=np.less, order=order)[0])

        idx = max_idx + min_idx + [len(close)-1]

        idx.sort()

        current_idx = idx[-5:]

        start = min(current_idx)
        end = max(current_idx)

        current_pat = close[current_idx]

        return idx, current_pat, start, end

    def get_gartley_hp(self, moves, err_allowed):
        
        close = data.close

    for i in range(100,len(close)):

        idx, current_pat, start, end = peak_detect(close.values[:i])

        XA = current_pat[1] - current_pat[0]
        AB = current_pat[2] - current_pat[1]
        BC = current_pat[3] - current_pat[2]
        CD = current_pat[4] - current_pat[3]

        moves = [XA, AB, BC, CD]

        XA = moves[0]
        AB = moves[1]
        BC = moves[2]
        CD = moves[3]
                    
        AB_range = np.array([.618 - err_allowed, .618 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        ## === Bulish Gartley === ## 
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                self.b_g_signal = 'Buy' 
                self.b_g_relevence = 1 
                print('Detected Bullish Gartley')
            else:
                pass

        ## === Bearish Gartley === ## 
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                self.b_g_signal = 'Sell' 
                self.b_g_relevence = -1 
                print('Detected Bearish Gartley')
            else:
                pass

        else:
            self.b_g_signal = 'Flay' 
            self.b_g_relevence = 0 
            print('No Harmonic Pattern Detected')
            

        


