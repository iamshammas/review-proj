from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Review, Advisor, Reviewer
from .forms import ReviewForm, ReviewUpdateForm
import datetime

@login_required
def dashboard(request):
    if request.user.is_staff:
        return coordinator_dashboard(request)
    else:
        return advisor_dashboard(request)

@login_required
@staff_member_required
def coordinator_dashboard(request):
    # Get filter parameters
    date_filter = request.GET.get('date', '')
    advisor_filter = request.GET.get('advisor', '')
    reviewer_filter = request.GET.get('reviewer', '')
    status_filter = request.GET.get('status', '')
    
    # Start with all reviews
    reviews = Review.objects.all()
    
    # Apply filters
    if date_filter:
        reviews = reviews.filter(date=date_filter)
    if advisor_filter:
        reviews = reviews.filter(intern__advisor_id=advisor_filter)
    if reviewer_filter:
        reviews = reviews.filter(assigned_reviewer_id=reviewer_filter)
    if status_filter:
        reviews = reviews.filter(status=status_filter)
    
    context = {
        'reviews': reviews,
        'advisors': Advisor.objects.all(),
        'reviewers': Reviewer.objects.all(),
        'date_filter': date_filter,
        'advisor_filter': advisor_filter,
        'reviewer_filter': reviewer_filter,
        'status_filter': status_filter,
    }
    return render(request, 'coordinator/dashboard.html', context)

@login_required
def advisor_dashboard(request):
    advisor = request.user.advisor
    date_filter = request.GET.get('date', '')
    
    reviews = Review.objects.filter(intern__advisor=advisor)
    if date_filter:
        reviews = reviews.filter(date=date_filter)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.created_by = request.user
            review.save()
            return redirect('dashboard')
    else:
        form = ReviewForm(user=request.user)
    
    return render(request, 'advisor/dashboard.html', {
        'reviews': reviews,
        'form': form,
        'date_filter': date_filter,
    })

@login_required
@staff_member_required
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        form = ReviewUpdateForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ReviewUpdateForm(instance=review)
    
    return render(request, 'coordinator/update_review.html', {
        'form': form,
        'review': review,
    })

@login_required
@staff_member_required
def reporting(request):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    count = None
    
    if start_date and end_date:
        count = Review.objects.filter(
            date__range=[start_date, end_date]
        ).count()
    
    return render(request, 'coordinator/reporting.html', {
        'start_date': start_date,
        'end_date': end_date,
        'count': count,
    })

def generate_notification(request):
    review_ids = request.GET.getlist('review_ids[]')
    target = request.GET.get('target')  # 'advisor' or 'reviewer'
    
    reviews = Review.objects.filter(id__in=review_ids).order_by('start_time')
    
    if not reviews.exists():
        return JsonResponse({'error': 'No reviews selected'}, status=400)
    
    date = reviews[0].date
    text = f"Reviews on {date}\n\n"
    
    for review in reviews:
        if target == 'advisor':
            text += f"Intern: {review.intern.name}\n"
            text += f"Reviewer: {review.assigned_reviewer.name if review.assigned_reviewer else 'Not assigned'}\n"
        elif target == 'reviewer':
            text += f"Intern: {review.intern.name}\n"
            text += f"Lesson: {review.lesson.name}\n"
        
        text += f"Google Meet: {review.google_meet_link if review.google_meet_link else 'Link not set'}\n"
        text += f"Time: {review.start_time.strftime('%I:%M %p') if review.start_time else 'Time not set'}\n\n"
    
    return JsonResponse({'text': text})