from __future__ import absolute_import
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from app.models import Post, Answer, PsuedoUser, Upvote, Comment, Region, Subscribe
from app.forms import PostForm, PostFormExperience, PostFormQuestion, AnswerForm, CommentForm, PsuedoUserForm, FlagPostForm
from django.utils.text import slugify
# from faker import Faker
from utils.ip import view_log, ip_info, get_tags, view_log_entry
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import ObjectDoesNotExist
from taggit.models import Tag
from gbosa.decorators import current_user_is_owner, post_is_not_flagged, post_is_not_deleted
# from django.contrib.auth.mixins import

# Import signals
from app.signals import notifications

from app.faker_ng import fake
# faker = Faker()

# Class base Posts List View
class PostList(ListView):
    queryset = Post.objects.filter(is_published=True, is_flagged=False, is_deleted=False).order_by('-created_at')
    context_object_name = 'posts'
    template_name = './parts/index.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        paginator = Paginator(self.queryset, self.paginate_by)
        page = self.request.GET.get('p')
        post_list = paginator.get_page(page)
        context['posts'] = post_list
        return context

class UserPostList(ListView):
    template_name = './parts/posts/user_posts.html'
    paginate_by = 15
    context_object_name = "posts"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, is_deleted=False).order_by( '-is_flagged', '-created_at' )



# Class Based Question Details View
@method_decorator(post_is_not_flagged, name="dispatch")
@method_decorator(post_is_not_deleted, name="dispatch")
class PostDetail(DetailView):
    model = Post
    form = AnswerForm
    template_name = './parts/posts/post.html'
    c_form = CommentForm
    is_subscribed = False
    ip_details = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.ip_details = get_geoip_info(self.request)
        current_post = Post.objects.get(pk=self.kwargs['pk'])
        view_log_entry(current_post, self.ip_details)

        tags = [ tag.name for tag in current_post.tags.all() ]
        context['form'] = self.form
        context['c_form'] = self.c_form
        context['answers'] = Answer.by_upvotes.filter(post__pk=self.kwargs['pk'])
        context['related_posts'] = Post.objects.filter(tags__name__in=tags, is_published=True, is_flagged=False, is_deleted=False).exclude(pk=current_post.pk).distinct()
        return context

