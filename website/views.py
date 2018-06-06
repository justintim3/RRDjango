from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db import connection

# Create your views here.

def homepage(request):
    newsFeed = NewsFeed.objects.raw('SELECT * FROM website_newsfeed ORDER BY DATE DESC limit 10')
    comics = Comic.objects.raw('SELECT ComicID, ComicIssueTitle FROM website_comic '
                               'ORDER BY ComicRating DESC, ComicNumberOfRaters DESC LIMIT 10;')
    return render(request, 'homepage/homepage.html', {'newsFeeds': newsFeed , 'comics': comics })


def get_comicpage(request):
    comicId = request.GET.get('id')
    userId = request.user.id
    date = timezone.now()
    userName = request.user.username

    #Rating
    if 'rate' in request.POST:
        userRating = int(request.POST.get("rating", None))
        comic = Comic.objects.get(ComicID=comicId)
        try:
            prevRating = UserRatings.objects.get(UserID=userId, ComicID=comicId)
            cursor = connection.cursor()
            if userRating > 0:
                cursor.execute("UPDATE website_userratings SET UserRating = %s WHERE UserID = %s AND ComicID = %s;", (userRating, userId, comicId))
                comic.ComicTotalRating = comic.ComicTotalRating - prevRating.UserRating + userRating
                comic.ComicRating = comic.ComicTotalRating / comic.ComicNumberOfRaters
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Rating",
                                             TimelineItemTypeID=comic.ComicID, TimelineItemDatePosted=date)
            elif userRating == 0:
                cursor.execute("DELETE FROM website_userratings WHERE UserID = %s AND ComicID = %s;", (userId, comicId))
                comic.ComicNumberOfRaters = comic.ComicNumberOfRaters - 1
                comic.ComicTotalRating = comic.ComicTotalRating - prevRating.UserRating
                if comic.ComicNumberOfRaters == 0:
                    comic.ComicRating = 0
                else:
                    comic.ComicRating = comic.ComicTotalRating / comic.ComicNumberOfRaters
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Unrating",
                                             TimelineItemTypeID=comic.ComicID, TimelineItemDatePosted=date)
            comic.save(update_fields=["ComicRating", "ComicTotalRating", "ComicNumberOfRaters"])
            cursor.close()

        except:
            if userRating > 0:
                newRating = UserRatings.objects.create(UserID=userId, ComicID=comicId, UserRating=userRating)
                if comic.ComicNumberOfRaters:
                    comic.ComicNumberOfRaters = comic.ComicNumberOfRaters + 1
                else:
                    comic.ComicNumberOfRaters = 1
                if comic.ComicTotalRating:
                    comic.ComicTotalRating = comic.ComicTotalRating + userRating
                else:
                    comic.ComicTotalRating = userRating
                comic.ComicRating = comic.ComicTotalRating / comic.ComicNumberOfRaters
                comic.save(update_fields=["ComicRating", "ComicTotalRating", "ComicNumberOfRaters"])
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Rating",
                                             TimelineItemTypeID=comic.ComicID, TimelineItemDatePosted=date)


    #Reviews
    reviewList = Reviews.objects.raw('SELECT * FROM website_reviews '
                                     'WHERE ComicID = %s ORDER BY ReviewDate DESC', [comicId])
    userList = Users.objects.raw('SELECT * FROM auth_user')
    if "review" in request.POST:
        reviewText = request.POST.get("textfield", None)
        review = Reviews(ComicID=comicId, UserID=userId, username=userName, ReviewDate=date,
                         ReviewText=reviewText)
        review.save()
        #timelineItemTypeId = Reviews.objects.latest('id').id
        TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Review",
                                     TimelineItemTypeID=comicId, TimelineItemDatePosted=date)

    #Edit Reviews
    editReview = False
    for review in reviewList:
        if 'editreview' + str(review.id) in request.POST:  # Found review
            editReview = review.id
            break
        if 'savereview' + str(review.id) in request.POST:  # Found review
            reviewText = request.POST.get('reviewText', None)
            try:
                Reviews.objects.get(id=review.id)
                cursor = connection.cursor()
                cursor.execute("UPDATE website_reviews SET ReviewText = %s, EditDate = %s WHERE id = %s;",
                               (reviewText, date, review.id))
                cursor.close()
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="EditReview",
                                             TimelineItemTypeID=comicId, TimelineItemDatePosted=date)
            except:
                pass
            break
        if 'deletereview' + str(review.id) in request.POST:  # Found review
            try:
                cursor = connection.cursor()
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="DeleteReview",
                                             TimelineItemTypeID=comicId, TimelineItemDatePosted=date)
                cursor.execute("DELETE FROM website_reviews WHERE id = %s;)", [review.id])
                #cursor.close()
            except:
                pass
            break

    comicList = Comic.objects.raw('select * from website_comic where ComicID = %s', [comicId])
    characterList = Character.objects.raw('SELECT DISTINCT Characters.CharacterID, CharacterName FROM website_comic '
                                       'INNER JOIN ComicCharacters ON website_comic.ComicID = ComicCharacters.ComicID '
                                       'INNER JOIN Characters ON ComicCharacters.CharacterID = Characters.CharacterID '
                                       'WHERE website_comic.ComicID = %s', [comicId])
    series = Series.objects.raw('SELECT DISTINCT ComicID, Series.SeriesID, Series.SeriesName FROM website_comic '
                                    'INNER JOIN Series ON website_comic.SeriesID = Series.SeriesID '
                                    'WHERE ComicID = %s', [comicId])
    publisher = Publishers.objects.raw('SELECT DISTINCT website_comic.ComicID, Publishers.PublisherID, Publishers.PublisherName FROM website_comic '
                                      'INNER JOIN Publishers ON website_comic.PublisherID = Publishers.PublisherID '
                                      'WHERE website_comic.ComicID = %s', [comicId])
    storyArcList = StoryArcs.objects.raw('SELECT DISTINCT StoryArcs.StoryArcID, StoryArcTitle FROM website_comic '
                                         'INNER JOIN ComicStoryArcs ON website_comic.ComicID = ComicStoryArcs.ComicID '
                                         'INNER JOIN StoryArcs ON ComicStoryArcs.StoryArcID = StoryArcs.StoryArcID '
                                         'WHERE website_comic.ComicID = %s', [comicId])
    writerList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Writer";', [comicId])
    pencillerList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Penciller";', [comicId])
    inkerList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Inker";', [comicId])
    coloristList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Colorist";', [comicId])
    lettererList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Letterer";', [comicId])
    editorList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Editor";', [comicId])
    coverArtistList = Series.objects.raw('SELECT DISTINCT * FROM website_comic '
                                 'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE website_comic.ComicID = %s AND CreatorTypeName = "Cover Artist";', [comicId])


    try:
        userRating = UserRatings.objects.raw('SELECT * FROM website_userratings WHERE UserID = %s AND ComicID = %s',
                                             (userId, comicId))[0]
        return render(request, 'comicpage.html', {'comic': comicList[0], 'characterList': characterList,
                                                  'series': series[0], 'publisher': publisher[0],
                                                  'storyArcList': storyArcList, 'writerList': writerList,
                                                  'pencillerList': pencillerList, 'inkerList': inkerList,
                                                  'coloristList': coloristList, 'lettererList': lettererList,
                                                  'editorList': editorList, 'coverArtistList': coverArtistList,
                                                  'reviewList': reviewList, 'userList': userList,
                                                  'editReview': editReview, 'userRating': userRating})

    except:
        return render(request, 'comicpage.html', {'comic': comicList[0], 'characterList': characterList,
                                                  'series': series[0], 'publisher': publisher[0],
                                                  'storyArcList': storyArcList, 'writerList': writerList,
                                                  'pencillerList': pencillerList, 'inkerList': inkerList,
                                                  'coloristList': coloristList, 'lettererList': lettererList,
                                                  'editorList': editorList, 'coverArtistList': coverArtistList,
                                                  'reviewList': reviewList, 'userList': userList,
                                                  'editReview': editReview})


  
