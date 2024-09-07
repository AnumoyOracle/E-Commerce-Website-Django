from django.db import models

# Create your models here.

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default="")
    head0 = models.CharField(max_length=200, default="")
    chead0 = models.CharField(max_length=10000, default="")
    head1 = models.CharField(max_length=200, default="")
    chead1 = models.CharField(max_length=10000, default="")
    head2 = models.CharField(max_length=200, default="")
    chead2 = models.CharField(max_length=10000, default="")
    pub_date = models.DateField()
    image = models.ImageField(upload_to="blog/img", default="") 

    def __str__(self):
        return self.title
