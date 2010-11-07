'''
Created on Nov 7, 2010

@author: jtk
'''
if __name__ == '__main__':
    import subprocess
    import re
    import os.path
    red = os.path.expanduser('~jtk/icypc/hunter')
    blue = os.path.expanduser('~jtk/icypc/planter')
    command = ['java', '-jar', '../icypc.jar', '-player', 'pipe', '1', red, '-player', 'pipe', '1', blue, '-view', 'trace', 'trace.txt']
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = p.communicate()[0];
    print '=====\n' + output + '\n====='
    pattern = re.compile(r'Winner: (\d+)')
    match = pattern.match(output)
    if match is None:
        print "no match"
    else:
        print 'winner is', match.group(1) 
