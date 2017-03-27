#----------------------------------------------------------------------
# Author:            Brian Wolf
# Date:              2009.12.31
# Module:            utils.py
# Description:       Utility functions.
#
# Modifications:
#
#
#----------------------------------------------------------------------


class Utils:
    def __init__(self):
        self.COLORS = ["#F1F1F1", "#E4E8F5"]
        self.MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        self.PAYMENT_METHODS = dict(
            chk='Check',
            csh='Cash',
            cc='Credit Card',
            pp='PayPal',
            ach='ACH',
            eck='eCheck',
            oth='Other',
            amz='Amazon',
        )


    def getRadioValues(self, key, params):
        values = []
        for k,v in params.items():
            if k == key:
                values.append(v)
        return values


    def _fmt(self, s, sep):
        if len(s) <= 3: return s
        return self._fmt(s[:-3], sep) + sep + s[-3:]


    def fmt(self, s, sep=','):
        # format number by inserting comma at thousands
        if s is None: return ''
        if type(s) is not type(''): s = str(s)
        parts = s.split('.')
        sl = [self._fmt(parts[0], sep)]
        if len(parts) == 2: sl.append(parts[1][:2])
        return '.'.join(sl)


    def get_value(self, filename, key):
        # get value from configuration file given a key
        with open(filename, 'r') as f:
            for line in f:
                if key in line:
                    return line.strip().replace(' ','').split('=')[1]
