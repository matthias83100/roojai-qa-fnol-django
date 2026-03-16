from django.core.management.base import BaseCommand
from qa_dashboard.models import CustomUser

class Command(BaseCommand):
    help = 'Initialize test users (Top Management, Managers, and Agents)'

    def handle(self, *args, **options):
        password = 'password123'
        
        self.stdout.write('Initializing test users...')

        # 1. Create Top Management (Admin)
        top_manager, created = CustomUser.objects.get_or_create(
            username='topmanager',
            defaults={
                'email': 'top@example.com',
                'role': 'TOP_MANAGEMENT',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            top_manager.set_password(password)
            top_manager.save()
            self.stdout.write(self.style.SUCCESS(f'Created Top Manager: {top_manager.username}'))
        else:
            self.stdout.write(f'Top Manager {top_manager.username} already exists')

        # 2. Create Managers
        managers = []
        for i in range(1, 3):
            manager, created = CustomUser.objects.get_or_create(
                username=f'manager{i}',
                defaults={
                    'email': f'manager{i}@example.com',
                    'role': 'MANAGER',
                    'is_staff': True,
                    'manager': top_manager
                }
            )
            if created:
                manager.set_password(password)
                manager.save()
                self.stdout.write(self.style.SUCCESS(f'Created Manager: {manager.username}'))
            managers.append(manager)

        # 3. Create Agents
        for i in range(1, 7):
            # Assign agents to managers (1-3 to manager1, 4-6 to manager2)
            assigned_manager = managers[0] if i <= 3 else managers[1]
            
            agent, created = CustomUser.objects.get_or_create(
                username=f'agent{i}',
                defaults={
                    'email': f'agent{i}@example.com',
                    'role': 'AGENT',
                    'manager': assigned_manager
                }
            )
            if created:
                agent.set_password(password)
                agent.save()
                self.stdout.write(self.style.SUCCESS(f'Created Agent: {agent.username}'))

        self.stdout.write(self.style.SUCCESS('--- User initialization complete ---'))
