from django.contrib.auth.models import Group, Permission


# Create a new group
regular_users = Group.objects.create(name='regularUser')

# Assign permissions to the group
publish_permission = Permission.objects.get(codename='can_Add')
regular_users.permissions.add(publish_permission)