$(function () {
    $(document).on('submit', '#login', function (e) {
        e.preventDefault();

        $.post($(this).attr('action'), $(this).serialize())
            .done(function (data) {
                $('#account-box').html(data.html);
            })
            .fail(function (xhr) {
                const errors = xhr.responseJSON ? xhr.responseJSON.errors : { '': ['An error occurred.'] };
                const messages = Object.values(errors).flat();
                $('#login-errors').empty();
                $.each(messages, function (i, message) {
                    $('#login-errors').append($('<p>').text(message));
                });
            });
    });

    $(document).on('submit', '#logout', function (e) {
        e.preventDefault();

        $.post($(this).attr('action'), $(this).serialize())
            .done(function (data) {
                $('#account-box').html(data.html);
            });
    });
});