from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta


def grab_active_users(model):
    return model.objects.filter(is_active=True).aggregate(Count('id'))['id__count']

def grab_total_users(model):
    return model.objects.all().aggregate(Count('id'))['id__count']

def grab_registered_users(model, interval):
    qs = model.objects.all()
    if interval.lower() == 'day':
        return len([user for user in qs if user.date_joined.astimezone(timezone.utc).replace(tzinfo=None) >= datetime.now()-timedelta(days=1)])
    elif interval.lower() == 'week':
        return len([user for user in qs if user.date_joined.astimezone(timezone.utc).replace(tzinfo=None) >= datetime.now()-timedelta(weeks=1)])
    elif interval.lower() == 'month':
        return len([user for user in qs if user.date_joined.astimezone(timezone.utc).replace(tzinfo=None) >= datetime.now()-timedelta(weeks=4)])
        
