from CS390CP.ladder.models import Result
#from django.http import HttpResponse
#from django.template import Context, loader
from django.shortcuts import render_to_response 

def index(request):
    results_list = Result.objects.all()
#    template = loader.get_template('ladder/index.html')
#    context = Context({'results_list' : results_list,})
#    return HttpResponse(", ".join((r.winnerUser for r in results)))
#    return HttpResponse(template.render(context))
    return render_to_response('ladder/index.html', {'results_list': results_list,})
