"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from checkApp.models import CheckList, Task
from django.utils import simplejson


class CheckTestHelper(object):
    """
    Helper Object to Handle creating models in the db
    """
    def create_checklist(self, **kwargs):
        defaults = {
            'name': 'test',
            'creator': 'tester'
        }
        defaults.update(kwargs)
        return CheckList.objects.create(**defaults)

    def create_checkItem(self, **kwargs):
        if kwargs.get('pk'):
            pk = kwargs.get('pk')
        else:
            pk = 1
        defaults = {
            'text': 'test this',
            'done': False,
            'checkList': CheckList.objects.get(id=pk)
        }
        return Task.objects.create(**defaults)

    def setupCheckList(self):
        """
        Sets up some CheckList and Tasks for testing
        """
        CheckTestHelper.create_checklist(self)
        CheckTestHelper.create_checkItem(self, text='test1')
        CheckTestHelper.create_checkItem(self, text='test2')


class index_TestCase(CheckTestHelper, TestCase):
    """
    Tests the index view
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('index')

    def test_pageLoads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/index.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list', context)


class viewList_TestCase(CheckTestHelper, TestCase):
    """
    Tests the viewList
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('viewList', args=[1])

    def test_pageLoads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/viewList.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list', context)
        items = context['list'].tasks.all()
        self.assertEqual(items.count(), 2)


class taskDone_TestCase(CheckTestHelper, TestCase):
    """
    tests the Ajax view for marking Tasks as Done
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('taskDone')

    def test_post(self):
        data = {'pk': 1, 'val': 'true'}
        response = self.client.post(self.url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        item = simplejson.loads(response.content)[0]
        self.assertEqual(item['pk'], 1)
        self.assertEqual(item['model'], 'checkApp.task')
        self.assertEqual(item['fields']['done'], False)


class createTask_TestCase(CheckTestHelper, TestCase):
    """
    Tests the Ajax view for creating Tasks
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('createTask')

    def test_post(self):
        itemsTotalBefore = Task.objects.all().count()
        data = {'checkList': 1, 'text': 'test'}
        response = self.client.post(self.url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        itemsTotalAfter = Task.objects.all().count()
        self.assertEqual(itemsTotalBefore + 1, itemsTotalAfter)


class createCheckListTestCase(CheckTestHelper, TestCase):
    """
    Tests the Ajax view for Creating CheckLists
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('createCheckList')

    def test_post(self):
        data = {'name': 'testlist',
              'creator': 'tester'}
        response = self.client.post(self.url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        newList = simplejson.loads(response.content)[0]
        self.assertIn('name', newList['fields'])
        self.assertIn('creator', newList['fields'])
