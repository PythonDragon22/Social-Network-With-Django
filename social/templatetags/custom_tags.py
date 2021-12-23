from django import template
from social.models import Notification

register = template.Library()


@register.inclusion_tag('social/show_notifications.html', takes_context=True)
def show_notifications(context):
    # get the current logged in user (the user who receives the notifications)
    request_user = context['request'].user

    # filter the notifications based on the receiver user that haven't been seen   (Display all user notifications
    # except that been seen)
    notifications = Notification.objects.filter(to_user=request_user).exclude(user_has_seen=True).order_by('-date')

    return {
        'notifications': notifications
    }

