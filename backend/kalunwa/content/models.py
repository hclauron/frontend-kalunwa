from django.db import models

# Create your models here.
from django.db import models
from django.forms import DateField
from kalunwa.core.models import TimestampedModel


class ContentModel(TimestampedModel):
    is_published = (models.BooleanField)
    # created_by (User)
    # last_updated_by (User)

    class Meta:
        abstract=True

class Tag(ContentModel):
    name = models.CharField(db_index=True, unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name

class Image(ContentModel):
    title = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='images/')
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True) # warning for image tag, 0 to many tags

    def __str__(self) -> str:
        return self.title

class Jumbotron(ContentModel):
    featured_image = models.OneToOneField(Image, on_delete=models.PROTECT)
    header_title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=225)

    def __str__(self) -> str:
        return f'{self.header_title} jumbotron'

class Homepage(ContentModel):
    # fk - jumbotron
    # fk - featured event
    # fk - featured project
    pass

class Event(ContentModel):
    # title
    # description
    # start_date
    # end_date
    # camp
    # featured_image
    #status
    pass

class Project(ContentModel):
    title = models.CharField(max_length=50)  
    description = models.CharField(max_length=225)
    start_date = DateField(auto_now=False, auto_now_add=False)    #notinERD
    end_date = DateField(auto_now=False, auto_now_add=False)
    # camp
    featured_image = models.OneToOneField(Image, on_delete=models.PROTECT)
    #status    
    pass

class News(ContentModel):
    title = models.CharField(max_length=50)  
    description = models.CharField(max_length=225)
    featured_image = models.OneToOneField(Image, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title


class Announcement(ContentModel):
    title = models.CharField(max_length=50, default=' ')  #try without default
    description = models.CharField(max_length=225, default=' ')
    
    def __str__(self) -> str:
        return self.title
