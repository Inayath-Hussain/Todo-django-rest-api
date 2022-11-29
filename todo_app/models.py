from django.utils import timezone
from django.db import models
from django.conf import settings

# Create your models here.


def one_week_since():
    return timezone.now() + timezone.timedelta(days=7)


class TodoItemManager(models.Manager):
    def status_order(self, *args, **kwargs):
        qs = self.get_queryset().filter(*args, **kwargs)
        qs = qs.annotate(
            custom_order=models.Case(
                models.When(status=TodoItem.task_status_1,
                            then=models.Value(0)),
                models.When(status=TodoItem.task_status_2,
                            then=models.Value(1)),
                output_field=models.IntegerField()
            )
        ).order_by('custom_order')
        return qs


class TodoItem(models.Model):
    task_status_1 = 'P'
    task_status_2 = 'C'
    STATUS = [
        (task_status_1, 'Pending'),
        (task_status_2, 'Completed')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=one_week_since)
    status = models.CharField(
        max_length=1, choices=STATUS, default=task_status_1)

    objects = TodoItemManager()
