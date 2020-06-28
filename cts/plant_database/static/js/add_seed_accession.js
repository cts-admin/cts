let form_count = Number($("[name=add_collector_count]").val());
let remove_btn = $("#remove-another");

$("#add-another").click(function (e) {
    e.preventDefault();
    if (form_count < 6) {
        form_count++;

        // New first name input
        let fn_fg = $('<div id="fn-fg-' + form_count + '" class="form-group"></div>');
        let fn_label = $('<label for="id_col_fname_' + form_count + '">Collector #' + form_count + ' first name</label>');
        let fn_input = $('<input id="id_col_fname_' + form_count + '" class="form-control" type="text" ' +
            'name="col_fname_' + form_count + '" placeholder="First name" maxlength="30">');
        fn_fg.append(fn_label);
        fn_fg.append(fn_input);

        // New last name input
        let ln_fg = $('<div id="ln-fg-' + form_count + '" class="form-group"></div>');
        let ln_label = $('<label for="id_col_lname_' + form_count + '">Collector #' + form_count + ' last name</label>');
        let ln_input = $('<input id="id_col_lname_' + form_count + '" class="form-control" type="text" ' +
            'name="col_fname_' + form_count + '" placeholder="Last name" maxlength="30">');
        ln_fg.append(ln_label);
        ln_fg.append(ln_input);

        // Add the new elements to the form
        fn_fg.insertBefore(e.target);
        ln_fg.insertBefore(e.target);

        // Update the hidden field with the current count of collector input groups
        $("[name=add_collector_count]").val(form_count);
    }

    // Make sure the remove button isn't hidden
    if (remove_btn.hasClass("hidden")) {
        remove_btn.removeClass("hidden");
    }
});

remove_btn.click(function (e) {
    e.preventDefault();

    // Remove the most recently added collector input groups
    $("#fn-fg-" + form_count).remove();
    $("#ln-fg-" + form_count).remove();

    // Decrement the count of collector groups
    form_count--;
    $("[name=add_collector_count]").val(form_count);

    // Check if we should hide the button
    if (form_count < 2 && !remove_btn.hasClass("hidden")) {
        remove_btn.addClass("hidden");
    }
});

