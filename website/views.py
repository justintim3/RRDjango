from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def homepage(request):
    newsFeed = NewsFeed.objects.raw('SELECT * FROM website_newsfeed ORDER BY DATE DESC limit 10')
    comics = Comic.objects.raw('select ComicID,ComicIssueTitle from Comics limit 10' )
    return render(request, 'homepage/homepage.html', {'newsFeeds': newsFeed , 'comics': comics })


def get_comicpage(request):
    comicId = request.GET.get('id')
  
    comicList = Comic.objects.raw('select ComicID,ComicIssueTitle,ComicIssueNumber,ComicImage,ComicCoverDate,ComicPrice,ComicFormat,ComicSynopisis,(ComicRatingSum/ComicNumberOfRaters) as ComicRating, ComicViewRanking from Comics where ComicID = %s', [comicId])
    characterList = Character.objects.raw('SELECT DISTINCT Characters.CharacterID, CharacterName FROM Comics '
                                       'INNER JOIN ComicCharacters ON Comics.ComicID = ComicCharacters.ComicID '
                                       'INNER JOIN Characters ON ComicCharacters.CharacterID = Characters.CharacterID '
                                       'WHERE Comics.ComicID = %s', [comicId])
    series = Series.objects.raw('SELECT DISTINCT ComicID, Series.SeriesID, SeriesName FROM Comics '
                                    'INNER JOIN Series ON Comics.SeriesID = Series.SeriesID '
                                    'WHERE ComicID = %s', [comicId])
    publisher = Publishers.objects.raw('SELECT DISTINCT Comics.ComicID, Publishers.PublisherID, PublisherName FROM Comics '
                                      'INNER JOIN Publishers ON Comics.PublisherID = Publishers.PublisherID '
                                      'WHERE Comics.ComicID = %s', [comicId])
    storyArcList = StoryArcs.objects.raw('SELECT DISTINCT StoryArcs.StoryArcID, StoryArcTitle FROM Comics '
                                         'INNER JOIN ComicStoryArcs ON Comics.ComicID = ComicStoryArcs.ComicID '
                                         'INNER JOIN StoryArcs ON ComicStoryArcs.StoryArcID = StoryArcs.StoryArcID '
                                         'WHERE Comics.ComicID = %s', [comicId])
    writerList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Writer";', [comicId])
    pencillerList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Penciller";', [comicId])
    inkerList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Inker";', [comicId])
    coloristList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Colorist";', [comicId])
    lettererList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Letterer";', [comicId])
    editorList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Editor";', [comicId])
    coverArtistList = Series.objects.raw('SELECT DISTINCT * FROM Comics '
                                 'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                 'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                 'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                 'WHERE Comics.ComicID = %s AND CreatorTypeName = "Cover Artist";', [comicId])

    return render(request, 'comicpage.html', {'comic': comicList[0], 'characterList': characterList,
                                              'series': series[0], 'publisher': publisher[0],
                                              'storyArcList': storyArcList, 'writerList': writerList,
                                              'pencillerList': pencillerList, 'inkerList': inkerList,
                                              'coloristList': coloristList, 'lettererList': lettererList,
                                              'editorList': editorList, 'coverArtistList': coverArtistList})


def get_characterpage(request):
    characterId = request.GET.get('id')
    characterList = Character.objects.raw('SELECT * FROM Characters WHERE CharacterID = %s', [characterId])
    comicList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle FROM Comics '
                                   'INNER JOIN ComicCharacters ON Comics.ComicID = ComicCharacters.ComicID '
                                   'INNER JOIN Characters ON ComicCharacters.CharacterID = Characters.CharacterID '
                                   'WHERE Characters.CharacterID = %s', [characterId])
    return render(request, 'characterpage.html', {'character': characterList[0], 'comicList': comicList})


def get_creatorpage(request):
    creatorId = request.GET.get('id')
    creator = Creator.objects.raw('SELECT * FROM Creators WHERE CreatorID = %s', [creatorId])
    writerList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Writer"', [creatorId])

    pencillerList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Penciller"', [creatorId])

    inkerList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Inker"', [creatorId])

    coloristList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Colorist"', [creatorId])

    lettererList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Letterer"', [creatorId])

    editorList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'INNER JOIN CreatorTypes ON ComicCreators.CreatorTypeID = CreatorTypes.CreatorTypeID '
                                   'WHERE Creators.CreatorID = %s AND CreatorTypeName = "Editor"', [creatorId])

    coverArtistList = Comic.objects.raw('SELECT DISTINCT Comics.ComicID, ComicIssueTitle, Creators.CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
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
    comics = Comic.objects.raw('SELECT ComicID, ComicIssueTitle FROM Comics ORDER BY ComicIssueTitle ASC')
    return render(request, 'comic.html',{'comics': comics})


def get_character(request):
    characters = Character.objects.raw('SELECT CharacterID, CharacterName FROM Characters ORDER BY CharacterName ASC')
    return render(request, 'character.html', {'characters': characters})


def get_creator(request):
    creators = Creator.objects.raw('SELECT CreatorID,CreatorName,CreatorDOB FROM Creators ORDER BY CreatorName ASC')
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


#def rate_comic(request, rating):
#    pass
#def post_comment():


def get_profile(request):
    return render(request, 'profile.html')


def get_signuppage(request):
    return render(request, 'signup.html')


def get_about(request):
    return render(request, 'about.html')



