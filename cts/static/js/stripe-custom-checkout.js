var $donationForm = $('.stripe-custom-checkout');
var $submitButton = $donationForm.find('#donate');

var handler = StripeCheckout.configure({
    key: $donationForm.attr('data-stripe-key'),
    image: $donationForm.attr('data-stripe-icon'),
    locale: 'auto',
    token: function (token) {
        $submitButton.prop('disabled', true).addClass('disabled');
        var amount = $donationForm.find('[name=amount]').val();
        var csrfToken = $donationForm.find('[name=csrfmiddlewaretoken]').val();
        var interval = $donationForm.find('[name=interval]').val();
        var data = {
            'stripe_token': token.id,
            'token_type': token.type,
            'receipt_email': token.email,
            'amount': amount,
            'interval': interval,
            'csrfmiddlewaretoken': csrfToken
        };

        $.ajax({
            type: "POST",
            url: $donationForm.attr('action'),
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    window.location = data.redirect;
                } else {
                    $submitButton.prop('disabled', false).removeClass('disabled');
                    alert(data.error);
                }
            }
        })
    }
});

// Close Checkout on page navigation
$(window).on('popstate', function () {
    handler.close();
});

$donationForm.on('submit', function (e) {
    e.preventDefault();
    var amountDollars = $donationForm.find('[name=amount]').val();
    var amountCents = parseFloat(amountDollars) * 100;

    handler.open({
        name: 'Conservation Technology Solutions Inc',
        description: 'CTS Donation',
        amount: amountCents,
        currency: 'USD',
        bitcoin: true,
        zipCode: true,
        billingAddress: true,
        panelLabel: 'Donate'
    });
});