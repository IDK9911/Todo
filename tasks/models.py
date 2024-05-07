from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator,MinLengthValidator,MaxLengthValidator
from django.core.exceptions import ValidationError

import datetime
# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,null=False,blank=False)
    username = models.EmailField(max_length=30,null=False,blank=False,unique=True)
    password = models.CharField(max_length=100,default='p@ssw0rd123',null=False,validators=[MinLengthValidator(8)])

    def __str__(self):
        return f'user_id:{self.user_id},name={self.name},username={self.username}'

class Todo(models.Model):
    user = models.ForeignKey(User, default="1",on_delete=models.CASCADE)
    task_id = models.IntegerField(primary_key=True)
    task_desc = models.CharField(validators=[MinLengthValidator(3)],max_length=50,blank=True)
    task_deadline = models.DateTimeField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True)
    STATUS_CHOICES = [
        (0, 'Incomplete'),
        (1, 'Completed'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES,default=0)
    TAG_CHOICES = [
        ('0',''),
        ('health', 'Health'),
        ('study', 'Study'),
        ('fitness', 'Fitness'),
        ('errands', 'Errands'),
        ('mental_health', 'Mental Health'),
        ('academic', 'Academic'),
        ('professional', 'Professional'),
    ]
    tag = models.CharField(max_length=20, choices=TAG_CHOICES,default='health')
    slug=models.SlugField(default="",blank=True,null=False,unique=True,db_index=True) 
    #slug=models.SlugField(default="",blank=True) 
    #need to set this field to unique=True at some point later. 
    #All Attributes
    
    #dynamic url
    def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})
        return reverse("task_pg", args=[self.slug])

    #@Override
    def save(self,*args,**kwargs):
        self.slug=slugify(self.task_desc)
        self.last_edited=timezone.now()
        super().save(*args,**kwargs)

    def clean(self):
        if self.task_deadline.date() < timezone.now().date():
            raise ValidationError({'task_deadline': ['Task deadline must be a future date']})    

        elif self.task_deadline.date() == timezone.now().date():
            if self.task_deadline.time() == timezone.now().time():
                raise ValidationError({'task_deadline': ['Task deadline must be a future date or time']})    
    def __str__(self):
        return f"{self.task_id}.Task_desc:{self.task_desc},ctime:{self.created_time},etime:{self.last_edited}"
    

class SubTask(models.Model):
    subtask_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(Todo, on_delete=models.CASCADE)  # Foreign key referencing Todo's task_id
    subtask_desc = models.CharField(validators=[MinLengthValidator(4)],max_length=65)
    #parent_id = models.IntegerField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        (0, 'Incomplete'),
        (1, 'Completed'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES,default=0)


    def __str__(self):
        return f"SubTask {self.subtask_id} Subtask_Desc {self.subtask_desc}"