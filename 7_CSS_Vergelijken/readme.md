# Comparing CSS files

### Description

7_CSS.py takes 2 CSS files, parses them and outputs CSS code:

green: style rule found in both files
blue: "extra" style rules in test but not in key
red: "missing" stule rules in key but not in test

### Remarks
- this is pretty much spaghetti code. The desired output can also be achieved with just dictionary operations instead of unnecessarily complex classes.
- this code only takes style rules. Rules like media queries are not taken into accout
