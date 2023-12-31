from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse, render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from .forms import CommentForm
from .models import Video, Comment, Topic


# Create your views here.

# def index(request):                                   This index view was made at the start for developing purpose,
#     return render(request, 'videos/index.html')       now we can delete it and add in an actual index class view.


class Index(ListView):
    model = Video
    template_name = 'videos/index.html'
    ordering = '-date_posted'  # Date posted sort by negative => Most recent uploads on top


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail', 'topic']
    template_name = 'videos/create_video.html'

    # After hitting "Upload", validate the form data before the user do anything
    def form_valid(self, form):
        form.instance.uploader = self.request.user  # Set the uploader to be current logged in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})


# class DetailVideo(DetailView):                            With the comments in play,
#     model = Video                                         redo this entire view
#     template_name = 'videos/detail_video.html'

class DetailVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        topics = Video.objects.filter(topic=video.topic)[:20]
        context = {
            'object': video,
            'comments': comments,
            'topics': topics,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(user=self.request.user,
                              comment=form.cleaned_data['comment'],
                              video=video)
            comment.save()

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        topics = Video.objects.filter(topic=video.topic)[:20]
        context = {
            'object': video,
            'comments': comments,
            'topics': topics,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)

    # This function is not working
    def delete(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)
        form = CommentForm(request.GET)
        if form.is_valid():
            comment = Comment(user=self.request.user,
                              comment=form.cleaned_data['comment'],
                              video=video)
            comment.delete()

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        context = {
            'object': video,
            'comments': comments
        }
        return render(request, 'videos/detail_video.html', context)


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description', 'thumbnail', 'topic']
    template_name = 'videos/update_video.html'

    def get_success_url(self):
        return reverse('video_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()                   # If the uploader and the logged in user is the same
        return self.request.user == video.uploader  # only then does the user gets to execute


class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('index')

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


class TopicVideo(View):
    def get(self, request, pk, *args, **kwargs):
        topic = Topic.objects.get(pk=pk)
        videos = Video.objects.filter(topic=pk).order_by('-date_posted')
        context = {
            'topic': topic,
            'videos': videos
        }
        return render(request, 'videos/similar_videos.html', context)


class SearchVideo(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        query_list = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(uploader__username__icontains=query)
        )

        context = {
            'query_list': query_list
        }
        return render(request, 'videos/search_video.html', context)
