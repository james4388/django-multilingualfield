import sys, os
REPO_ROOT = os.path.dirname( __file__ )
sys.path.append(REPO_ROOT)
sys.path.append(os.path.join(REPO_ROOT,'testproject'))

#Switch to newer Python on Dreamhost
if sys.version < "2.7.3": os.execl(os.path.join(REPO_ROOT,"env/bin/python"), "python2.7.3", *sys.argv)

sys.path.insert(0,os.path.join(REPO_ROOT,'env/bin'))
sys.path.insert(0,os.path.join(REPO_ROOT,'env/lib/python2.7/site-packages/django'))
sys.path.insert(0,os.path.join(REPO_ROOT,'env/lib/python2.7/site-packages'))
sys.path.insert(0,os.path.join(REPO_ROOT,'testproject'))
#Import app here
#sys.path.insert(0,os.path.join(REPO_ROOT,'app_name'))

os.environ['DJANGO_SETTINGS_MODULE'] = "testproject.settings"
from dbconfig import *

#Django settings
os.environ['SERVER_TYPE'] = "dreamhost"
os.environ['LC_ALL'] = "en_US.UTF-8"
os.environ['LANG'] = "en_US.UTF-8"

os.environ['APP_MODE'] = "prod"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
