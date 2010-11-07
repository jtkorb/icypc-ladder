'''
Created on Nov 5, 2010

@author: jtk
'''

# Adjust the ladder to account for the match winner and loser.  Return True if the match did
# not result in any change to the ladder, indicating that no further matches are necessary.
def adjustLadder(ladder, winner, loser):
    if winner not in ladder:
        ladder.append(winner)
    if loser not in ladder:
        ladder.append(loser)
    wIndex = ladder.index(winner)
    lIndex = ladder.index(loser)
#    assert abs(wIndex - lIndex) == 1
    if wIndex < lIndex:
        return True
    else:
        (ladder[wIndex], ladder[lIndex]) = (ladder[lIndex], ladder[wIndex])
        return False
        
def buildLadder(results_list):
    ladder = []
    for result in results_list:
        winner = (result.winnerUser, result.winnerPlayer)
        loser = (result.loserUser, result.loserPlayer)
        adjustLadder(ladder, winner, loser)
    for r in ladder:
        print 'r = ' + r[0] + ' ' + r[1]
    return ladder
