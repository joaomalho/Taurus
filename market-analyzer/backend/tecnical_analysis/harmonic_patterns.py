import numpy as np

class HarmonicPatterns:
    """
    Detect all candlestick patterns using TA-Lib.
    """

    def __init__(self):
        self

    def get_gartley_hp(self, moves, err_allowed):
        """
        Definition of Gartley Harmonic Pattern and targets
        """
        XA = moves[0]
        AB = moves[1]
        BC = moves[2]
        CD = moves[3]
                    
        AB_range = np.array([.618 - err_allowed, .618 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None
        }

        ## === Bulish Butterfly === ## 
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D + (C - D) * 1.618

                return 1, targets
            else:
                return np.nan, targets

        ## === Bearish Butterfly === ## 
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D - (D - C) * 1.618

                return -1, targets
            else:
                return np.nan, targets
        else:
            return np.NAN
        

    def get_bat_hp(self, moves, err_allowed):
        """
        Definition of Bat Harmonic Pattern and targets
        """
        XA = moves[0]
        AB = moves[1]
        BC = moves[2]
        CD = moves[3]
                    
        AB_range = np.array([.382 - err_allowed, .5 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

        # AD = XA + AB + BC + CD
        # AD_expected = 0.886 * abs(XA)

        # if abs(abs(AD) - AD_expected) < err_allowed * abs(XA):
        # # Ponto D válido!

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None
        }

        ## === Bulish Butterfly === ## 
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D + (C - D) * 1.618

                return 1, targets
            else:
                return np.nan, targets

        ## === Bearish Butterfly === ## 
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D - (D - C) * 1.618

                return -1, targets
            else:
                return np.nan, targets
        else:
            return np.NAN 
        

    def get_butterfly_hp(self, moves, err_allowed):
        """
        Definition of Butterfly Harmonic Pattern and targets
        """
        XA = moves[0]
        AB = moves[1]
        BC = moves[2]
        CD = moves[3]
                    
        AB_range = np.array([.786 - err_allowed, .786 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(XA) # abs(BC) Inicialmente

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None
        }

        ## === Bulish Butterfly === ## 
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D + (C - D) * 1.618  # extensão para cima

                return 1, targets
            else:
                return np.nan, targets

        ## === Bearish Butterfly === ## 
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA
                targets["AB"] = AB
                targets["BC"] = BC
                targets["CD"] = CD

                D = XA + AB + BC + CD
                C = XA + AB + BC
                B = XA + AB

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D - (D - C) * 1.618  # extensão para baixo

                return -1, targets
            else:
                return np.nan, targets
        else:
            return np.NAN
        
    def get_crab_hp(self, moves, err_allowed):
            
        XA = moves[0]
        AB = moves[1]
        BC = moves[2]
        CD = moves[3]
                    
        AB_range = np.array([.382 - err_allowed, .618 + err_allowed]) * abs(XA)
        BC_range = np.array([.382 - err_allowed, .886 + err_allowed]) * abs(AB)
        CD_range = np.array([2.24 - err_allowed, 3.618 + err_allowed]) * abs(XA) # abs(BC) Inicialmente

        targets = {
            "XA": None,
            "AB": None,
            "BC": None,
            "CD": None,
            "TP1": None,
            "TP2": None,
            "TP3": None,
        }

        ## === Bulish Butterfly === ## 
        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA # 3rd Target
                targets["AB"] = AB # 1st Target
                targets["BC"] = BC # 2nd Target
                targets["CD"] = CD # Last Break Point

                D = moves[0] + moves[1] + moves[2] + moves[3]
                C = moves[0] + moves[1] + moves[2]
                B = moves[0] + moves[1]

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D + (C - D) * 1.618
                
                return 1, targets # Buy
            else:
                return np.NAN, targets

        ## === Bearish Butterfly === ## 
        elif XA < 0 and AB > 0 and BC < 0 and CD > 0:

            if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
                targets["XA"] = XA # 3rd Target
                targets["AB"] = AB # 1st Target
                targets["BC"] = BC # 2nd Target
                targets["CD"] = CD # Last Break Ppint

                D = moves[0] + moves[1] + moves[2] + moves[3]
                C = moves[0] + moves[1] + moves[2]
                B = moves[0] + moves[1]

                targets["TP1"] = B
                targets["TP2"] = C
                targets["TP3"] = D - (D - C) * 1.618
                
                return -1, targets
            else:
                return np.NAN, targets
        else:
            return np.NAN, targets