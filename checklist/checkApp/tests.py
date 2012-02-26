"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.contrib.auth.models import User

from checkApp.models import CheckList, Task, Template

def login(self, username="tester", password="test"):
    url = reverse('login')
    data = { 'username': username,
             'password': password, }
    return self.client.post(url,data=data,follow=True)

def logout(self):
    url = reverse('logout')
    return self.client.post(url,follow=True)

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

    def setupUser(self):
        return User.objects.create_user(username="tester",email="test@test.com",password="test")

class userAuth_TestCase(CheckTestHelper, TestCase):
    def setUp(self):
        CheckTestHelper.setupUser(self)

    def test_login(self):
        response = login(self)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/index.html')
        self.assertEqual(response.context['user'].username, 'tester')

    def test_logout(self):
        response = login(self)
        response = logout(self)
        self.assertEqual(response.status_code, 200)


class index_TestCase(CheckTestHelper, TestCase):
    """
    Tests the index view
    """
    def setUp(self):
        CheckTestHelper.setupUser(self)
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
        login(self)
        context = self.client.get(self.url).context
        self.assertIn('form', context)
        form = context['form']
        self.assertEqual(form.initial['creator'], 'tester')


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
        resp = simplejson.loads(response.content)
        self.assertEqual(resp['pk'], data['pk'])
        self.assertLess(checkLists_After, checkLists_Before)
        self.assertLess(tasks_After, tasks_Before)


class CheckListTemplate_TestCase(CheckTestHelper, TestCase):
    """
    Tests for the Template Model & ViewTemplates View
    """
    def setUp(self):
        CheckTestHelper.setupCheckList(self)
        self.url = reverse('viewTemplates')

    def test_createFromCheckList(self):
        clist = CheckList.objects.get(pk=1)
        temp = Template().createFromCheckList(clist)
        self.assertEqual(temp.name, clist.name)
        self.assertEqual(temp.creator, clist.creator)
        self.assertEqual(temp.pickledTasks.count(), 2)

    def test_ViewTemplates(self):
        clist = CheckList.objects.get(pk=1)
        new_template = Template().createFromCheckList(clist)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkApp/viewTemplates.html')

    def test_createFromTemplate(self):
        clist = CheckList.objects.get(pk=1)
        new_template = Template().createFromCheckList(clist)
        new_checklist = CheckList().createFromTemplate(new_template, 'tester')

    def test_startCheckListFromTemplate(self):
        clist = CheckList.objects.get(pk=1)
        taskcount_Before = Task.objects.all().count()
        temp = Template().createFromCheckList(clist)
        url = reverse('startCheckList')
        response = self.client.post(url, data={'pk': temp.pk})
        self.assertEqual(response.status_code, 302)

        taskcount_After = Task.objects.all().count()
        self.assertGreater(taskcount_After, taskcount_Before)
