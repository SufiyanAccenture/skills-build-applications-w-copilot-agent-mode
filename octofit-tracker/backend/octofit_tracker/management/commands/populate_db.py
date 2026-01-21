from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from pymongo import MongoClient
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users
        ironman = User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel)
        captain = User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel)
        batman = User.objects.create(name='Batman', email='batman@dc.com', team=dc)
        superman = User.objects.create(name='Superman', email='superman@dc.com', team=dc)

        # Activities
        Activity.objects.create(user=ironman, type='run', duration=30, date='2024-01-01')
        Activity.objects.create(user=batman, type='cycle', duration=45, date='2024-01-02')
        Activity.objects.create(user=superman, type='swim', duration=60, date='2024-01-03')
        Activity.objects.create(user=captain, type='walk', duration=20, date='2024-01-04')

        # Workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', suggested_for='all')
        Workout.objects.create(name='Situps', description='Do 30 situps', suggested_for='all')

        # Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        # Ensure unique index on email
        client = MongoClient('localhost', 27017)
        db = client[settings.DATABASES['default']['NAME']]
        db.users.create_index('email', unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data and unique index on email created.'))
