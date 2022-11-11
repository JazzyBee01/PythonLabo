import cssutils
from dataclasses import dataclass
from colored import fg, bg, attr
import os
os.system('color')

ok = fg("green")
extra = fg("blue")
missing = fg("red")
res = attr('reset')


def printList(list, listname=""):
    print(f'{listname} ({len(list)}): ')
    print('\t',end="")
    for item in list:
        print(f'{item}; ',end="")
    print('\n')

class CSSComparator:
    """ def __init__(self, keyfile, testfile):
        self.file1 = keyfile
        #self.file2 = testFile """
    
    def parse(self, cssFilename):
        StyleSheet = cssutils.parseFile(cssFilename, validate=False)
        return StyleSheet
    def printRules(self, ruleList):
        for rule in ruleList:
            print(rule)
    def printSelectors(self,stylesheet):
        for rule in stylesheet.cssRules:
            print(rule.selectorText)

@dataclass
class Match:
    match: int #match percentage
    matching: list
    extra: list
    missing: list

@dataclass
class SelectorMatch:
    match: int #match percentage
    matching: dict
    extra: dict
    missing: dict




def getStyleRuledict(stylesheet):   
    styleRuleDict = {}

    ## stijl lijnen per selector in dict opslaan
    for rule in stylesheet.cssRules.rulesOfType(1):
        lines = rule.style.cssText.split('\n')
        if rule.selectorText in styleRuleDict.keys():
            for line in lines:
                styleRuleDict[rule.selectorText].append(line)
        else:
            styleRuleDict[rule.selectorText] = lines
    
    return styleRuleDict

def printSRD(styleRuleDict):
    for selector in styleRuleDict.keys():
        print(selector)
        for rule in styleRuleDict[selector]:
            print("\t" + rule)

def collectSelectors(stylesheet):
    selectors = []
    
    #collect key selectors
    for rule in stylesheet.cssRules.rulesOfType(1):
        if rule.selectorText not in selectors:
            """ if ',' in rule.selectorText:
                s = rule.selectorText.split(',')
                for el in s:
                    keySelectors.append(el)
            else: """
            selectors.append(rule.selectorText)
    #collect test selectors
    return selectors


def compareLists(keySelectorList, testSelectorList):
    #keySelectors = collectSelectors(key)
    #testSelectors = collectSelectors(test)
    missing = []
    extra = []
    matching = []



    #collect matching and extra
    for selector in testSelectorList:
        if selector in keySelectorList:
            matching.append(selector)
        else:
            extra.append(selector)
    #collect missing
    for selector in keySelectorList:
        if selector not in testSelectorList:
            missing.append(selector)

    matchpercentage = len(matching)/(len(extra) + len(missing) + len(matching)) * 100

    return Match(matchpercentage, matching, extra, missing)


def compareStyleRules(key, test):
    keySRD = getStyleRuledict(key)
    testSRD = getStyleRuledict(test)
    matching = {}
    extra = {}
    missing = {}

    lines = 0
    correct_lines = 0


    selectorComp = compareLists(collectSelectors(key),collectSelectors(test))


    for s in selectorComp.matching:
        cl = compareLists(keySRD[s], testSRD[s])
        matching[s] = Match( cl.match, cl.matching, cl.extra, cl.missing )
        
        lines += len(cl.matching) + len(cl.extra) + len(cl.missing)
        correct_lines += len(cl.matching)

    for s in selectorComp.extra:
        extra[s] = testSRD[s]
        lines += len(testSRD)
    
    for s in selectorComp.missing:
        missing[s] = keySRD[s]
        lines += 1

    match = correct_lines/lines * 100
    print(correct_lines)
    print(lines)


    return SelectorMatch(match,matching, extra, missing)

    


    comparisonDict = {} #{ test_selector: {state: extra, match: , extra_lines: [] , lines_missing []  }, test_selector: {} }
    #op basis van state en extra enz in kleur weergeven

    print('key')
    printSRD(keySRD)
    print('test')
    printSRD(testSRD)

if __name__ == "__main__":
    APP = CSSComparator()

    key = APP.parse('lab4-oplossingen/oef5/stijl.css')
    test = APP.parse('L4/oef5/stijl.css')

    #APP.printRules(key.cssRules)
    """ 
    styleRules = key.cssRules.rulesOfType(1)
    mediaRules = key.cssRules.rulesOfType(4)
    comments = key.cssRules.rulesOfType(1001) """

    #compareSelectors(key,test)

    csr = compareStyleRules(key, test)
    #print(csr)
    #print(csr.matching["header"])

    percentageSelectorsMatched = compareLists(collectSelectors(key), collectSelectors(test)).match
    print(f'{percentageSelectorsMatched:.0f}% of the found selectors match.')
    print(f'{csr.match:.0f}% of all style rules match')
    print()
    print("green: same as in key file")
    print("blue:  found in test file but not present in keyfile.")
    print("red:   missing from test file.")

    print()
  

    for s in csr.matching.keys():
        selector = csr.matching[s]
        col = ok
        print(f'{col}{s} \t(match: {selector.match:.0f}%) {res}')
        for line in selector.matching:
            col = ok
            print(f'\t{col}{line}{res}')
        for line in selector.extra:
            col = extra
            print(f'\t{col}{line}{res}')
        for line in selector.missing:
            col = missing
            print(f'\t{col}{line}{res}')

        print()
    for selector in csr.extra.keys():
        col = extra
        print(f'{col}{selector}{res}')
        for line in csr.extra[selector]:
            print(f'\t{col}{line}{res}')
        print()

    for selector in csr.missing.keys():
        col = missing
        print(f'{col}{selector}{res}')
        for line in csr.missing[selector]:
            print(f'\t{col}{line}{res}')
        print()


    
    









