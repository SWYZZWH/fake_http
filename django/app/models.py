from django.db import models

# Create your models here.
class student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="photos/")
    

    def __str__(self):
        return str(self.id) + self.name + str(self.photo.null)

    