let likeIcon     = $('.fa-thumbs-up');
let isLiked      = likeIcon.data('is-liked');
let userId       = likeIcon.data('user-id');
let postId       = likeIcon.data('post-id');
let likesCounter = likeIcon.siblings();

if (isLiked === 'True') {
    likeIcon.css('color', 'blue')
}

likeIcon.on('click', function(){
    if (isLiked === 'True') {
        $.ajax({
            url: 'http://127.0.0.1:8000/post_likes/',
            data: {'like_or_unlike': 'unlike', 'user_id': userId, 'post_id': postId},
            type: 'GET',
            dataType: 'json',
        })
        .done(function () {
            let currentCounterValue = parseInt(likesCounter.text());
            let properCounterValue = currentCounterValue - 1;
            likesCounter.text(properCounterValue);
            likeIcon.css('color', '');
            isLiked = 'False';
        })
    } else {
        $.ajax({
            url: 'http://127.0.0.1:8000/post_likes/',
            data: {'like_or_unlike': 'like', 'user_id': userId, 'post_id': postId},
            type: 'GET',
            dataType: 'json',
        })
        .done(function () {
            let currentCounterValue = parseInt(likesCounter.text());
            let properCounterValue = currentCounterValue + 1;
            likesCounter.text(properCounterValue);
            likeIcon.css('color', 'blue');
            isLiked = 'True';
        })
    }
});
