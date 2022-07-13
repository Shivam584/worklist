from celery import shared_task
from time import sleep
from django.core.mail import send_mail


@shared_task
def sleepy(duariton):
    sleep(duariton)
    return None


@shared_task
def send_mail_task(username,useremail,title,desc):
    send_mail(
        'This is reminder mail of Task '+title,
                'Hi ' + username + "!  "+ desc,
                '',
                [useremail],
                fail_silently = False,
            )
    print("MAIL FROM CELERY")
    return None

