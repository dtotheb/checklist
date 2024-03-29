from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('checkApp.views',

    url(r'^view/(\d+)/', 'viewList', name='viewList'),
    url(r'^taskDone/', 'taskDone', name='taskDone'),
    url(r'^createTask/', 'createTask', name='createTask'),
    url(r'^createCheckList/', 'createCheckList', name='createCheckList'),
    url(r'^deleteCheckList/', 'deleteCheckList', name="deleteCheckList"),
    url(r'^viewTemplates/', 'viewTemplates', name="viewTemplates"),
    url(r'^startCheckList', 'startCheckList', name='startCheckList'),
    url(r'^startTemplate', 'startTemplate', name='startTemplate'),
    url(r'^login/', 'login_view', name='login'),
    url(r'^logout/', 'logout_view', name='logout'),
    url(r'^', 'index', name='index'),
)
