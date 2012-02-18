from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('checkApp.views',

    url(r'^view/(\d+)/', 'viewList', name='viewList'),
    url(r'^taskDone/', 'taskDone', name='taskDone'),
    url(r'^createTask/', 'createTask', name='createTask'),
    url(r'^createCheckList/', 'createCheckList', name='createCheckList'),
    url(r'^', 'index', name='index'),
)
