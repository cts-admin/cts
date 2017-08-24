var $amount = $("#id_amount");
var $membershipLevel = $("#id_membership_level");

$amount
    .change(function() {
        setMembershipLevel();
    });

$membershipLevel
    .change(function () {
        setDonationAmount();
    });

function setDonationAmount() {
    var selectedMembership = $membershipLevel.val();
    if (selectedMembership === '5') {
        $amount.val(25000);
    } else if (selectedMembership === '4') {
        $amount.val(10000);
    } else if (selectedMembership === '3') {
        $amount.val(5000);
    } else if (selectedMembership === '2') {
        $amount.val(3000);
    } else if (selectedMembership === '1') {
        $amount.val(1500);
    } else {
        $amount.val('');
    }
}

function setMembershipLevel() {
    var amount = parseInt($amount.val());
    if (amount >= 25000) {
        $membershipLevel.val(5);
    } else if (amount >= 10000) {
        $membershipLevel.val(4);
    } else if (amount >= 5000) {
        $membershipLevel.val(3);
    } else if (amount >= 3000) {
        $membershipLevel.val(2);
    } else if (amount >= 1500) {
        $membershipLevel.val(1);
    } else {
        $membershipLevel.val('');
    }
}
