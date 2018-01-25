SYSTEM_APP_LOGIN = '/system/login/'
VIEWER_APP_LOGIN = '/merchants/login/'

def is_crew(user):
    return user.groups.filter(name='Crew').exists()

def is_merchant(user):
    return user.groups.filter(name='Merchant').exists()
