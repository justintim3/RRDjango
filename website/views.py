from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def homepage(request):
    newsFeed = NewsFeed.objects.raw('select * from website_newsfeed limit 10')
    comics = Comic.objects.raw('select ComicID,ComicIssueTitle from Comics limit 10' )
    return render(request, 'homepage/homepage.html', {'newsFeeds': newsFeed , 'comics': comics })


def get_comicpage(request):
    comicId = request.GET.get('id')
  
    comicList = Comic.objects.raw('select ComicID,ComicIssueTitle,ComicIssueNumber,ComicImage,ComicCoverDate,ComicPrice,ComicFormat,ComicSynopisis,(ComicRatingSum/ComicNumberOfRaters) as ComicRating, ComicViewRanking from Comics where ComicID = %s', [comicId])
    characterList = Character.objects.raw('SELECT DISTINCT Characters.CharacterID, CharacterName FROM Comics '
                                       'INNER JOIN ComicCharacters ON Comics.ComicID = ComicCharacters.ComicID '
                                       'INNER JOIN Characters ON ComicCharacters.CharacterID = Characters.CharacterID '
                                       'WHERE Comics.ComicID = %s', [comicId])
    creatorList = Creator.objects.raw('SELECT DISTINCT Creators.CreatorID, CreatorName FROM Comics '
                                   'INNER JOIN ComicCreators ON Comics.ComicID = ComicCreators.ComicID '
                                   'INNER JOIN Creators ON ComicCreators.CreatorID = Creators.CreatorID '
                                   'WHERE Comics.ComicID = %s', [comicId])
    series = Series.objects.raw('SELECT DISTINCT ComicID, Series.SeriesID, SeriesName FROM Comics '
                                    'INNER JOIN Series ON Comics.SeriesID = Series.SeriesID '
                                    'WHERE ComicID = %s', [comicId])
    publisher = Publishers.objects.raw('SELECT DISTINCT Comics.ComicID, Publishers.PublisherID, PublisherName FROM Comics '
                                      'INNER JOIN Publishers ON Comics.PublisherID = Publishers.PublisherID '
                                      'WHERE Comics.ComicID = %s', [comicId])

    return render(request, 'comicpage.html', {'comic': comicList[0], 'characterList': characterList,
                                              'creatorList': creatorList, 'series': series[0],
                                              'publisher': publisher[0]} )


def get_characterpage(request):
    characterId = request.GET.get('id')
    characterList = Character.objects.raw('SELECT * FROM Characters WHERE CharacterID = %s', [characterId])
    return render(request, 'characterpage.html', {'character': characterList[0]})


def get_newsfeedpage(request):
    newsFeedID = request.GET.get('id')
    newsFeed = NewsFeed.objects.raw('select * from website_newsfeed where ID = %s', [newsFeedID])
    return render(request, 'newsfeedpage.html', {'newsFeed': newsFeed[0]})


def get_creatorpage(request):
    creatorId = request.GET.get('id')
    creatorList = Creator.objects.raw('SELECT * FROM Creators WHERE CreatorID = %s', [creatorId])
    return render(request, 'creatorpage.html', {'creator': creatorList[0]})


def get_comic(request):
    comics = Comic.objects.raw('select ComicID,ComicIssueTitle from Comics')
    return render(request, 'comic.html',{'comics': comics})


def get_character(request):
    characters = Character.objects.raw('select CharacterID,CharacterName from Characters')
    return render(request, 'character.html', {'characters': characters})


def get_creator(request):
    creators = Creator.objects.raw('select CreatorID,CreatorName,CreatorDOB from Creators')
    return render(request, 'creator.html', {'creators': creators})


def get_newsfeed(request):
    newsFeed = NewsFeed.objects.raw('select * from website_newsfeed')
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
    return render(request, 'profile.html')


def get_signuppage(request):
    return render(request, 'signup.html')


def get_about(request):
    return render(request, 'about.html')



