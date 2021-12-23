from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    body = models.TextField()
    post_image = models.ManyToManyField('PostImage', blank=True)
    created_on = models.DateTimeField(default=timezone.now)  # Set The Time When You Hit The Submit Btn.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    tags = models.ManyToManyField('Tag', blank=True)

    # handle tags
    def create_tags(self):
        # loop through every word inside the post body field
        for word in self.body.split():
            # if the first of any word inside the body contains '#'  >> This is #body
            if word[0] == '#':
                # the tag word starts from the first letter after '#' to the end of it , generally the second letter
                tag = Tag.objects.filter(name=word[1:])
                # if there're written tags in the post body
                if tag:
                    # add that tag(s) to the tags list
                    self.tags.add(tag.pk)
                # if there's no tag(s)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                # Save the Post
                self.save()


class PostImage(models.Model):
    post_image = models.ImageField(upload_to='post_image/', null=True, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_commentator')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commented_post')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class Notification(models.Model):
    notification_type = models.IntegerField()  # 1 == Like , 2 == Comment , 3 == Follow , 4 == DM
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from', null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')


class MessageModel(models.Model):
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length= 250)
    img = models.ImageField(upload_to='message/', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

