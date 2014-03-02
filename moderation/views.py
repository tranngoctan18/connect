import crypt, time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.timezone import now

from .forms import InviteMemberForm
from .models import UserRegistration, ModerationLogMsg
from .utils import generate_html_email


def hash_time():
    """
    Return a unique 30 character string based on the
    current timestamp. The returned string will consist
    of alphanumeric characters (A-Z, a-z, 0-9) only.
    """
    hashed = ''
    salt = '$1$O2xqbWD9'

    for pos in [-22, -8]:
        hashed += (crypt.crypt(str(time.time()), salt)[pos:].replace('/', '0')
                                                            .replace('.', '0'))
    return hashed


def create_token(user):
    """
    Create an authentication token for a user to activate their account.
    """


    return '123456'



@login_required
def invite_member(request):
    """
    Allow a moderator to invite a new member to the system.
    """
    moderator = request.user
    site = get_current_site(request)

    if request.method == 'POST':
        form = InviteMemberForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = hash_time()
            user_emails = [user.email for user in User.objects.all() if user.email]

            if email not in user_emails:

                # Create inactive user with unusable password
                new_user = User.objects.create_user(username, email)

                new_user.is_active = False
                new_user.first_name = first_name
                new_user.last_name = last_name

                new_user.save()

                # Add user registration details
                user_registration = UserRegistration.objects.create(
                    user=new_user,
                    method=UserRegistration.INVITED,
                    moderator=moderator,
                    approved_datetime=now(),
                    auth_token = create_token(new_user) # generate auth token
                )

                # Log invitation in moderation logs
                log = ModerationLogMsg.objects.create(
                    msg_type=ModerationLogMsg.INVITATION,
                    comment='{} invited by {}'.format(
                        new_user.get_full_name(),
                        moderator.get_full_name()
                    ),
                    pertains_to=new_user,
                    logged_by=moderator
                )

                # Send invitation email to new user
                subject = 'Welcome to '+ site.name
                recipient = new_user

                template_vars = {
                    'recipient': recipient,
                    'site_name': site.name,
                    'activation_url': '{}/{}'.format(settings.SITE_URL,
                                            user_registration.auth_token),
                    'inviter': moderator,
                }

                email = generate_html_email(
                    subject,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    'moderation/emails/invite_new_user.html',
                    template_vars,
                )

                email.send()

            return redirect(reverse('moderators:moderators'))

    else:
        form = InviteMemberForm()

    # Show pending invitations
    # i.e if users are not active AND have not set their passwords
    pending = User.objects.filter(userregistration__moderator=moderator,
                                  userregistration__auth_token_is_used=False,
                                  is_active=False)

    context = {
        'form' : form,
        'pending' : pending,
    }

    return render(request, 'moderation/invite_member.html', context)


@login_required
def review_applications(request):
    context = ''
    return render(request, 'moderation/review_applications.html', context)


@login_required
def review_abuse(request):
    context = ''
    return render(request, 'moderation/review_abuse.html', context)


@login_required
def view_logs(request):

    logs = ModerationLogMsg.objects.all()

    context = {'logs': logs }
    return render(request, 'moderation/logs.html', context)
