"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from checkApp.models import CheckList, CheckItem



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


class IndexPageTestCase(CheckTestHelper,TestCase):
    def setUp(self):
        CheckTestHelper.create_checklist(self)
        CheckTestHelper.create_checkItem(self, text='test1')
        CheckTestHelper.create_checkItem(self, text='test2')
        self.url = reverse('index')


    def test_pageLoads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/index.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list',context)