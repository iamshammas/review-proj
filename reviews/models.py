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
def create_user_profile(sender, instance, created, **kwargs):
    # Create Advisor profile only for regular users, not staff/superusers
    if created and not instance.is_staff:
        Advisor.objects.create(user=instance)

class Reviewer(models.Model):
    name = models.CharField(max_length=100)
    stack = models.CharField(max_length=100, blank=True)
    
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
    intern_name = models.CharField(max_length=100)
    lesson_name = models.CharField(max_length=200)
    preferred_reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='preferred_reviews')
    assigned_reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='assigned_reviews')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True, help_text="Additional comments or notes about the review")
    
    def __str__(self):
        return f"{self.intern_name} - {self.lesson_name} - {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']