from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('checkApp.views',

    url(r'^view/(\d+)/', 'viewList', name='viewList'),
    url(r'^checkDone/', 'checkItemDone', name='checkItemDone'),
    url(r'^', 'index', name='index'),
)
