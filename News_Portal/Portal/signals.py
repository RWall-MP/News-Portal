from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.id
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category}'

    text_content = (
        f'Пост: {instance.title}\n'
        f'Содержание: {instance.text}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Пост: {instance.title}<br>'
        f'Содержание: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на пост</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
