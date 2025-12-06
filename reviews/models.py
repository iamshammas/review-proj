from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Advisor.objects.create(user=instance)
    instance.advisor.save()

class Reviewer(models.Model):
    name = models.CharField(max_length=100)
    stack = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class Intern(models.Model):
    name = models.CharField(max_length=100)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='interns')
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    google_meet_link = models.URLField(blank=True)
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    preferred_reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='preferred_reviews')
    assigned_reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='assigned_reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.intern.name} - {self.lesson.name} - {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']