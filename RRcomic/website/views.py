from django.shortcuts import render
from .models import Comic
from django.http import HttpResponse
from .models import NewsFeed
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


def homepage(request):
    cookie = request.COOKIES.get("RRID")
    name= request.COOKIES.get("RRName")
    newsFeed = NewsFeed.objects.raw ('select ID,Title,Text,Date from NewsFeed')
    comics = Comic.objects.raw('select ComicID,ComicIssueTitle from Comics Order by Rand() limit 10' )
    return render(request, 'homepage/homepage.html', {'newsfeeds' : newsFeed , 'comics': comics,'RRName':name ,'RRID':cookie })
    
def get_comic_page(request):
    comicId = request.GET.get('id')
    comics = Comic.objects.raw('select ComicIssueTitle from Comics where ComicID = %d', [comicId])
    #comics = Comic.objects.raw('select ComicID,ComicIssueTitle,ComicIssueNumber,ComicImage,ComicCoverDate,ComicPrice,ComicSynopisis,(ComicRatingSum/ComicNumberOfRaters) as ComicRating, ComicViewRanking from Comics where ComicID = %d', [comicId])
    return render(request, 'comicpage.html', {'comic': comics} )

def get_comic(request):
    comics = Comic.objects.raw('select ComicID,ComicIssueTitle,ComicIssueNumber,ComicImage,ComicCoverDate,ComicPrice,ComicSynopisis,(ComicRatingSum/ComicNumberOfRaters) as ComicRating, ComicViewRanking from Comics')
    return render(request, 'comic.html',{'comics':comics})

def verify_user(request):
    data = '{"success":true,"error":"Login failed!", "data":{"UserID":2,"UserDisplayName":"test"}}'
    #return render(request, 'json.html', {'data':data})
    return HttpResponse (data, content_type = 'application/json')

def create_user(request):
    return render(request, 'json.html', {'data':data})