# Question add form view
@method_decorator(login_required, name='dispatch')
class PostCreateExperience(CreateView):
    model = Post
    form_class = PostFormExperience
    template_name = './parts/posts/add_experience.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_type = 'E'
        form.instance.slug = slugify(form.instance.title)
        if self.request.POST['status'] == 'Publish':
            form.instance.is_published = True
        else:
            form.instance.is_published = False
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostUpdateExperience(UpdateView):
    model = Post
    form_class = PostFormExperience
    template_name = './parts/posts/edit_e.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_type = 'E'
        form.instance.slug = slugify(form.instance.title)
        if self.request.POST['status'] == 'Publish':
            form.instance.is_published = True
        else:
            form.instance.is_published = False
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostCreateQuestion(CreateView):
    model = Post
    form_class = PostFormQuestion
    template_name = './parts/posts/add_question.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_type = 'Q'
        form.instance.slug = slugify(form.instance.title)
        if self.request.POST['status'] == 'Publish':
            form.instance.is_published = True
        else:
            form.instance.is_published = False
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
@method_decorator(current_user_is_owner, name="dispatch")
class PostUpdateQuestion(UpdateView):
    model = Post
    form_class = PostFormQuestion
    template_name = './parts/posts/edit.html'

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.post_type = "Q"
        if ( self.request.POST['status'] == 'Publish' ):
            form.instance.is_published = True
        else:
            form.instance.is_published = False
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
@method_decorator(current_user_is_owner, name="dispatch")
class PostDelete(DeleteView):
    model = Post
    template_name = './parts/posts/delete.html'
    def post(self, request, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.is_deleted = True
        post.save()
        return HttpResponseRedirect(reverse('user-posts'))

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
            geo = get_geoip_info(request)
            if geo:
                region = Region.objects.create(ip=geo['IPv4'], city=geo['city'], state=geo['state'], country_name= geo['country_name'], country_code= geo['country_code'], latitude=geo['latitude'], longitude=geo['longitude'])
                comment.region = region
            comment.save()

            self.object = self.get_object()
            self.object.comments.add(comment)
            self.object.save()
            notifications.send(sender=self.__class__, message="Someone commented on your post", user=self.object.user)
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
        return Post.objects.filter(tags__slug=self.kwargs['slug'], is_published=True, is_flagged=False, is_deleted=False).order_by('-created_at')

class PostTypeList(ListView):
    template_name = "./parts/posts/type.html"
    context_object_name = "posts"
    paginate_by = 3
    def get_queryset(self, **kwargs):
        return Post.objects.filter(post_type=self.kwargs['slug'], is_published=True, is_flagged=False, is_deleted=False).order_by('-created_at')

class SearchList(ListView):
    template_name = "./parts/search/search.html"
    context_object_name = "posts"
    def get_queryset(self):
        term = self.request.GET['q']
        query = SearchQuery(term)
        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('tags__name', weight='C')
        return Post.objects.annotate( rank=SearchRank(vector, query) ).filter(rank__gte=0.3, is_flagged=False, is_deleted=False).distinct().order_by('-rank')

@method_decorator(login_required, name="dispatch")
class CommentLike(SingleObjectMixin, View):
    model = Post
    ip_details = None
    region = None
    def post(self, request, *args, **kwargs):
        if int(request.POST['comment']) != int(self.kwargs['pk']):
            return HttpResponseRedirect(request.POST['_redirect'])

        ID = request.POST['comment']

        # Check if user has liked the comment
        # if they have, delete existing like and redirect
        has_liked = Upvote.objects.filter(comment__pk=ID, user=request.user)
        if has_liked.exists():
            has_liked.delete()
            return HttpResponseRedirect(request.POST['_redirect'])

        # Create the like object if user has not liked
        like = Upvote.objects.create(user=self.request.user)
        try:
            self.ip_details = get_geoip_info(request)
            region = Region.objects.create(ip=self.ip_details['IPv4'], city=self.ip_details['city'], state=self.ip_details['state'], country_name= self.ip_details['country_name'], country_code= self.ip_details['country_code'], latitude=self.ip_details['latitude'], longitude=self.ip_details['longitude'])
            like.region = region
        except:
            print('Error: Couldnt save region with comment like')
        comment = Comment.objects.get(pk=ID)
        like.save()
        comment.likes.add(like)
        comment.save()
        return HttpResponseRedirect(request.POST['_redirect'])

@method_decorator(login_required, name="dispatch")
class Subscribers(SingleObjectMixin, View):
    model = Post
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Check if user has subscribed
        is_user_subscribed = Subscribe.objects.filter(post__pk=self.object.pk, user=request.user)
        if is_user_subscribed.exists():
            is_user_subscribed.delete()
            return HttpResponseRedirect(reverse("app:view-post", kwargs={'pk':self.object.pk, 'slug':self.object.slug}))

        subscribe = Subscribe.objects.create(user=request.user)
        self.object.subscribers.add(subscribe)
        self.object.save()
        title = self.object.title
        user = request.user.first_name + ' ' + request.user.last_name
        total_followers = self.object.subscribers.count()
        notifications.send(self.__class__, message='{} is following your post: <strong>{}</strong>. You currently have {} follower(s)'.format(user, title, total_followers), user=self.object.user, link=reverse('app:view-post', kwargs={'pk':self.object.pk, 'slug':self.object.slug}))
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
            return {'first_name': fake.first_name(), 'last_name': fake.last_name()}
            # pass

# Flag post
class FlagPost(DetailView):
    model = Post
    template_name = './parts/posts/flag.html'
    context_object_name = 'post'
    form_class = FlagPostForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flag_form'] = self.form_class
        return context

    def post(self, request, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if request.POST['flagged_reason'] in ['abusive', 'offensive', 'lacks-credibility']:
            post.is_flagged = True
            post.flagged_reason = request.POST['flagged_reason']
            post.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect(reverse('app:flag-post', {'pk':post.pk}))

# Get tags from db
@login_required()
def search_tags_ajax(request):
    if request.is_ajax() and request.method == 'POST':
        text = request.POST.get('text')
        tags = serializers.serialize('json', Tag.objects.filter(name__icontains=text))
        return JsonResponse( {'tags': tags}, safe=False)
    else:
        return HttpResponseForbidden()

def get_geoip_info(request):
    ip_details = None
    if 'geoip' in request.session:
        ip_details = request.session['geoip']
    else:
        ip_details = ip_info()
        request.session['geoip'] = ip_details
    return ip_details


# Logout User
@login_required()
def account_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Custom error pages
def handler400(request):
    return render(request, 'errors/500.html', {})

def handler404(request):
    return render(request, 'errors/404.html', {})

def handler403(request):
    return render(request, 'errors/403.html', {})

def handler500(request):
    return render(request, 'errors/500.html', {})
