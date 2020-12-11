from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from HikingApp.view_mixins import GroupRequiredMixin
from .forms.forms import HikeCreateForm, FilterForm, CommentForm
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


def object_finder(h_id, u_id):
    all_likes = Like.objects.filter(hike__name__contains=h_id)
    if u_id not in all_likes:
        try:
            return [like for like in all_likes if like.user_id == u_id][0].id
        except:
            return 'create'
    else:
        return 'create'


def like_hike(request, pk):
    hike = Hike.objects.get(pk=pk)
    like = Like(definition='as', user=request.user)
    like.hike = hike
    test = object_finder(hike.name, request.user.id)
    if  test == 'create':
        like.save()
        return redirect('index')
    else:
        Like.objects.filter(id=int(test)).delete()
        return redirect('index')


# def add_comment_to_hike(request, pk):
#     hike = get_hike(pk)
#     if request.method == 'GET':
#         context = {
#             'hike': hike,
#             'form': CommentForm(instance=hike),
#         }
#         return render(request, 'hikes/add_comment_to_hike.html', context)
#     else:
#             form = CommentForm(
#                 request.POST,
#                 instance=hike
#             )
#             if form.is_valid():
#                 form.save()
#                 return redirect('hike details')
#
#             context = {
#                 'form': form,
#                 'hike': hike,
#             }
#             return render(request,'hikes/add_comment_to_hike.html', context)

def add_comment_to_hike(request, pk):
    hike = get_hike(pk)
    author = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.hike = hike
            comment.author = author
            comment.save()
            return redirect('hike details', pk=hike.pk)
    else:
        form = CommentForm()
    return render(request, 'hikes/add_comment_to_hike.html', {'form': form})


