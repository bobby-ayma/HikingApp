from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from HikingApp.view_mixins import GroupRequiredMixin
from .forms.forms import HikeCreateForm, FilterForm
from .forms.forms import DeleteHikeForm
from .models import Hike, Like


def extract_filter_values(params):
    order = params['order'] if 'order' in params else FilterForm.ORDER_ASC
    text = params['text'] if 'text' in params else ''

    return {
        'order': order,
        'text': text,
    }


class IndexView(ListView):
    template_name = 'index.html'
    model = Hike
    context_object_name = 'hikes'  # not sure
    order_by_asc = True
    order_by = 'name'
    contains_text = ''

    def dispatch(self, request, *args, **kwargs):
        params = extract_filter_values(request.GET)
        # self.order_by_asc = params['order'] == FilterForm.ORDER_ASC
        self.order_by = params['order']
        self.contains_text = params['text']
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        order_by = 'name' if self.order_by == FilterForm.ORDER_ASC else '-name'
        result = self.model.objects.filter(name__icontains=self.contains_text).order_by(order_by)

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = FilterForm(initial={
            'order': self.order_by,
            'text': self.contains_text
        })

        return context


def hike_details(request, pk, slug=None):
    hike = Hike.objects.get(pk=pk)
    if slug and hike.name.lower() != slug.lower():
        return redirect('404')
    context = {
        'hike': hike,
    }

    return render(request, 'hikes/hiike_description.html', context)  # to be changed


class HikeCreateView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    form_class = HikeCreateForm
    template_name = 'create.html'
    success_url = reverse_lazy('index')
    groups = ['User']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# TO BE PUT IN COMMON
def get_hike(pk):
    return Hike.objects.get(pk=pk)


def persist_hike(request, hike, template_name):
    if request.method == 'GET':
        form = HikeCreateForm(instance=hike)

        context = {
            'form': form,
            'hike': hike,
        }
        return render(request, f'{template_name}.html', context)
    else:
        form = HikeCreateForm(
            request.POST,
            instance=hike
        )
        if form.is_valid():
            form.save()
            return redirect('index')

        context = {
            'form': form,
            'hike': hike,
        }
        return render(request, f'{template_name}.html', context)


# view to edit hikes
def edit_hike(request, pk):
    hike = get_hike(pk)
    return persist_hike(request, hike, 'hikes/edit')


# view to delete hikes
def delete_hike(request, pk):
    hike = get_hike(pk)
    if request.method == 'GET':
        context = {
            'hike': hike,
            'form': DeleteHikeForm(instance=hike),
        }

        return render(request, 'hikes/delete.html', context)
    else:
        hike.delete()
        return redirect('index')

#like functionality for hikes on the index page

def like_hike(request, pk):
    hike = Hike.objects.get(pk=pk)
    like = Like(definition='as')
    like.hike = hike
    like.save()
    return redirect('index')