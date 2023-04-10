
  $( document ).ready(function() {
    ////////////////////////////////////////
    
    $('.item').click(function(){
        $(this).toggleClass('active')
        countChosenImages()
    })

    function countChosenImages(){
        let count = $('.item.active').length
        if (count == 0) {
        escAvatars()
        } else {
        $('#image-count p').text(count)
        $('#esc-avatars').show()
        $('#load-button').show()
        $('#chosen-avatars-link').show()
        }
        
    }

    function escAvatars(){
        $('#esc-avatars').hide()
        $('#load-button').hide()
        $('#chosen-avatars-link').hide()
        $('.item').removeClass('active')
        $('#image-count p').text('Выберите фото')
        
    }
    $('#esc-avatars').click(function(){
        escAvatars()
    })

    
    function getChosenAvatarsId(){
        // получить список id выбраных аватарок
        let chosenAvatars = $('.item.active')
        let ids = []
        chosenAvatars.each(function(){
        avatarId = $(this).data('id')
        ids.push(avatarId)
        })
        return ids
    }

    
    // ссылка на просмотр выбранных аватарок
    $('#chosen-avatars-link').click(function(){
        let strIds = getChosenAvatarsId().join(',')
        // let url = "{%url 'image_store:chosen_avatars'%}?avatars_ids=" + strIds
        let url = "/avatars/chosen_avatars?avatars_ids=" + strIds
        window.open(url, '_blank')
    })

    

    $('#load-button').click(function(){
        console.log('DOWNLOAD')
        let strIds = getChosenAvatarsId().join(',')
        // let url = "{%url 'image_store:download_chosen_avatars'%}?avatars_ids=" + strIds
        let url = "/avatars/download_chosen_avatars?avatars_ids=" + strIds   
        window.open(url, '_self')
    })



    // При клике на ESC
    $(document).keyup(function(e) {
        if (e.key === "Escape") { // escape key maps to keycode `27`
        escAvatars()
        }
    });
////////////////////////////////////////
});
  
  