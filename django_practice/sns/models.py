from django.db import models
from django.contrib.auth.models import User


# Messageクラス
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_owner')
    content = models.TextField(max_length=1000)
    share_id = models.IntegerField(default=0)   # share先のid。デフォルトは自分。
    good_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content) + ' (' + str(self.owner) + ')'
    
    def get_share(self):
        return Message.objects.get(id=self.share_id)
    
    class Meta:
        ordering = ('-pub_date',)
    

# Goodクラス
class Good(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='good_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return 'good for "' + str(self.message) + '" (by' + str(self.owner) + ')'
    

# Followingクラス
class Following(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_owner')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_target')

    def __str__(self):
        return '<' + str(self.owner) + ' is following ' + str(self.target) + '>'
    

# Profile_textクラス
class Profile_text(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_text_owner')
    content = models.TextField(max_length=1000)