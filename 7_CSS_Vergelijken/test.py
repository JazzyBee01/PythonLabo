import cssutils
from colored import fg, bg, attr
import os
os.system('color')
key = cssutils.parseFile('key.css', validate=False)

comments = key.cssRules.rulesOfType(1001)
for rule in comments:
    print(rule)
    comments = key.cssRules.rulesOfType(1001)
print('\n')
for rule in comments:
    print(rule)

ok = fg("green")
res = attr('reset')

print(ok + 'hello'+ res )