from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from reports.models import Reports, Text

class IndexView(generic.TemplateView):
    template_name = 'reports/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        reports_list = Reports.objects.order_by('?')[:5]
        context['reports_list'] = reports_list
        return context


class ListView(generic.ListView):
    model = Reports
    template_name = 'reports/list.html'
    """
    def get_queryset(self):
        return Reports.objects.filter(pub_date__lte=timezone.now())[:10]
    """
    """
    def listing(request):
        reports_list = Reports.objects.all()
        paginator = Paginator(reports_list, 10)

        page = request.GET.get('page')
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)

        return render_to_response('list.html', {"reports": reports})
    """
    context_object_name = "reports_list"    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    paginate_by = 10




class DetailView(generic.DetailView):
    model = Reports
    template_name = 'reports/detail.html'
    def get_queryset(self):
        """
       # Excludes any reports that aren't published yet.
        """
        return Reports.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Reports
    template_name = 'reports/results.html'

def browsed(request, reports_id):
    p = get_object_or_404(Reports, pk=reports_id)
    try:
        selected_text = p.text_set.get(pk=request.POST['text'])
    except (KeyError, Text.DoesNotExist):
        # Redisplay form.
        return render(request, 'reports/detail.html', {
            'reports': p,
            'error_message': "You didn't select a Report.",
        })
    else:
        selected_text.browsed += 1
        selected_text.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reports:results', args=(p.id,)))
