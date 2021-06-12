from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Post(models.Model):
  shared_body = models.TextField(blank=True, null=True)
  body = models.TextField(blank=True, null=True, default='')
  image = models.ManyToManyField('Image', blank=True)
  created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  shared_on = models.DateTimeField(blank=True, null=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  shared_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='+')
  likes = models.ManyToManyField(User, blank=True, related_name='likes')
  dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

  class Meta:
    ordering = ['-created_on', '-shared_on']

  def __str__(self):
      return self.body

class Image(models.Model):
  image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)


class Comment(models.Model):
  comment = models.TextField(blank=True, null=True, default='')
  created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
  post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True, null=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
  dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
  parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

  def __str__(self):
      return self.comment

  @property
  def children(self):
    return Comment.objects.filter(parent=self).order_by('-created_on').all()

  @property
  def is_parent(self):
    if self.parent is None:
      return True
    return False

class UserProfile(models.Model):
  user = models.OneToOneField(User, verbose_name=("user"), related_name='profile',  on_delete=models.CASCADE)
  name = models.CharField(max_length=50, blank=True, null=True)
  bio = models.TextField(max_length=500, blank=True, null=True)
  birth_date = models.DateField(null=True, blank=True)
  location = models.CharField(max_length=50, blank=True, null=True)
  picture = models.ImageField(upload_to='uploads/profile_picture', default='uploads/profile_pictures/default.png', height_field=None, width_field=None, max_length=None, blank=True)
  followers = models.ManyToManyField(User, blank=True, related_name='followers')

  def __str__(self):
      return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Notification(models.Model):
  notification_type = models.IntegerField(blank=True, null=True)
  to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
  from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
  post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
  comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
  thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
  date = models.DateTimeField(auto_now=False, auto_now_add=True)
  user_has_seen = models.BooleanField(default=False)

class ThreadModel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  has_read = models.BooleanField(default=False)

class MessageModel(models.Model):
  thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
  sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
  body = models.CharField(max_length=1000)
  image = models.ImageField(upload_to=' ', blank=True, null=True)
  date = models.DateTimeField(auto_now=False, auto_now_add=True)
  is_read = models.BooleanField(default=False)
