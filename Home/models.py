from django.db import models

# Create your models here.

class chatbot(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'chatbot'
    def __str__(self):
        return self.question[:50]  
    
class contact_us(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True)
    email_id = models.TextField(null=True)
    subject = models.CharField(max_length=50,null=True)
    message = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'contact_us'


class webiste_counter(models.Model):
    id = models.AutoField(primary_key=True)
    counter = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'webiste_counter'


class about_us(models.Model):
    about_id = models.AutoField(primary_key=True)
    about_full_name = models.CharField(max_length=30,null=True)
    about_email_id = models.TextField(null=True, blank=True)
    about_requirement = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'about_us'


class error_log(models.Model):
    id = models.AutoField(primary_key=True)
    method =models.TextField(null=True,blank=True)
    error =models.TextField(null=True,blank=True)
    error_date = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    user = models.TextField(null=True,blank=True)
    class Meta:
        db_table = 'error_log'