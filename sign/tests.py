from django.test import TestCase
from sign.models import Event
from sign.models import Guest
# Create your tests here.


class ModuleTest(TestCase):

    def setUp(self) -> None:
        Event.objects.create(id=1, name='oneplus 3 event',
                            status=True, limit=200,
                            address='shenzhen',
                            start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1,
                             realname='alen',
                             phone='13711001101',
                             email='alen@mail.com',
                             sign=False)

    def test_event_modles(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_modles(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, 'alen')
        self.assertFalse(result.sign)