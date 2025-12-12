from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
from .models import Review, Advisor, Reviewer
from django.contrib.auth import logout
from .forms import AdvisorReviewForm, ReviewUpdateForm
# import datetime
from datetime import date
from django.utils.timezone import now

def register(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(first_name=name,username=username,password=password)
        if user is not None:
            # Advisor.objects.create(user=name)
            user.save()
            return redirect('login')
    # return render(request, 'register.html')
    return render(request,'registration/register.html')

def user_logout(request):
    logout(request)
    return redirect('dashboard')

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
    today = date.today().strftime('%Y-%m-%d')
    date_filter = request.GET.get('date', today)
    advisor_filter = request.GET.get('advisor', '')
    reviewer_filter = request.GET.get('reviewer', '')
    status_filter = request.GET.get('status', '')
    
    # Start with all reviews
    reviews = Review.objects.all()
    
    # Apply filters
    if date_filter:
        reviews = reviews.filter(date=date_filter)
    if advisor_filter:
        reviews = reviews.filter(created_by_id=advisor_filter)  # Changed this line
    if reviewer_filter:
        reviews = reviews.filter(assigned_reviewer_id=reviewer_filter)
    if status_filter:
        reviews = reviews.filter(status=status_filter)
    
    context = {
        'reviews': reviews,
        'advisors': User.objects.filter(is_superuser=False),
        'reviewers': Reviewer.objects.all(),
        'date_filter': date_filter,
        'today': today,
        'advisor_filter': advisor_filter,
        'reviewer_filter': reviewer_filter,
        'status_filter': status_filter,
    }
    return render(request, 'coordinator/dashboard.html', context)

@login_required
def advisor_dashboard(request):
    date_filter = request.GET.get('date', '')
    
    # Get only reviews created by this advisor
    reviews = Review.objects.filter(created_by=request.user)
    if date_filter:
        reviews = reviews.filter(date=date_filter)
    
    if request.method == 'POST':
        form = AdvisorReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.created_by = request.user
            review.save()
            return redirect('dashboard')
    else:
        form = AdvisorReviewForm()
    
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
    text = f"Reviews on {date}\n"
    text += f'-------------------------\n'
    for review in reviews:
        if target == 'advisor':
            text += f"Intern: {review.intern_name}\n"
            text += f"Reviewer: {review.assigned_reviewer.name if review.assigned_reviewer else 'Not assigned'}\n"
        elif target == 'reviewer':
            text += f"Intern: {review.intern_name}\n"
            text += f"Week: {review.lesson_name}\n"
        text += f"Google Meet: {review.google_meet_link if review.google_meet_link else 'Link not set'}\n"
        text += f"Time: {review.start_time.strftime('%I:%M %p') if review.start_time else 'Time not set'}\n"
        text += f'-------------------------\n'
    
    return JsonResponse({'text': text})





def add_reviewer(request):
    count = Reviewer.objects.count()
    context = {
        'count':count
    }
    if request.method == 'POST':
        reviewer = request.POST.get('reviewerName')
        stack = request.POST.get('stack')
        us = Reviewer.objects.create(name=reviewer,stack=stack)
        if us is not None:
            us.save()
            return redirect('dashboard')
    return render(request,'coordinator/add_reviewer.html',context)
    # return HttpResponse('worked')



def remarks(request,review_id):
    review = get_object_or_404(Review, id=review_id)
    data = {
        'review':review
    }
    return render(request,'coordinator/remarks.html',data)

def feedback(request,review_id):
    review = get_object_or_404(Review,id=review_id)
    if request.method == 'POST':
        review.feedback = request.POST.get('feedback')
        review.save()
        return redirect('dashboard')
    return render(request,'coordinator/feedback.html',{'review':review})