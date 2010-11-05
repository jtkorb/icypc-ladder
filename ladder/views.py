from models import Result, Challenger
#from django.http import HttpResponse
#from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response 
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from datetime import datetime
from ladderadjust import adjustLadder

def index(request):
    results_list = Result.objects.all()
    challengers_list = Challenger.objects.all()
#    template = loader.get_template('ladder/index.html')
#    context = Context({'results_list' : results_list,})
#    return HttpResponse(", ".join((r.winnerUser for r in results)))
#    return HttpResponse(template.render(context))

    ladder = []
    for result in results_list:
        winner = (result.winnerUser, result.winnerPlayer)
        loser = (result.loserUser, result.loserPlayer)
        adjustLadder(ladder, winner, loser)
    for r in ladder:
        print 'r = ' + r[0] + ' ' + r[1]

    return render_to_response('ladder/index.html', 
                              {'results_list': results_list,
                               'challengers_list': challengers_list,
                               'ladder_list': ladder},
                              context_instance=RequestContext(request))

def challenge(request):
    userid = request.POST['userid']
    player = request.POST['player']
    c = Challenger(time=datetime.now(), user=userid, player=player)
    c.save()
    return HttpResponseRedirect('/ladder/')
