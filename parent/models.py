from django.db import models

# Create your models here.


class ParentName(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.first_name

class ChildName(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    dob = models.DateField()

    # relationship
    parent = models.ForeignKey(ParentName, on_delete=models.CASCADE)
# This example assumes there is only one parent and multiple children.

    def __str__(self):
        return self.first_name

