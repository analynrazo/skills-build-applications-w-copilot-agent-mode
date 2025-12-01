from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel, is_superhero=True),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel, is_superhero=True),
            User(name='Captain America', email='cap@marvel.com', team=marvel, is_superhero=True),
            User(name='Batman', email='batman@dc.com', team=dc, is_superhero=True),
            User(name='Superman', email='superman@dc.com', team=dc, is_superhero=True),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc, is_superhero=True),
        ]
        User.objects.bulk_create(users)

        # Create Workouts
        workout1 = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        workout2 = Workout.objects.create(name='Flight', description='Flying workout')
        workout1.suggested_for.add(marvel)
        workout2.suggested_for.add(dc)

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, points=300)
        Leaderboard.objects.create(team=dc, points=250)

        # Create Activities
        user_objs = list(User.objects.all())
        Activity.objects.create(user=user_objs[0], type='Swing', duration=30, date=timezone.now().date())
        Activity.objects.create(user=user_objs[3], type='Detective Work', duration=60, date=timezone.now().date())

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
