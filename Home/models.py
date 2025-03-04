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
    name = models.TextField(null=True, blank=True)
    email_id = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
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