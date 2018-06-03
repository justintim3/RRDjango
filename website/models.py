from django.db import models

# Create your models here.


class Comic (models.Model):
    ComicID = models.IntegerField(db_column='ComicID', primary_key=True)
    SeriesID = models.IntegerField()
    SeriesName = models.CharField(max_length=500)
    ComicIssueTitle = models.CharField(max_length=500)
    ComicIssueNumber = models.IntegerField()
    PublisherID = models.IntegerField()
    PublisherName = models.CharField(max_length = 500)
    ComicImage = models.CharField(max_length = 500)
    ComicCoverDate = models.DateField()
    ComicPrice = models.DecimalField(max_digits = 15 , decimal_places = 2)
    TimelineItemID = models.IntegerField()
    ComicFormat = models.CharField(max_length = 500)
    ComicSynopsis = models.TextField()
    ComicRating = models.DecimalField(max_digits=15 , decimal_places=2)
    ComicTotalRating = models.IntegerField(db_column='ComicTotalRating')
    ComicNumberOfRaters = models.IntegerField(db_column = 'ComicNumberOfRaters')
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
    id = models.IntegerField(db_column='id', primary_key=True)
    last_login = models.DateField()
    is_superuser = models.BinaryField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    is_staff = models.BinaryField()
    date_joined = models.CharField(max_length=255)
    DOB = models.DateField()
    biography = models.TextField()
    user_picture = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    interests = models.CharField(max_length=255)
    favorite_comic = models.CharField(max_length=255)
    favorite_character = models.CharField(max_length=255)

    def __str__(self):
        return "ID: " + str(self.UserID) + "\tUserName: " + self.UserDisplayName


class Reviews(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    ComicID = models.IntegerField()
    UserID = models.IntegerField()
    username = models.CharField(max_length = 255)
    ReviewText = models.TextField()
    ReviewDate = models.DateTimeField()
    EditDate = models.DateTimeField()

    def __str__(self):
        return str(self.user)

      
class UserRatings(models.Model):
    UserRatingID = models.AutoField(db_column='UserRatingID', primary_key=True)
    UserID = models.IntegerField(db_column='UserID')
    ComicID = models.IntegerField(db_column='ComicID')
    UserRating = models.IntegerField()


class UserFollowings(models.Model):
    UserFollowingID = models.AutoField(db_column='UserFollowingID', primary_key=True)
    UserID = models.IntegerField(db_column='UserID')
    UserName = models.CharField(max_length=255)
    FollowedUserID = models.IntegerField(db_column='FollowedUserID')
    FollowedUserName = models.CharField(max_length=255)
    FollowStatus = models.BooleanField()


class TimelineItems(models.Model):
    TimelineItemID = models.AutoField(db_column='TimelineItemID', primary_key=True)
    UserID = models.IntegerField()
    UserName = models.CharField(max_length=255)
    TimelineItemTypeName = models.CharField(max_length = 255)
    TimelineItemTypeID = models.IntegerField()
    TimelineItemDatePosted = models.DateTimeField()

class TimelineItemLikeDislikes(models.Model):
    TimelineItemID = models.IntegerField(db_column='TimelineItemID', primary_key=True)
    UserID = models.IntegerField()
    LikeDislikeStatus = models.IntegerField()