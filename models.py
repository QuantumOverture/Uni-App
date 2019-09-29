from django.db import models


class UniComment(models.Model):
    Comment = models.TextField()
    StarRating = models.SmallIntegerField()
    UniID = models.CharField(max_length=100)
    CommentID = models.CharField(max_length=100,default='')
