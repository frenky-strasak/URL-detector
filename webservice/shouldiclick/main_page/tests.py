from django.test import TestCase

# Create your tests here.
import sys

sys.path.insert(0, '.....')

from database.request_queue_db import print_file


print_file()