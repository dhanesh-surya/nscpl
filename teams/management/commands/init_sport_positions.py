from django.core.management.base import BaseCommand
from sports.models import Sport
from teams.models import SportPosition

class Command(BaseCommand):
    help = 'Initialize default positions for different sports'

    def handle(self, *args, **options):
        # Cricket positions
        cricket_positions = [
            ('BAT', 'Batsman'),
            ('BWL', 'Bowler'),
            ('AR', 'All-Rounder'),
            ('WK', 'Wicket-Keeper'),
            ('CAP', 'Captain'),
            ('VC', 'Vice-Captain'),
        ]

        # Football positions
        football_positions = [
            ('GK', 'Goalkeeper'),
            ('DEF', 'Defender'),
            ('MID', 'Midfielder'),
            ('FWD', 'Forward'),
            ('CAP', 'Captain'),
        ]

        # Basketball positions
        basketball_positions = [
            ('PG', 'Point Guard'),
            ('SG', 'Shooting Guard'),
            ('SF', 'Small Forward'),
            ('PF', 'Power Forward'),
            ('C', 'Center'),
            ('CAP', 'Captain'),
        ]

        # Create positions for each sport
        sports_positions = {
            'Cricket': cricket_positions,
            'Football': football_positions,
            'Basketball': basketball_positions,
        }

        for sport_name, positions in sports_positions.items():
            try:
                sport = Sport.objects.get(name__iexact=sport_name)
                for code, name in positions:
                    SportPosition.objects.get_or_create(
                        sport=sport,
                        code=code,
                        defaults={'name': name}
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully created positions for {sport_name}'))
            except Sport.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Sport {sport_name} not found'))