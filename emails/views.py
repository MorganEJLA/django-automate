from django.shortcuts import render, redirect, get_object_or_404

from .tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber, Email, Sent
from django.db.models import Sum
# Create your views here.
def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            #send an email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = email.email_list
            #Access the selected email list
            email_list = email.email_list
            #Extract email addresses from the subscribers' model
            subscribers = Subscriber.objects.filter(email_list=email_list)

            to_email = [email.email_address for email in subscribers]

            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            email_id = email.id
            # handover email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment, email_id)

            #display a success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
    else:
        email = EmailForm()
        context = {
            'email_form': email,
        }
        return render(request, 'emails/send_email.html', context)

def track_click(request):
    #Logic to store the tracking info
    return

def track_open(request):
    #Logic to store opening info
    return

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent'))
    context = {
        'emails':emails,
    }
    return render(request, 'emails/track_dashboard.html', context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email': email,
        'total_sent':sent.total_sent,
    }
    return render(request, 'emails/track_stats.html', context)
