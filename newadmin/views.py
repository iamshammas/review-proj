from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from reviews.models import Reviewer
from django.contrib import messages
from django.http import HttpResponse
import re
# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pswd = request.POST.get('pswd')
        user = User.objects.create_superuser(username=uname,password=pswd)
        return redirect('reg')
    return render(request,'newadmin/register.html')

# data = [
#         "SIYAHUDHEEN_FLUTTER",
#         "IRSHAD_FLUTTER",
#         "AKHIL_FLUTTER",
#         "AJMAL_FLUTTER",
#         "JASSIM_FLUTTER",
#         "LIKHIN_FLUTTER",
#         "JUSTINE_FLUTTER",
#     ]

# def addlist(request):
#     Reviewer.objects.create(name=data,stack='FLUTTER')
#     return render(request,'newadmin/test.html')


# views.py


def addlist(request):
    context = {}
    
    if request.method == 'POST':
        stack = request.POST.get('stack', '').strip()
        names_input = request.POST.get('names', '').strip()
        
        # Validate inputs
        if not stack:
            messages.error(request, "Please select a stack")
            return render(request, 'newadmin/add_reviewers.html', context)
        
        if not names_input:
            messages.error(request, "Please enter at least one name")
            return render(request, 'newadmin/add_reviewers.html', context)
        
        # Parse names - handle multiple formats
        names_list = parse_names_input(names_input)
        
        if not names_list:
            messages.error(request, "No valid names found in the input")
            return render(request, 'newadmin/add_reviewers.html', context)
        
        # Remove duplicates (case-insensitive)
        unique_names = remove_duplicates(names_list)
        
        # Check for existing reviewers (optional - to avoid duplicates)
        existing_names = set(
            Reviewer.objects.filter(
                name__in=unique_names,
                stack=stack
            ).values_list('name', flat=True)
        )
        
        # Create only new reviewers
        new_names = [name for name in unique_names if name not in existing_names]
        
        if not new_names:
            messages.info(request, "All reviewers already exist for this stack")
            context['names'] = names_input
            context['stack'] = stack
        else:
            # Create reviewers in bulk
            reviewers = [
                Reviewer(name=name, stack=stack)
                for name in new_names
            ]
            
            Reviewer.objects.bulk_create(reviewers)
            
            success_message = f"Successfully added {len(reviewers)} reviewer(s)"
            if existing_names:
                success_message += f" (skipped {len(existing_names)} existing ones)"
            
            messages.success(request, success_message)
            context['added_count'] = len(reviewers)
            context['names'] = ''  # Clear the form
            context['stack'] = stack
    
    # Get recent reviewers for display
    context['recent_reviewers'] = Reviewer.objects.all()[:10]  # Last 10
    
    return render(request, 'newadmin/add_reviewers.html', context)

def parse_names_input(names_input):
    """Parse names from various input formats"""
    names_list = []
    
    # Split by newlines
    lines = names_input.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # If line contains commas, split by commas
        if ',' in line:
            comma_names = [name.strip() for name in line.split(',') if name.strip()]
            names_list.extend(comma_names)
        else:
            # Single name per line
            names_list.append(line)
    
    # Clean up names (remove extra spaces, ensure proper capitalization)
    cleaned_names = []
    for name in names_list:
        # Remove extra spaces and normalize
        name = re.sub(r'\s+', ' ', name.strip())
        # Basic capitalization (first letter of each word)
        name = ' '.join([word.capitalize() for word in name.split()])
        cleaned_names.append(name)
    
    return cleaned_names

def remove_duplicates(names_list):
    """Remove duplicate names (case-insensitive)"""
    seen = set()
    unique_names = []
    
    for name in names_list:
        name_lower = name.lower()
        if name_lower not in seen:
            seen.add(name_lower)
            unique_names.append(name)
    
    return unique_names

# Alternative: View for API/JSON input
def bulk_add_reviewers_api(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            stack = data.get('stack')
            names = data.get('names', [])
            
            if not stack or not names:
                return HttpResponse(
                    json.dumps({'error': 'Stack and names are required'}),
                    content_type='application/json',
                    status=400
                )
            
            # Create reviewers
            reviewers = [
                Reviewer(name=name, stack=stack)
                for name in names
            ]
            
            Reviewer.objects.bulk_create(reviewers)
            
            return HttpResponse(
                json.dumps({
                    'success': True,
                    'added_count': len(reviewers),
                    'message': f'Added {len(reviewers)} reviewers'
                }),
                content_type='application/json'
            )
            
        except json.JSONDecodeError:
            return HttpResponse(
                json.dumps({'error': 'Invalid JSON'}),
                content_type='application/json',
                status=400
            )
        except Exception as e:
            return HttpResponse(
                json.dumps({'error': str(e)}),
                content_type='application/json',
                status=500
            )
    
    return HttpResponse(
        json.dumps({'error': 'Method not allowed'}),
        content_type='application/json',
        status=405
    )