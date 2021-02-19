from django.db import models
import random, string
# Create your models here.

def generate_unigue_code():
    lenght = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k = lenght))
        if Room.objects.filter(code = code).count() == 0:
            return code
    


class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unigue_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)