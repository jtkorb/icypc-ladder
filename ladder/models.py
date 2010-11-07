from django.db import models

def executable(user, player):
    return '~' + user + '/icypc/' + player

class Challenger(models.Model):
    '''
    >>> from datetime import datetime
    >>> c1 = Challenger.objects.create(time=datetime.now(), user='jtk', player='hunter')
    >>> c1.__unicode__().split(' ')[2]
    '~jtk/icypc/hunter'
    '''
    time = models.DateTimeField('time challenged')
    user = models.CharField(max_length=10)
    player = models.CharField(max_length=20)
    def __unicode__(self):
        return self.time.__str__() + ' ' + executable(self.user, self.player)


class Result(models.Model):
    time = models.DateTimeField('time played')
    winnerUser = models.CharField(max_length=10)
    winnerPlayer = models.CharField(max_length=20)
    loserUser = models.CharField(max_length=10)
    loserPlayer = models.CharField(max_length=20)
    def __unicode__(self):
        return self.time.__str__() + ' ' + executable(self.winnerUser, self.winnerPlayer) + ' over ' + executable(self.loserUser, self.loserPlayer)
