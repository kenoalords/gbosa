from __future__ import absolute_import
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from app.models import Post, Answer, PsuedoUser, Upvote, Comment, Region, Subscribe
from app.forms import PostForm, AnswerForm, CommentForm, PsuedoUserForm
from django.utils.text import slugify
from faker import Faker
from utils.ip import view_log, ip_info, get_tags, view_log_entry
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from app.tasks import mailer, log_the_view
from django.core.exceptions import ObjectDoesNotExist
from taggit.models import Tag

faker = Faker()

class SocialLoginView(TemplateView):
    template_name = "parts/accounts/login.html"

# Class base Posts List View
class PostList(ListView):
    queryset = Post.objects.filter(is_published=True).order_by('-created_at').all()
    context_object_name = 'posts'
    template_name = './parts/index.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('p')
        post_list = paginator.get_page(page)
        context['posts'] = post_list
        return context

class UserPostList(ListView):
    template_name = './parts/posts/user_posts.html'
    paginate_by = 3
    context_object_name = "posts"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-created_at')



# Class Based Question Details View
class PostDetail(DetailView):
    model = Post
    form = AnswerForm
    template_name = './parts/posts/post.html'
    c_form = CommentForm
    is_subscribed = False
    ip_details = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'geoip' in self.request.session:
            self.ip_details = self.request.session['geoip']
        else:
            self.ip_details = ip_info()
            self.request.session['geoip'] = self.ip_details

        current_post = Post.objects.get(pk=self.kwargs['pk'])
        view_log_entry(current_post, self.ip_details)
        context['form'] = self.form
        context['c_form'] = self.c_form
        context['answers'] = Answer.by_upvotes.filter(post__pk=self.kwargs['pk'])
        return context

# Question add form view
@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = './parts/posts/add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.instance.title)
        if self.request.POST['status'] == 'publish':
            form.instance.is_published = True
            
        mailer.delay('Post created', 'A new post was created', ['kenoalords@gmail.com'])
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = './parts/posts/add.html'

@method_decorator(login_required, name="dispatch")
class PostDelete(DeleteView):
    pass

@method_decorator(login_required, name="dispatch")
class AnswerSubmit(SingleObjectMixin, View):
    model = Post
    def post(self, request, *args, **kwargs):
        answer = AnswerForm(request.POST)
        if answer.is_valid():
            query = answer.save(commit=False)
            query.user = request.user
            query.save()
        self.object = self.get_object()
        self.object.answers.add(query)
        self.object.save()
        return HttpResponseRedirect(reverse('app:view-post', kwargs={'pk': self.object.pk, 'slug': self.object.slug}))

@method_decorator(login_required, name="dispatch")
class CommentSubmit(SingleObjectMixin, View):
    model = Post

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            geo = ip_info()
            if geo:
                region = Region.objects.create(ip=geo['IPv4'], city=geo['city'], state=geo['state'], country_name= geo['country_name'], country_code= geo['country_code'], latitude=geo['latitude'], longitude=geo['longitude'])
                comment.region = region
            comment.save()

            self.object = self.get_object()
            self.object.comments.add(comment)
            self.object.save()
            return HttpResponseRedirect(reverse('app:view-post', kwargs={'pk': self.object.pk, 'slug': self.object.slug}))
        else:
            return HttpResponseRedirect(reverse('app:view-post', kwargs={'pk': self.object.pk, 'slug': self.object.slug}))

@method_decorator(login_required, name="dispatch")
class UpvoteSubmit(SingleObjectMixin, View):
    model = Answer

    def post(self, request, *args, **kwargs):
        geo = ip_info()
        region = Region.objects.create(ip=geo['IPv4'], city=geo['city'], state=geo['state'], country_name= geo['country_name'], country_code= geo['country_code'], latitude=geo['latitude'], longitude=geo['longitude'])
        upvote = Upvote.objects.create(user=request.user, region=region)
        self.object = self.get_object()
        self.object.upvotes.add(upvote)
        self.object.save()
        post = Post.objects.filter(answers__pk=self.object.pk)

        return HttpResponseRedirect(reverse('app:view-post', kwargs={'pk':post[0].pk, 'slug': post[0].slug}))

class TagList(ListView):
    # model = Tag
    template_name = "./parts/tags/tags.html"
    context_object_name = "posts"
    def get_queryset(self, **kwargs):
        return Post.objects.filter(tags__slug=self.kwargs['slug']).order_by('-created_at')

class PostTypeList(ListView):
    template_name = "./parts/posts/type.html"
    context_object_name = "posts"
    def get_queryset(self, **kwargs):
        return Post.objects.filter(post_type=self.kwargs['slug']).order_by('-created_at')

class SearchList(ListView):
    template_name = "./parts/search/search.html"
    context_object_name = "posts"
    def get_queryset(self):
        term = self.request.GET['q']
        query = SearchQuery(term)
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('tags__name', weight='C')
        return Post.objects.annotate( rank=SearchRank(vector, query) ).filter(rank__gte=0.3).distinct().order_by('-rank')

@method_decorator(login_required, name="dispatch")
class CommentLike(SingleObjectMixin, View):
    model = Post
    def post(self, request, *args, **kwargs):

        if int(request.POST['comment']) != int(self.kwargs['pk']):
            return HttpResponseRedirect(request.POST['_redirect'])

        ID = request.POST['comment']
        geo = ip_info()
        if geo:
            region = Region.objects.create(ip=geo['IPv4'], city=geo['city'], state=geo['state'], country_name= geo['country_name'], country_code= geo['country_code'], latitude=geo['latitude'], longitude=geo['longitude'])
        else:
            region = ''
        like = Upvote.objects.create(user=self.request.user, region=region)
        comment = Comment.objects.get(pk=ID)
        comment.likes.add(like)
        comment.save()
        # Return response
        return HttpResponseRedirect(request.POST['_redirect'])

@method_decorator(login_required, name="dispatch")
class Subscribers(SingleObjectMixin, View):
    model = Post
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        subscribe = Subscribe.objects.create(user=request.user)
        self.object.subscribers.add(subscribe)
        self.object.save()
        return HttpResponseRedirect(reverse("app:view-post", kwargs={'pk':self.object.pk, 'slug':self.object.slug}))

# Psuedo User Form
class PsuedoCreate(FormView):
    model = PsuedoUser
    form_class = PsuedoUserForm
    template_name = './parts/accounts/psuedo_name_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        psuedouser = PsuedoUser.objects.filter(user=self.request.user).first()
        if psuedouser:
            psuedouser.first_name = form.instance.first_name
            psuedouser.last_name = form.instance.last_name
            psuedouser.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form.instance.user = self.request.user
            form.instance.save()
            return super().form_valid(form)

    def get_initial(self):
        try:
            psuedonym = self.request.user.psuedouser
            return {'first_name': psuedonym.first_name, 'last_name': psuedonym.last_name}
        except:
            return {'first_name': faker.first_name(), 'last_name': faker.last_name()}
            # pass

# Get tags from db
@login_required()
def tagSuggestions(request):
    # tags = Tag.objects.filter(name__icontains=request.POST.get('t'))
    pass


# Logout User
@login_required()
def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
