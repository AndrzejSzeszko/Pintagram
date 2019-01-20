let likeIcon     = $('.fa-thumbs-up');
let isPostLiked  = likeIcon.data('is-post-liked') === 'True';
let postId       = likeIcon.data('post-id');
let likesCounter = likeIcon.siblings("span");

if (isPostLiked) {
    likeIcon.css('color', '#2d7fc8')
}

likeIcon.on('click', function(){
    if (isPostLiked) {
        $.ajax({
            url: 'http://127.0.0.1:8000/post_like/',
            data: {'like_or_unlike': 'unlike', 'post_id': postId},
            type: 'GET', // todo zrobić tu DELETE
            dataType: 'json',
        })
        .done(function () {
            let currentCounterValue = parseInt(likesCounter.text());
            let properCounterValue = currentCounterValue - 1;
            likesCounter.text(properCounterValue);
            likeIcon.css('color', '');
            isPostLiked = false;
        })
    } else {
        $.ajax({
            url: 'http://127.0.0.1:8000/post_like/',
            data: {'like_or_unlike': 'like', 'post_id': postId},
            type: 'GET', // todo zrobić tu POST
            dataType: 'json',
        })
        .done(function () {
            let currentCounterValue = parseInt(likesCounter.text());
            let properCounterValue = currentCounterValue + 1;
            likesCounter.text(properCounterValue);
            likeIcon.css('color', '#2d7fc8');
            isPostLiked = true;
        })
    }
});
