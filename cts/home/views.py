from django.conf import settings
from django.shortcuts import render

from .forms import ContactForm
from .tasks import mail_task


def home(request):
    return render(request, 'home/home_page.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cts_mail = 'ctsadmin@conservationtechnologysolutions.org'
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message'] + '\n\nName: {}\nSender: {}'.format(name, sender)

            cc_myself = form.cleaned_data['cc_myself']

            recipients = [cts_mail]
            if cc_myself:
                recipients.append(sender)
            mail_task.delay(subject, message, cts_mail, recipients)
            return render(request, 'home/thankyou.html', {
                'name': name,
            })
    else:
        form = ContactForm()

    return render(request, 'home/contact_us.html', {
        'form': form,
    })


def mission(request):
    return render(request, 'home/mission.html')

# Testing out the Get Shit Done bootstrap package
if settings.DEBUG:
    def components(request):
        return render(request, 'home/components.html')

    def index(request):
        return render(request, 'home/index.html')

    def navbar(request):
        return render(request, 'home/navbar-transparent.html')


    def notification(request):
        return render(request, 'home/notification.html')


    def template(request):
        return render(request, 'home/template.html')


    def tutorial(request):
        return render(request, 'home/tutorial.html')


def dash_example_1_view(request, template_name="home/demo_six.html", **kwargs):
    context = {}
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['django_to_dash_context'] = "I am Dash receiving context from Django"
    request.session['django_plotly_dash'] = dash_context

    return render(request, template_name=template_name, context=context)


def session_state_view(request, template_name, **kwargs):
    'Example view that exhibits the use of sessions to store state'

    session = request.session

    demo_count = session.get('django_plotly_dash', {})

    ind_use = demo_count.get('ind_use', 0)
    ind_use += 1
    demo_count['ind_use'] = ind_use

    context = {'ind_use' : ind_use}

    session['django_plotly_dash'] = demo_count

    return render(request, template_name=template_name, context=context)