def get_characterpage(request):
    characterId = request.GET.get('id')
    characterList = Character.objects.raw('SELECT * FROM Characters WHERE CharacterID = %s', [characterId])
    comicList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle FROM website_comic '
                                   'INNER JOIN ComicCharacters ON website_comic.ComicID = ComicCharacters.ComicID '
                                   'INNER JOIN Characters ON ComicCharacters.CharacterID = Characters.CharacterID '
                                   'WHERE Characters.CharacterID = %s', [characterId])
    return render(request, 'characterpage.html', {'character': characterList[0], 'comicList': comicList})


def get_creatorpage(request):
    creatorId = request.GET.get('id')
    creator = Creator.objects.raw('SELECT * FROM Creators WHERE CreatorID = %s', [creatorId])
    writerList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Writer"', [creatorId])

    pencillerList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Penciller"', [creatorId])

    inkerList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Inker"', [creatorId])

    coloristList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Colorist"', [creatorId])

    lettererList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Letterer"', [creatorId])

    editorList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Editor"', [creatorId])

    coverArtistList = Comic.objects.raw('SELECT DISTINCT website_comic.ComicID, ComicIssueTitle, Creators.CreatorName FROM website_comic '
                                   'INNER JOIN ComicCreators ON website_comic.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Cover Artist"', [creatorId])
    return render(request, 'creatorpage.html', {'creator': creator[0], 'writerList': writerList,
                                                'pencillerList': pencillerList, 'inkerList': inkerList,
                                                'coloristList': coloristList, 'lettererList': lettererList,
                                                'editorList': editorList, 'coverArtistList': coverArtistList})


