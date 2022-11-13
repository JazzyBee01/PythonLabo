

def printList(list, listname=""):
    print(f'{listname} ({len(list)}): ')
    print('\t',end="")
    for item in list:
        print(f'{item}; ',end="")
    print('\n')


def printSRD(styleRuleDict):
    for selector in styleRuleDict.keys():
        print(selector)
        for rule in styleRuleDict[selector]:
            print("\t" + rule)