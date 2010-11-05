'''
Created on Nov 5, 2010

@author: jtk
'''

# Adjust the ladder to account for the match winner and loser.  Return True if the challenger won,
# which means there should be another match (unless challenger is now number one).
def adjustLadder(ladder, winner, loser):
    if winner not in ladder:
        ladder.append(winner)
    if loser not in ladder:
        ladder.append(loser)
    wIndex = ladder.index(winner)
    lIndex = ladder.index(loser)
#    assert abs(wIndex - lIndex) == 1
    if wIndex < lIndex:
        return False
    else:
        (ladder[wIndex], ladder[lIndex]) = (ladder[lIndex], ladder[wIndex])
        return True
        