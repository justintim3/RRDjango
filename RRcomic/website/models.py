from django.db import models

# Create your models here.

class Comic (models.Model):
    ComicID = models.IntegerField(db_column='ComicID', primary_key=True)
    PublisherID = models.IntegerField()
    SeriesID = models.IntegerField()
    ComicIssueTitle = models.CharField(max_length = 500)
    CommicIssueNumber = models.IntegerField()
    ComicImage = models.CharField(max_length = 500)
    ComicCoverDate = models.DateField()
    ComicPrice = models.DecimalField(max_digits = 15 , decimal_places = 2)
    StoryArcId = models.IntegerField()
    CharacterID = models.IntegerField()
    ReviewID = models.IntegerField()
    TimelineItemID = models.IntegerField()
    ComicVolumeID = models.IntegerField()
    ComicFormat = models.CharField(max_length = 500)
    ComicSynopisis = models.TextField()
    ComicRating = models.IntegerField(db_column = 'ComicRating')
    ComicViewRanking = models.IntegerField()


    def __str__(self):
        return "ID: " + str(self.ComicID) + "\tTitle: " + self.ComicIssueTitle 

class NewsFeed(models.Model):
    ID = models.IntegerField(db_column = 'ID', primary_key = True)
    Title = models.CharField(max_length = 200)
    Text = models.TextField()
    Date = models.DateField()

    def __str__ (self):
        return "Title " + self.Title

class Users(models.Model):
    UserID = models.IntegerField(db_column = 'UserID', primary_key= True)
    UserDisplayName = models.CharField(max_length = 200)

    def __str__(self):
        return "ID: " + str(self.UserID) + "\tUserName: " + self.UserDisplayName
