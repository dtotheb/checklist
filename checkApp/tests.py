"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from checkApp.models import CheckList, CheckItem
from django.core import serializers
from django.utils import simplejson


class CheckTestHelper(object):
    def create_checklist(self, *args, **kwargs):
        id = CheckList.objects.all().count()
        defaults = {
            'name':'test',
            'creator':'tester'
        }
        defaults.update(kwargs)
        return CheckList.objects.create(**defaults)

    def create_checkItem(self, *args, **kwargs):
        id = CheckItem.objects.all().count()
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
        else:
            pk = 1
        defaults = {
            'text' : 'test this',
            'done' : False,
            'checkList' : CheckList.objects.get(id=pk)
        }
        return CheckItem.objects.create(**defaults)

    def setupCheckList(self):
        CheckTestHelper.create_checklist(self)
        CheckTestHelper.create_checkItem(self, text='test1')
        CheckTestHelper.create_checkItem(self, text='test2')


class IndexPageTestCase(CheckTestHelper,TestCase):
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('index')


    def test_pageLoads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/index.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list',context)

class viewListTestCase(CheckTestHelper,TestCase):
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('viewList', args=[1])

    def test_pageLoads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'checkApp/viewList.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list',context)
        items = context['list'].items.all()
        self.assertEqual(items.count(),2)


class checkItemDoneTestCase(CheckTestHelper,TestCase):
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('checkItemDone')

    def test_post(self):
        response = self.client.post(self.url,data={'pk':1,'val': 'true'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code,200)

        item = simplejson.loads(response.content)[0]
        self.assertEqual(item['pk'],1)
        self.assertEqual(item['model'],'checkApp.checkitem')
        self.assertEqual(item['fields']['done'], False)


class createCheckItemTestCase(CheckTestHelper,TestCase):
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('createCheckItem')

    def test_post(self):
        itemsTotalBefore = CheckItem.objects.all().count()
        response = self.client.post(self.url,data={'pk':1,'text':'test'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code,200)
        itemsTotalAfter = CheckItem.objects.all().count()
        self.assertEqual(itemsTotalBefore+1,itemsTotalAfter)

