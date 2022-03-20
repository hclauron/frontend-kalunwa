
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from .utils import get_test_image_file
from kalunwa.content.models import CampEnum, Image, Jumbotron, News, Project, Tag, Event
from kalunwa.content.serializers import EventSerializer, HomepageJumbotronSerializer, HomepageEventSerializer, HomepageNewsSerializer, HomepageProjectSerializer, ProjectSerializer
from kalunwa.content.serializers import StatusEnum


class ImageURLSerializerTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.image = Image.objects.create(
            title='eating_me',
            image=get_test_image_file(),
        )

        cls.jumbotron = Jumbotron.objects.create(
            id=1, 
            header_title= 'J1', 
            short_description= 'short description 1',
            image = cls.image
        )

        test_date = '2022-03-19 14:35:46.271745+00:00'

        cls.event = Event.objects.create(
            title= 'Event 1', 
            description= 'description 1',
            start_date=test_date,
            end_date=test_date,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=1),
            is_featured=True,
            ) 

        cls.project = Project.objects.create(
            title= 'Project 1', 
            description= 'description 1',
            start_date=test_date,
            end_date=test_date,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=1),
            is_featured=False,
            )   

        cls.news = News.objects.create(
                title = 'News 1',
                description= 'description 1',
                image = Image.objects.get(pk=1),
            )

        cls.request_factory = RequestFactory()


    def test_get_object_image_pk(self):
        """
        test for:
        image = Image.objects.get(pk=obj.image.pk)
        """
        image = Image.objects.get(pk=self.jumbotron.image.id)
        self.assertEqual(self.image, image)
        

    def test_jumbotron_image_full_url(self):
        #print(self.client.)
        request = self.request_factory.get(reverse("homepage-jumbotrons"))
        serializer = HomepageJumbotronSerializer(self.jumbotron, context={'request':request})
        ## build complete url 
            # request.scheme -> http
            # request.get_host() -> testserver        
            # self.image.image.name ->  images/content/test_U5U97df.jpg
        url = f'{request.scheme}://{request.get_host()}/media/{self.image.image.name}'
        self.assertEqual(url, serializer.data['image'])

    def test_event_image_full_url(self):
        request = self.request_factory.get(reverse("homepage-events"))
        serializer = HomepageEventSerializer(self.event, context={'request':request})
        url = f'{request.scheme}://{request.get_host()}/media/{self.image.image.name}'
        self.assertEqual(url, serializer.data['image'])

    def test_project_image_full_url(self):
        request = self.request_factory.get(reverse("homepage-projects"))
        serializer = HomepageProjectSerializer(self.project, context={'request':request})
        url = f'{request.scheme}://{request.get_host()}/media/{self.image.image.name}'
        self.assertEqual(url, serializer.data['image'])

    def test_news_image_full_url(self):
        request = self.request_factory.get(reverse("homepage-news"))
        serializer = HomepageNewsSerializer(self.news, context={'request':request})
        url = f'{request.scheme}://{request.get_host()}/media/{self.image.image.name}'
        self.assertEqual(url, serializer.data['image'])
        

class StatusSerializerTestCase(TestCase):
    """
    test dates are prepared to simulate a timezone.now() request, and
    get the expected status
    """
    @classmethod
    def setUpTestData(cls) -> None: 
        date_tomorrow = timezone.now() + timezone.timedelta(days=1)
        date_yesterday = timezone.now() - timezone.timedelta(days=1)

        image_file = get_test_image_file()
 
        for _ in range(4): 
            Image.objects.create(
                pk=_,
                title=f'image_{_}',
                image=image_file,
            )

        image = Image.objects.create(
                title='image_1',
                image=get_test_image_file(),            

        )
        # events
            #  upcoming
        cls.event_upcoming = Event.objects.create(
            title= 'upcoming event', 
            description= 'description 1',
            start_date=date_tomorrow,
            end_date=date_tomorrow,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=1),
            is_featured=True,
        ) 
            #  ongoing            
        cls.event_ongoing = Event.objects.create(
            title= 'ongoing event', 
            description= 'description 1',
            start_date=timezone.now(),
            end_date=date_tomorrow,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=2),
            is_featured=True,
        ) 

            #  past            
        cls.event_past = Event.objects.create(
            title= 'past event', 
            description= 'description 1',
            start_date=date_yesterday,
            end_date=date_yesterday,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=3),
            is_featured=True,
        ) 

        #projects 
            # upcoming
        cls.project_upcoming = Project.objects.create(
            title= 'upcoming project', 
            description= 'description 1',
            start_date=date_tomorrow,
            end_date=date_tomorrow,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=1),
            is_featured=True,
        ) 
            #  ongoing            
        cls.project_ongoing = Project.objects.create(
            title= 'ongoing project', 
            description= 'description 1',
            start_date=timezone.now(),
            end_date=date_tomorrow,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=2),
            is_featured=True,
        ) 
            #no_end date, ongoing
        cls.project_ongoing_no_end_date = Project.objects.create(
            title= 'ongoing project no end date', 
            description= 'description 1',
            start_date=timezone.now(),
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=3),
            is_featured=True,
        ) 

            #  past            
        cls.project_past = Project.objects.create(
            title= 'past project', 
            description= 'description 1',
            start_date=date_yesterday,
            end_date=date_yesterday,
            camp=CampEnum.GENERAL,
            image = Image.objects.get(pk=4),
            is_featured=True,
        ) 

    def test_past_status_event(self):
        serializer = EventSerializer(self.event_past)
        self.assertEqual(serializer.data['status'], StatusEnum.PAST.value)

    def test_ongoing_status_event(self):
        serializer = EventSerializer(self.event_ongoing)
        self.assertEqual(serializer.data['status'], StatusEnum.ONGOING.value)

    def test_upcoming_status_event(self):
        serializer = EventSerializer(self.event_upcoming)
        self.assertEqual(serializer.data['status'], StatusEnum.UPCOMING.value)

    def test_past_status_project(self):
        serializer = ProjectSerializer(self.project_past)
        self.assertEqual(serializer.data['status'], StatusEnum.PAST.value)

    def test_ongoing_status_project(self):
        serializer = ProjectSerializer(self.project_ongoing)
        self.assertEqual(serializer.data['status'], StatusEnum.ONGOING.value)

    def test_ongoing_no_date_status_project(self):
        serializer = ProjectSerializer(self.project_ongoing_no_end_date)
        self.assertEqual(serializer.data['status'], StatusEnum.ONGOING.value)


    def test_upcoming_status_project(self):
        serializer = ProjectSerializer(self.project_upcoming)
        self.assertEqual(serializer.data['status'], StatusEnum.UPCOMING.value)

