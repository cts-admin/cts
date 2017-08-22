$("#id_amount")
    .change(function () {
        if ($(this).val() === 'custom') {
            $(this).remove();
            $('.custom-donation')
                .append('<input class="form-group form-control" type="number" name="amount" value="25">').show();
            var input = $('.custom-donation input');
            input.focus();
            // here we're moving the "focus" at the end of the input text
            var tmpStr = input.val();
            input.val('');
            input.val(tmpStr);
            setDonateButtonText();
        }
    });

$("#id_interval")
    .change(function () {
        setDonateButtonText();
    });

function setDonateButtonText() {
    var text = 'Donate';
    var interval = $('#id_interval').val();
    if (interval != 'onetime') {
        text += ' ' + interval;
    }
    $('#donate-btn').html(text);
}