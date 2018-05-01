$(function(){
    var url = 'http://rss.nytimes.com/services/xml/rss/nyt/Movies.xml';
    var news = $('.news');
    function dateFormat(pubDate) {
        var date = new Date(pubDate);
        var months = Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");
        return date.getDate() + " " + months[date.getMonth()] + " " + date.getFullYear()
    }
    function loadNews(url) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: "xml"
          })
          .done(function(xml) {
              news.prepend()
              var i;
              for(i=0; i<5; i++) {
                  var self = $(xml).find('channel item').eq(i);
                  console.log("Found item");
                  var url = $(self).find('link').text();
                  console.log("Found item");
                  var title = $(self).find('title').text();
                  console.log("Found item");
                  var text = $(self).find('description').text();
                  console.log("Found item");
                  var date = $(self).find('pubDate').text();
                  console.log("Found item");
                  news.append('<h2>' + title + '</h2><p>' + dateFormat(date) + '</p><p>' + text + '</p><a href="' + url + '">Link</a>');
              }
          })
          //.fail(function(){
           // news.hide();
          //});
        }
        loadNews(url);
      });