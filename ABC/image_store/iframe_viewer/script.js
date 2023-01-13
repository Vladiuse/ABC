
    $('img').click(function(){
        $(this).toggleClass('chosen')
    })
    function getUrlOfChosen(){
        console.log('getUrlOfChosen')
        images = $('img.chosen')
        urls = []
        $.each(images,function(){
            urls.push($(this).attr('src'))
        })
        return urls
    }
    function removeAllChosen(){
        $('img.chosen').removeClass('chosen')
    }
       var country_iframe = 'XX'
    console.log(country, country_iframe,'in iframe')
    console.log('JQ')