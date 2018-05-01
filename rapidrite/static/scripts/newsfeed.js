//replace getNews.js with this

$.ajax({
    type: 'GET',
    url: 'https://comicvine.gamespot.com/feeds/news',
    dataType: 'xml',
    success: function(data) {
        var liHTML_template =
            '<li>' +
            '<div class="media">' +
                '<div class="media-ele">' +
                    '</div>' +
                '<div class="media-bd">' +
                    '<div class="box">' +
                        '<div class="box-hd box-hd_min threeLines">' +
                    '       <h4 class="hdg">' +
                        '       <a href="{link}" target="_blank">' +
                                    '{title}' +
                                    '</a>' +
                                '</h4>' +
                            '</div>' +
                        '<div class="box-ft">' +
                            '<p class="txt_miniscule">' +
                                '{pubDate}' +
                                '</p>' +
                            '</div>' +
                        '<div class ="box-ft">' +
                            '<p>' +
                                '{description}' +
                                '</p>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</li>';
        var ulHTML = "";
        $(data).find("item").each(function () {
            var title = $(this).find("title").text();
            var link = $(this).find("link").text();
            var pubDate = $(this).find("pubDate").text();
            var description = $(this).find("description").text();

            ulHTML += liHTML_template.replace('{title}', title).replace('{link}', link).replace('{pubDate}', pubDate).replace('{description}', pubDate);

            //debug
            console.log(ulHTML);
        });

        $('#FeedContainer > div > div.feed-bd > ul').html(ulHTML);

    },
    error: function(jqXHR, textStatus, errorThrown ) {
        console.log(errorThrown);
    }

});