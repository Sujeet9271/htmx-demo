from datetime import datetime
import random
import string
from django.core.management.base import BaseCommand

from accounts.models import Users



def generate_random_string(length):
    # Generate a string containing both letters and digits
    characters = string.ascii_letters + string.digits
    # Shuffle the characters
    random_characters = ''.join(random.sample(characters, len(characters)))
    # Take the first 6 characters to get a random 6-letter string
    random_string = random_characters[:length]
    return random_string


class Command(BaseCommand):
    help = 'Create Users'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--num', type=int, help='Number of Records', default=100)
  
  
    def handle(self, *args, **kwargs):
        num = kwargs.get('num')
        create_list=[]
        for _ in range(num):
            create_list.append(Users(name=generate_random_string(10)))
        Users.objects.bulk_create(create_list,batch_size=1000)
        return 'Users Created'


        