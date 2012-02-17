from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('checkApp.views',

    url(r'^view/(\d+)/', 'viewList', name='viewList'),
    url(r'^taskDone/', 'taskDone', name='taskDone'),
    url(r'^createCheckItem/', 'createTask', name='createTask'),
    url(r'^', 'index', name='index'),
)
