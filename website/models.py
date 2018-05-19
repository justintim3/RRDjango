from django.db import models
from django import forms

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


class ComicCharacters(models.Model):
    ComicID = models.IntegerField(db_column='ComicID', primary_key=True)
    CharacterID = models.IntegerField(db_column='CharacterID', primary_key=True)


class ComicCreators(models.Model):
    ComicID = models.IntegerField(db_column='ComicID', primary_key=True)
    CreatorID = models.IntegerField(db_column='CreatorID', primary_key=True)
    CreatorTypeID = models.IntegerField(db_column='CreatorTypeID', primary_key=True)


class Creator(models.Model):
    CreatorID = models.IntegerField(db_column='CreatorID', primary_key=True)
    CreatorName = models.CharField(max_length=255)
    CreatorPicture = models.CharField(max_length=255)
    CreatorBiography = models.TextField()
    CreatorDOB = models.CharField(max_length=255)
    ComicID = models.IntegerField(db_column='ComicID')
    CreatorBirthPlace = models.CharField(max_length=255)


class CreatorTypes(models.Model):
    CreatorTypeID = models.IntegerField(db_column='CreatorTypeID', primary_key=True)
    CreatorTypeName = models.CharField(max_length=255)


class Publishers(models.Model):
    PublisherID = models.IntegerField(db_column='PublisherID', primary_key=True)
    PublisherName = models.CharField(max_length=255)
    PublisherInformation = models.TextField()
    PublisherPicture = models.CharField(max_length=255)
    ComicID = models.IntegerField(db_column='ComicID')
    SeriesID = models.IntegerField(db_column='SeriesID')
    CharacterID = models.IntegerField(db_column='CharacterID')
    #ComicVolumeID = models.IntegerField(db_column='ComicVolumeID')
    PublisherTotalSeries = models.IntegerField(db_column='PublisherTotalSeries')
    PublisherWebsite = models.CharField(max_length=255)


class Series(models.Model):
    SeriesID = models.IntegerField(db_column='SeriesID', primary_key=True)
    SeriesName = models.CharField(max_length=255)
    PublisherID = models.IntegerField(db_column='PublisherID')
    PublicationDate = models.CharField(max_length=255)
    SeriesCountry = models.CharField(max_length=255)
    SeriesLanguage = models.CharField(max_length=255)
    SeriesNotes = models.TextField()


class SeriesPublishers(models.Model):
    SeriesID = models.IntegerField(db_column='SeriesID', primary_key=True)
    PublisherID = models.IntegerField(db_column='PublisherID', primary_key=True)


class Character(models.Model):
    CharacterID = models.IntegerField(db_column='CharacterID', primary_key=True)
    CharacterName = models.CharField(max_length=255)
    CharacterRealName = models.CharField(max_length=255)
    CharacterPowers = models.CharField(max_length=255)
    CharacterBiography = models.CharField(max_length=255)
    CharacterWeaknesses = models.CharField(max_length=255)


class ComicStoryArcs(models.Model):
    ComicID = models.IntegerField(db_column='ComicID', primary_key=True)
    StoryArcID = models.IntegerField(db_column='CharacterID', primary_key=True)


class StoryArcs(models.Model):
    StoryArcID = models.IntegerField(db_column='StoryArcID', primary_key=True)
    StoryArcTitle = models.CharField(max_length=255)
    StoryArcNotes = models.TextField()


class NewsFeed(models.Model):
    ID = models.IntegerField(db_column = 'ID', primary_key = True)
    Title = models.CharField(max_length = 200)
    Date = models.DateField()
    Author = models.CharField(max_length=100)
    Preview = models.TextField()
    Text = models.TextField()

    def __str__ (self):
        return "Title " + self.Title


class Users(models.Model):
    UserID = models.IntegerField(db_column = 'UserID', primary_key= True)
    UserDisplayName = models.CharField(max_length = 200)
    UserFirstName = models.CharField(max_length=255)
    UserLastName = models.CharField(max_length=255)
    UserDOB = models.DateField()
    UserAddress = models.CharField(max_length=255)
    UserBiography = models.TextField()
    UserInterest = models.CharField(max_length=255)
    UserPicture = models.CharField(max_length=255)
    UserPassword = models.CharField(max_length=255)
    UserEmail = models.CharField(max_length=255)

    def __str__(self):
        return "ID: " + str(self.UserID) + "\tUserName: " + self.UserDisplayName


class Reviews(models.Model):
    ComicID = models.IntegerField()
    username = models.CharField(max_length = 255)
    ReviewText = models.TextField()
    ReviewDate = models.DateTimeField()

    def __str__(self):
        return str(self.user)

