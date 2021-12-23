from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from social.models import Post, PostImage, Comment, Notification, ThreadModel, MessageModel
from users.models import Profile
from social.forms import AddPostForm, AddCommentForm, ThreadForm, MessageForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def tweet_page(request):
    return render(request, 'social/tweet.html')

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # posts = Post.objects.all().order_by('-created_on')    # display all posts of all users
        logged_in_user = self.request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')  # display posts of persons that the logged in user follow

        post_form = AddPostForm()

        context = {
            'post_list': posts,
            'form': post_form
        }

        return render(request, 'social/home.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = self.request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')

        post_form = AddPostForm(request.POST, request.FILES)
        files = request.FILES.getlist("post_image")
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            # if there're tags ... add them
            new_post.create_tags()

            for f in files:
                img = PostImage(post_image=f)
                img.save()
                new_post.post_image.add(img)
            new_post.save()

            context = {
                'post_list': posts,
                'form': post_form
            }

            return render(request, 'social/home.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        comment_form = AddCommentForm()

        context = {
            'post': post,
            'comments': comments,
            'form': comment_form,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.commentator = request.user
            new_comment.save()

        # create post comment notifications       (when a user make a comment .. notify the post author)
        notification = Notification.objects.create(
            notification_type=2,
            to_user=post.author,
            from_user=request.user,
            post=post
        )

        context = {
            'post': post,
            'comments': comments,
            'form': comment_form
        }

        return render(request, 'social/post_detail.html', context)

class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(id=post_pk)
        parent_comment = Comment.objects.get(id=pk)
        form = AddCommentForm(request.POST)

        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.commentator = request.user
            my_form.post = post
            my_form.parent = parent_comment
            my_form.save()

            # create post comment notifications       (when a user make a comment .. notify the post author)
            notification = Notification.objects.create(
                notification_type=2,
                to_user=parent_comment.commentator,
                from_user=request.user,
                comment=parent_comment
            )

        return redirect('post_detail', pk=post_pk)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'social/post_update.html'
    form_class = AddPostForm

    def get_success_url(self):
        return reverse_lazy(
            'post_detail',
            kwargs={
                'pk': self.kwargs['post_pk']
            }
        )

    def test_func(self):  # built_in f() that comes with UserPassesTestMixin
        post = self.get_object()  # grab the post
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post_list')  # == get_success_url()

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'social/comment_update.html'
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse_lazy(
            'post_detail',
            kwargs={
                'pk': self.kwargs['post_pk']
            }
        )

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.commentator

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'post_detail',
            kwargs={
                'pk': self.kwargs['post_pk']
            }
        )

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.commentator

class AddFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # get the profile
        profile = Profile.objects.get(user_id=pk)
        # add followers to the ManyToMany Field (List)
        profile.followers.add(request.user)

        notification = Notification.objects.create(
            notification_type=3,
            to_user=profile.user,
            from_user=request.user
        )

        return redirect('user_profile_page', pk=profile.pk)

class RemoveFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user_id=pk)
        profile.followers.remove(request.user)

        return redirect('user_profile', pk=profile.pk)

class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)

        # When clicking dislike and a like is existing .. remove that like and make a dislike
        is_disliked = False
        dislikes = post.dislikes.all()
        for dislike in dislikes:
            if request.user == dislike:
                is_disliked = True
                break

        if is_disliked:
            post.dislikes.remove(request.user)

        # Just make a like ... created first
        # Initialization for users likes list (there is no users make likes to this post)
        is_liked = False
        # grab the likes list
        likes = post.likes.all()
        # loop through that list
        for like in likes:
            # if user make a like
            if request.user == like:
                # change the initialization to true (user make a like to post)
                is_liked = True
                # stop ...
                break

        if not is_liked:  # (if not is_liked) == (if is_liked == False)
            post.likes.add(request.user)

        if is_liked:  # (if is_liked) == (if is_liked == True)
            post.likes.remove(request.user)

        return redirect('post_detail', pk=post.pk)

class AddDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # grab the post you need to dislike it
        post = Post.objects.get(id=pk)

        # When clicking dislike and a like is existing .. remove that like   (Last Created)
        is_liked = False
        likes = post.likes.all()
        for like in likes:
            if request.user == like:
                is_liked = True
                break

        if is_liked:
            post.likes.remove(request.user)

        # Just make a dislike ... Created First
        # initialization value for the dislike users  [there is no users that disliked this post]
        is_disliked = False
        # grab the dislikes list of users
        dislikes = post.dislikes.all()
        # loop through that list
        for dislike in dislikes:
            # if the user in that list
            if request.user == dislike:
                # the value of the dislike users be True [there are users that disliked this post]
                is_disliked = True
                # stop ..!
                break

        # in case of there is no users disliked this post .. when click dislike btn , add them to dislikes list
        if not is_disliked:
            post.dislikes.add(request.user)

            notification = Notification.objects.create(
                notification_type=1,
                to_user=post.author,
                from_user=request.user,
                post=post
            )

        # in case of there are users disliked this post .. when click dislike btn , remove them to dislikes list
        if is_disliked:
            post.dislikes.remove(request.user)

        return redirect('post_detail', pk=post.pk)

class UserFollowersView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(user_id=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'social/user_followers.html', context)

class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(id=post_pk)
        comment = Comment.objects.get(id=pk)
        likes = comment.likes.all()

        is_disliked = False
        dislikes = comment.dislikes.all()
        for dislike in dislikes:
            if request.user == dislike:
                is_disliked = True
                break

        if is_disliked:
            comment.dislikes.remove(request.user)

        is_liked = False
        for like in likes:
            if request.user == like:
                is_liked = True
                break

        if not is_liked:
            comment.likes.add(request.user)

            notification = Notification.objects.create(
                notification_type=1,
                to_user=comment.commentator,
                from_user=request.user,
                comment=comment
            )

        if is_liked:
            comment.likes.remove(request.user)

        return redirect('post_detail', pk=post.pk)

class CommentDislikeView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(id=post_pk)
        comment = Comment.objects.get(id=pk)
        dislikes = comment.dislikes.all()

        is_liked = False
        likes = comment.likes.all()
        for like in likes:
            if request.user == like:
                is_liked = True
                break

        if is_liked:
            comment.likes.remove(request.user)

        is_disliked = False
        for dislike in dislikes:
            if request.user == dislike:
                is_disliked = True
                break

        if not is_disliked:
            comment.dislikes.add(request.user)

        if is_liked:
            comment.dislikes.remove(request.user)

        return redirect('post_detail', pk=post.pk)

class PostNotificationsView(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        notification = Notification.objects.get(pk=notification_pk)

        # Mark the notification as seen when the user click on it ...
        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', pk=post_pk)

class FollowNotificationsView(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        porofile = Profile.objects.get(pk=profile_pk)
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('user_profile', pk=profile_pk)

class ThreadNotificationView(View):
    def get(self, request, notification_pk, thread_pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=thread_pk)
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('thread', pk=thread_pk)

class ListThreadsView(View):
    def get(self, request, *args, **kwargs):

        threads = ThreadModel.objects.filter(
            Q(user=request.user) |
            Q(receiver=request.user)
        )

        context = {
            'threads': threads
        }

        return render(request, 'social/inbox.html', context)

class CreateThreadView(View):
    def get(self, request, *args, **kwargs):
        thread_form = ThreadForm()

        context = {
            'thread_form': thread_form
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        thread_form = ThreadForm(request.POST)
        username = request.POST.get('username')

        # Get The Receiver User
        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)

            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if thread_form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect('thread', pk=thread.pk)

        except:
            messages.error(request, 'invalid username')
            return redirect('create_thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        message_form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)

        context = {
            'message_form': message_form,
            'thread': thread,
            'message_list': message_list
        }

        return render(request, 'social/thread.html', context)

class CreateMessageView(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            myform = form.save(commit=False)
            myform.thread = thread
            myform.sender_user = request.user
            myform.receiver_user = receiver
            myform.save()

        # message = MessageModel(
        #     thread=thread,
        #     sender_user=request.user,
        #     receiver_user=receiver,
        #     body=request.POST.get('body')
        # )
        # message.save()

        notification = Notification.objects.create(
            notification_type=4,
            to_user=receiver,
            from_user=request.user,
            thread=thread
        )

        return redirect('thread', pk=pk)

