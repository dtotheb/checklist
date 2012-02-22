"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from checkApp.models import CheckList, Task, Template
from django.utils import simplejson


class CheckTestHelper(object):
    """
    Helper Object to Handle creating models in the db
    """
    def create_checklist(self, **kwargs):
        """
        Creates a CheckList model in the DB
        """
        defaults = {
            'name': 'test',
            'creator': 'tester'
        }
        defaults.update(kwargs)
        return CheckList.objects.create(**defaults)

    def create_task(self, **kwargs):
        """
        Creates a Task Model in the DB
        """
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
        Sets up a CheckList and some Tasks for testing
        """
        CheckTestHelper.create_checklist(self)
        CheckTestHelper.create_task(self, text='test1')
        CheckTestHelper.create_task(self, text='test2')


class index_TestCase(CheckTestHelper, TestCase):
    """
    Tests the index view
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('index')

    def test_pageLoads(self):
        """
        Tests that the page loads, and uses the expected template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/index.html')

    def test_pageContext(self):
        context = self.client.get(self.url).context
        self.assertIn('list', context)
        self.assertIn('title', context)

    def test_FormContents(self):
        """
        Makes sure that the Form exists and has all the required initial data
        """
        context = self.client.get(self.url).context
        self.assertIn('form', context)
        form = context['form']
        self.assertEqual(form.initial['creator'], 'anon')


class viewList_TestCase(CheckTestHelper, TestCase):
    """
    Tests the viewList
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('viewList', args=[1])

    def test_pageLoads(self):
        """
        Tests that the page loads, and uses the expected template.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/viewList.html')

    def test_pageContext(self):
        """
        Tests the contents of the Context Object
        """
        context = self.client.get(self.url).context
        self.assertIn('list', context)
        items = context['list'].tasks.all()
        self.assertEqual(items.count(), 2)
        self.assertIn('title', context)

    def test_FormContents(self):
        """
        Makes sure that the Form exists and has all the required initial data
        """
        context = self.client.get(self.url).context
        self.assertIn('form', context)
        form = context['form']
        self.assertEqual(form.initial['checkList'].pk, 1)


class taskDone_TestCase(CheckTestHelper, TestCase):
    """
    tests the Ajax view for marking Tasks as Done
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('taskDone')

    def test_post(self):
        """
        Sends a post request to the view
        Checks that task.done is updated
        """
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
        """
        Sends a post request to the View
        Checks that a task is created in the DB
        """
        itemsTotalBefore = Task.objects.all().count()
        data = {'checkList': 1, 'text': 'test'}
        response = self.client.post(self.url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        itemsTotalAfter = Task.objects.all().count()
        self.assertEqual(itemsTotalBefore + 1, itemsTotalAfter)


class createCheckList_TestCase(CheckTestHelper, TestCase):
    """
    Tests the Ajax view for Creating CheckLists
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('createCheckList')

    def test_post(self):
        """
        Sends a post request to the View
        Checks that a CheckList is created in the DB
        """
        data = {'name': 'testlist',
              'creator': 'tester'}
        response = self.client.post(self.url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        newList = simplejson.loads(response.content)[0]
        self.assertIn('name', newList['fields'])
        self.assertIn('creator', newList['fields'])


class deleteCheckList_TestCase(CheckTestHelper, TestCase):
    """
    Tests the Ajax view for Deleting CheckLists
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('deleteCheckList')

    def test_post(self):
        """
        Sends a post request to the deletecheckList view
        Tests that there's less CheckLists/Tasks after the Request
        """
        checkLists_Before = CheckList.objects.all().count()
        tasks_Before = Task.objects.all().count()
        data = {'pk': 1}
        response = self.client.post(self.url,
                   data=data,
                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        checkLists_After = CheckList.objects.all().count()
        tasks_After = Task.objects.all().count()

        self.assertEqual(response.status_code, 200)
        self.assertLess(checkLists_After, checkLists_Before)
        self.assertLess(tasks_After, tasks_Before)



class CheckListTemplate_TestCase(CheckTestHelper, TestCase):
    """
    Tests for the Template Model, which is a sublcass of CheckLit
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)

    def test_createFromCheckList(self):
        clist = CheckList.objects.get(pk=1)
        new_template = Template()
        new_template.createFromCheckList(clist)
        temp = Template.objects.all()[0]
        self.assertEqual(temp.name, clist.name)
        self.assertEqual(temp.creator, clist.creator)
        self.assertEqual(temp.pickledTasks.count(), 2)