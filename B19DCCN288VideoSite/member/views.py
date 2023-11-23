from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Member
from videos.models import Video


# Create your views here.
class MemberView(View):
    def get(self, request, pk, *args, **kwargs):
        member = get_object_or_404(Member, pk=pk)
        member_videos = Video.objects.all().filter(uploader=member.user).order_by('-date_posted')

        context = {
            'member': member,
            'member_videos': member_videos
        }
        return render(request, 'member/member_profile.html', context)


class UpdateMemberView(UpdateView):
    model = Member
    fields = ['name', 'date_of_birth', 'other', 'profile_image']
    template_name = 'member/update.html'

    def form_valid(self, form):
        if not form.instance.profile_image:
            form.instance.profile_image = 'uploads/profile_images/default.jpg'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('member', kwargs={'pk': self.object.pk})
