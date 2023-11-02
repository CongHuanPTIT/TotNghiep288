from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Video


# Create your views here.

# def index(request):                                   This index view was made at the start for developing purpose,
#     return render(request, 'videos/index.html')       now we can delete it and add in an actual index class view.


class Index(ListView):
    model = Video
    template_name = 'videos/index.html'
    order_by = '-date_posted'                   # Date posted sort by negative => Most recent uploads on top


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail']
    template_name = 'videos/create_video.html'

    # After hitting "Upload", validate the form data before the user do anything
    def form_valid(self, form):
        form.instance.uploader = self.request.user          # Set the uploader to be current logged in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})


class DetailVideo(DetailView):
    model = Video
    template_name = 'videos/detail_video.html'


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'thumbnail']
    template_name = 'videos/update_video.html'

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()                           # If the uploader and the logged in user is the same
        return self.request.user == video.uploader          # only then does the user gets to execute


class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('index')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader
