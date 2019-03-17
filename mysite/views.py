from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UserEditForm, ProfileEditForm,CommentForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin,ModelFormMixin
from .models import Profile, Contact, Category, Comment, Post
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count


def index(request):
    categorys = Category.objects.all()
    posts= Post.objects.all().filter(status__gt=0)[:10]
    post_hot = Post.objects.filter(status=2)[:5]
    post_pop = Post.objects.filter(status=3)
    real_hot = Post.objects.filter(status=1).order_by('-clicks')[:5]
    return render(request, 'index.html',
                  {
                      "categorys": categorys,
                      "posts": posts,
                      "post_hot": post_hot,
                      "post_pop": post_pop,
                      "real_hot": real_hot
                  })


@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/dashboard.html', {'profile': profile})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            Profile.objects.create(user=user)
            messages.success(request, '注册成功！')
            return redirect("/")
        else:
            return render(request, 'account/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'account/register.html', {'form': form})


@login_required
def profileedit(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '修改成功！')
            return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/pro_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class ProfileList(ListView):
    model = Profile
    template_name = 'follow/profile_list.html'
    context_object_name = 'profiles'
    object_list = Profile.objects.all()
    # 对用户按粉丝数排列
    queryset = object_list.annotate(fols=Count('followers')).order_by('-fols')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myself'] = Profile.objects.get(user=self.request.user)
        return context


class ProfileDetail(DetailView):
    model = Profile
    template_name = 'follow/profile_detail.html'


@require_POST
def user_like(request):
    fromid = request.POST.get('fromid')
    toid = request.POST.get('toid')
    action = request.POST.get('action')

    if fromid and toid and action:
        try:
            user_from = Profile.objects.get(id=fromid)
            user_to = Profile.objects.get(id=toid)
            if action == 'like':
                Contact.objects.create(user_from=user_from, user_to=user_to)
            else:
                contact = Contact.objects.get(user_from=user_from, user_to=user_to)
                contact.delete()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


def user_chk(request):
    username = request.GET.get('username')
    result = User.objects.filter(username=username)
    if result:
        return JsonResponse({
            'status': 'ko'
        })
    return JsonResponse({
        'status': 'ok'
    })


def catposts(request,id):
    cat = Category.objects.get(id=id)
    posts = cat.cat_posts.all()
    return render(request,'post/posts_list.html',{'posts':posts,'section':cat.title})

def authposts(request,id):
    auth = Profile.objects.get(id=id)
    posts = auth.pro_posts.all()
    return render(request, 'post/posts_list.html', {'posts': posts,'section':auth.user.get_username()})

class PostCreate(CreateView):
    model = Post
    fields = ('title','category','body','status')
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.instance.publish = timezone.now()
        return super().form_valid(form)

class PostDetail(FormMixin,DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    form_class = CommentForm

@require_POST
def post_comment(request):
    id = request.POST.get('id')
    body = request.POST.get('body')
    if id and body:
        try:
            user = request.user
            post = Post.objects.get(id=id)
            Comment.objects.create(user=user, post=post,body=body)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})