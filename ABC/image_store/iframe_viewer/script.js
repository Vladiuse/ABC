
    console.log('custom JS START')
    $('img').click(function(){
        $(this).toggleClass('chosen')
        console.log('click')
    })
    // $('img').mousedown(function(){
    //     $(this).toggleClass('chosen')
    // })
    
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

    let a_to_prev = []
    function dropImagesLiks(){
        $('a').each(function(){
            if ($(this).children('img').length){
                a_to_prev.push($(this))
                $(this).attr('href', '')
                $(this).click(function(e){
                    e.preventDefault()
                })
            }
        })
        
    }
    $('a').click(function(e){
        e.preventDefault()
    })
    function removeA(){
        $('a').remove()
    }
    removeA()
    // dropImagesLiks()
    console.log('custom JS in site WORK')
