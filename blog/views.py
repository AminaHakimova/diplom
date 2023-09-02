from django.db.models import Count
from django.shortcuts import render
from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from pytils.translit import slugify

from .models.like.models import Like
from .models.comment.models import Comment
from .models.post.models import Post
from .models.tag.models import Tag
from .models.image.models import Image

from blog.forms import LoginUserForm, RegisterUserForm, PostAddForm


class PostListView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "index.html", context={
            'posts': Post.objects.filter(status=Post.PUBLISHED),
            'tags': Tag.objects.all()
        })


class PostCreateView(View):

    def get(self, request):
        return render(request, 'create.html', context={
            'form': PostAddForm()
        })

    def post(self, request, *args, **kwargs):
        post = Post.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            status=Post.DRAFT,
            author=request.user,
            slug=slugify(request.POST['title'])
        )
        index_main_foto = request.POST['main_foto']
        for name, foto in request.FILES.items():
            Image.objects.create(
                image=foto,
                current=index_main_foto == name[-1],
                post=post
            )
        tags = [Tag.objects.get(id=tag_id) for tag_id in
                request.POST.getlist('tags')]
        post.tags.set(tags)
        return redirect("home")


class PostFilterView(View):

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(status=Post.PUBLISHED)
        if request.GET.get("tag_option"):
            queryset = queryset.filter(tags__id=request.GET.get("tag_option"))
        like = request.GET.get("like_option")
        if like == "more":
            queryset = queryset.annotate(
                count_likes=Count('likes_post')).order_by('-count_likes')
        elif like == "small":
            queryset = queryset.annotate(
                count_likes=Count('likes_post')).order_by('count_likes')
        return render(request, "index.html", context={
            'posts': queryset,
            'tags': Tag.objects.all()
        })


class PostUserFilterView(View):

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(author=request.user)
        if request.GET.get("filter_option"):
            queryset = queryset.filter(status=request.GET.get("filter_option"))
        return render(request, "user.html", context={
            'posts': queryset,
        })


def logout_user(request):
    """Log out"""
    logout(request)
    return redirect('home')


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserView(View):
    def get(self, request):
        return render(request, "user.html", context={
            'posts': Post.objects.filter(author=request.user),
        })


class PostDetailView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        like = None
        if request.user.is_authenticated:
            like = Like.objects.filter(author=request.user, post=post)
        return render(request, "detail.html", context={
            "post": post,
            "comments": Comment.objects.filter(post=post),
            "like": like
        })


class CommentsCreateView(View):

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.POST['comment']:
            Comment.objects.create(
                title=request.POST['comment'],
                author=request.user,
                post=post
            )
        return redirect('detail', post.pk)


class LikeCreateView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        like = Like.objects.filter(author=request.user, post=post)
        if not like:
            Like.objects.create(
                author=request.user,
                post=post
            )
        else:
            like.first().delete()
        return redirect('detail', post.pk)
