
# Create the project directory
mkdir tutorial
cd tutorial

# Create a virtualenv to isolate our package dependencies locally
virtualenv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install Django and Django REST framework into the virtualenv
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin.py startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin.py startapp quickstart
cd ..

Now sync your database for the first time:

python manage.py migrate

We'll also create an initial user named admin with a password of password123. We'll authenticate as that user later in our example.

python manage.py createsuperuser

Once you've set up a database and initial user created and ready to go, open up the app's directory and we'll get coding...
Serializers

First up we're going to define some serializers. Let's create a new module named tutorial/quickstart/serializers.py that we'll use for our data representations.

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

Notice that we're using hyperlinked relations in this case, with HyperlinkedModelSerializer. You can also use primary key and various other relationships, but hyperlinking is good RESTful design.
Views

Right, we'd better write some views then. Open tutorial/quickstart/views.py and get typing.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

Rather than write multiple views we're grouping together all the common behavior into classes called ViewSets.

We can easily break these down into individual views if we need to, but using viewsets keeps the view logic nicely organized as well as being very concise.
URLs

Okay, now let's wire up the API URLs. On to tutorial/urls.py...

from django.conf.urls import url, include
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

Because we're using viewsets instead of views, we can automatically generate the URL conf for our API, by simply registering the viewsets with a router class.

Again, if we need more control over the API URLs we can simply drop down to using regular class based views, and writing the URL conf explicitly.

Finally, we're including default login and logout views for use with the browsable API. That's optional, but useful if your API requires authentication and you want to use the browsable API.
Settings

We'd also like to set a few global settings. We'd like to turn on pagination, and we want our API to only be accessible to admin users. The settings module will be in tutorial/settings.py

INSTALLED_APPS = (
    ...
    'rest_framework',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 10
}