def get_newsfeedpage(request):
    newsFeedID = request.GET.get('id')
    newsFeed = NewsFeed.objects.raw('select * from website_newsfeed where ID = %s', [newsFeedID])
    return render(request, 'newsfeedpage.html', {'newsFeed': newsFeed[0]})


def get_comic(request):
    comics = Comic.objects.raw('SELECT Series.SeriesID, website_comic.ComicID, Series.SeriesName, ComicIssueTitle '
                               'FROM website_comic '
                               'INNER JOIN ComicSeries ON website_comic.ComicID = ComicSeries.ComicID '
                               'INNER JOIN Series ON ComicSeries.SeriesID = Series.SeriesID '
                               'ORDER BY SeriesName ASC, ComicIssueNumber ASC')
    return render(request, 'comic.html',{'comics': comics})


def get_character(request):
    characters = Character.objects.raw('SELECT CharacterID, CharacterName, CharacterPicture FROM Characters ORDER BY CharacterName ASC')
    return render(request, 'character.html', {'characters': characters})


def get_creator(request):
    creators = Creator.objects.raw('SELECT CreatorID,CreatorName,CreatorPicture FROM Creators ORDER BY CreatorName ASC')
    return render(request, 'creator.html', {'creators': creators})


def get_newsfeed(request):
    newsFeed = NewsFeed.objects.raw('SELECT * FROM website_newsfeed ORDER BY DATE DESC')
    return render(request, 'newsfeed.html', {'newsFeed': newsFeed})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def get_profile(request):
    profileId = request.GET.get('id')
    userId = request.user.id
    userName = request.user.username
    date = timezone.now()

    #Save profile
    if "saveProfile" in request.POST:
        fname = request.POST.get("firstname", None)
        lname = request.POST.get("lastname", None)
        useremail = request.POST.get("email", None)
        address = request.POST.get("address", None)
        birthdate = request.POST.get("dob", None)
        interests = request.POST.get("interests", None)
        biography = request.POST.get("biography", None)
        favcomic = request.POST.get("favcomic", None)
        favchar = request.POST.get("favchar", None)
        cursor = connection.cursor()
        cursor.execute("UPDATE auth_user SET first_name = %s, last_name = %s, email = %s, address = %s, interests = %s, "
                       "biography = %s, DOB = %s, favorite_comic = %s, favorite_character = %s WHERE id = %s;",
                       (fname, lname, useremail, address, interests, biography, birthdate, favcomic, favchar, userId))
        cursor.close()

    #User following
    following = False
    if userId:
        cursor = connection.cursor()
        try:
            following = UserFollowings.objects.get(UserID=userId, FollowedUserID=profileId)
            if 'follow' in request.POST:
                cursor.execute("UPDATE website_userfollowings SET FollowStatus = TRUE WHERE UserID=%s AND FollowedUserID=%s;",
                               (userId, profileId))
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Follow",
                                             TimelineItemTypeID=profileId, TimelineItemDatePosted=date)

                following = UserFollowings.objects.get(UserID=userId, FollowedUserID=profileId)
            if 'unfollow' in request.POST:
                cursor.execute("UPDATE website_userfollowings SET FollowStatus = FALSE WHERE UserID=%s AND FollowedUserID=%s;",
                               (userId, profileId))
                TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Unfollow",
                                             TimelineItemTypeID=profileId, TimelineItemDatePosted=date)
                following = UserFollowings.objects.get(UserID=userId, FollowedUserID=profileId)
        except:
            if userId == int(profileId):
                pass
            else:
                profileName = Users.objects.raw('SELECT * FROM auth_user WHERE id = %s', [profileId])[0].username
                if 'follow' in request.POST:
                    cursor.execute(
                        "INSERT INTO website_userfollowings (UserID, UserName, FollowedUserID, FollowedUserName, FollowStatus)"
                        " VALUES (%s, %s, %s, %s, %s);", (userId, userName, profileId, profileName, True))
                    TimelineItems.objects.create(UserID=userId, UserName=userName, TimelineItemTypeName="Follow",
                                                 TimelineItemTypeID=profileId, TimelineItemDatePosted=date)
                else:
                    cursor.execute(
                        "INSERT INTO website_userfollowings (UserID, UserName, FollowedUserID, FollowedUserName, FollowStatus)"
                        " VALUES (%s, %s, %s, %s, %s);", (userId, userName, profileId, profileName, False))

                following = UserFollowings.objects.get(UserID=userId, FollowedUserID=profileId)
        cursor.close()

    profile = Users.objects.raw('SELECT * FROM auth_user WHERE id = %s', [profileId])
    timelineItemList = TimelineItems.objects.raw('SELECT * FROM website_timelineitems WHERE UserID = %s ORDER BY TimelineItemDatePosted DESC', [profileId])
    ratingList = UserRatings.objects.raw('SELECT * FROM website_userratings WHERE UserID = %s', [profileId])
    reviewList = Reviews.objects.raw('SELECT * FROM website_reviews WHERE UserID = %s', [profileId])
    comicList = Comic.objects.raw('SELECT ComicID, ComicIssueTitle FROM website_comic')
    userList = Users.objects.raw('SELECT id, username FROM auth_user')
    userFollowingList = UserFollowings.objects.raw('SELECT * FROM website_userfollowings ORDER BY FollowedUserName ASC')
    timelineItemLikeDislikeList = TimelineItemLikeDislikes.objects.raw('SELECT * FROM website_timelineitemlikedislikes WHERE UserID = %s', [userId])

    #Likes/Dislikes
    cursor = connection.cursor()
    for timelineItem in timelineItemList:
        if userId:
            try:
                TimelineItemLikeDislikes.objects.get(TimelineItemID=timelineItem.TimelineItemID, UserID=userId)
            except:
                cursor.execute(
                    "INSERT INTO website_timelineitemlikedislikes (TimelineItemID, UserID, LikeDislikeStatus)"
                    " VALUES (%s, %s, %s);", (timelineItem.TimelineItemID, userId, 0))

        if 'thumbup'+str(timelineItem.TimelineItemID) in request.POST:  #Found timelineItem
            timelineItemLikeDislike = TimelineItemLikeDislikes.objects.raw(
                'SELECT * FROM website_timelineitemlikedislikes WHERE TimelineItemID = %s AND UserID = %s', (timelineItem.TimelineItemID, userId))[0]
            if timelineItemLikeDislike.LikeDislikeStatus == 1:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsUp = TimelineThumbsUp - 1 "
                               "WHERE TimelineItemID = %s", [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = 0 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
            elif timelineItemLikeDislike.LikeDislikeStatus == -1:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsUp = TimelineThumbsUp + 1, "
                               "TimelineThumbsDown = TimelineThumbsDown - 1 WHERE TimelineItemID = %s",
                               [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = 1 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
            elif timelineItemLikeDislike.LikeDislikeStatus == 0:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsUp = TimelineThumbsUp + 1 "
                               "WHERE TimelineItemID = %s", [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = 1 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
        if 'thumbdown'+str(timelineItem.TimelineItemID) in request.POST:
            timelineItemLikeDislike = TimelineItemLikeDislikes.objects.raw(
                'SELECT * FROM website_timelineitemlikedislikes WHERE TimelineItemID = %s AND UserID = %s', (timelineItem.TimelineItemID, userId))[0]
            if timelineItemLikeDislike.LikeDislikeStatus == 1:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsUp = TimelineThumbsUp - 1, "
                               "TimelineThumbsDown = TimelineThumbsDown + 1 WHERE TimelineItemID = %s",
                               [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = -1 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
            elif timelineItemLikeDislike.LikeDislikeStatus == -1:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsDown = TimelineThumbsDown - 1 "
                               "WHERE TimelineItemID = %s", [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = 0 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
            elif timelineItemLikeDislike.LikeDislikeStatus == 0:
                cursor.execute("UPDATE website_timelineitems SET TimelineThumbsDown = TimelineThumbsDown + 1 "
                               "WHERE TimelineItemID = %s", [timelineItem.TimelineItemID])
                cursor.execute("UPDATE website_timelineitemlikedislikes SET LikeDislikeStatus = -1 "
                               "WHERE TimelineItemID = %s AND UserID = %s", (timelineItem.TimelineItemID, userId))
                break
    cursor.close()

    return render(request, 'profile.html', {'following': following, 'profile': profile[0],
                                            'timelineItemList': timelineItemList, 'ratingList': ratingList,
                                            'reviewList': reviewList, 'comicList': comicList, 'userList': userList,
                                            'userFollowingList': userFollowingList, 'timelineItemLikeDislikeList': timelineItemLikeDislikeList})


def get_editprofile(request):
    userId = request.user.id
    profile = Users.objects.raw('SELECT * FROM auth_user WHERE id = %s', [userId])

    return render(request, 'editprofile.html', {'profile': profile[0]})


def get_signuppage(request):
    return render(request, 'signup.html')


def get_about(request):
    return render(request, 'about.html')


def get_contact(request):
    return render(request, 'contact.html')


def get_publisherpage(request):
    publisherId = request.GET.get('id')
    publisherList = Publishers.objects.raw('SELECT * FROM Publishers WHERE PublisherID = %s', [publisherId])
    seriesList = Series.objects.raw('SELECT Series.SeriesID, Series.SeriesName FROM Publishers '
                                    'INNER JOIN SeriesPublishers ON Publishers.PublisherID = SeriesPublishers.PublisherID '
                                    'INNER JOIN Series ON SeriesPublishers.SeriesID = Series.SeriesID '
                                    'WHERE Publishers.PublisherID = %s ORDER BY Series.SeriesName ASC', [publisherId])
    comicList = Comic.objects.raw('SELECT Publishers.PublisherID, website_comic.ComicID, website_comic.ComicIssueTitle ' 
                                  'FROM website_comic INNER JOIN ComicPublishers ON website_comic.ComicID = ComicPublishers.ComicID '
                                  'INNER JOIN Publishers ON ComicPublishers.PublisherID = Publishers.PublisherID '
                                  'WHERE Publishers.PublisherID = %s ORDER BY website_comic.ComicIssueTitle ASC', [publisherId])
    return render(request, 'publisherpage.html', {'publisher': publisherList[0], 'seriesList': seriesList, 'comics': comicList})


def get_seriespage(request):
    seriesId = request.GET.get('id')
    seriesList = Series.objects.raw('SELECT * FROM Series WHERE SeriesID = %s', [seriesId])
    comicList = Comic.objects.raw('SELECT Series.SeriesID, website_comic.ComicID, website_comic.ComicIssueTitle '
                                  'FROM website_comic INNER JOIN ComicSeries ON website_comic.ComicID = ComicSeries.ComicID '
                                  'INNER JOIN Series ON ComicSeries.SeriesID = Series.SeriesID '
                                  'WHERE Series.SeriesID = %s ORDER BY website_comic.ComicIssueTitle ASC', [seriesId])
    publisherList = Publishers.objects.raw('SELECT Publishers.PublisherID, PublisherName FROM Publishers '
                                           'INNER JOIN SeriesPublishers ON Publishers.PublisherID = SeriesPublishers.PublisherID '
                                           'INNER JOIN Series ON SeriesPublishers.SeriesID = Series.SeriesID '
                                           'WHERE Series.SeriesID = %s ORDER BY Publishers.PublisherName ASC', [seriesId])
    return render(request, 'seriespage.html', {'series': seriesList[0], 'comics': comicList,
                                               'publisher': publisherList[0]})


def search(request):
    if 'search' in request.GET:
        searchString = request.GET.get('search', None)
        comicList = Comic.objects.raw('SELECT * FROM website_comic WHERE ComicIssueTitle LIKE %s', ["%" + searchString + "%"])
        characterList = Character.objects.raw('SELECT * FROM Characters WHERE CharacterName LIKE %s', ["%" + searchString + "%"])
        creatorList = Creator.objects.raw('SELECT * FROM Creators WHERE CreatorName LIKE %s', ["%" + searchString + "%"])
        seriesList = Series.objects.raw('SELECT * FROM Series WHERE SeriesName LIKE %s', ["%" + searchString + "%"])
        publisherList = Publishers.objects.raw('SELECT * FROM Publishers WHERE PublisherName LIKE %s', ["%" + searchString + "%"])
        newsList = NewsFeed.objects.raw('SELECT * FROM website_newsfeed WHERE Title LIKE %s', ["%" + searchString + "%"])
    return render(request, 'search.html', {'seriesList': seriesList, 'comicList': comicList, 'characterList': characterList,
                                           'creatorList': creatorList, 'publisherList': publisherList, 'newsList': newsList,
                                           'searchString': searchString})
