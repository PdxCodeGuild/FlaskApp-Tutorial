/**
 * util method
 * @see somepage.html
 */
function doTest( param ) {
    alert("doTest("+param+")");
}


/**
 * add confirm dialog for <a> with data-confirm-link attribute
 * @see item_edit.html
 */
$(document).ready(function () {
    $('a[data-confirm-link]').click(function () {
        if (confirm($(this).data('confirm-link')))
            window.location = $(this).attr('href');
        return false;
    });
});


/**
 * Check/Uncheck all checkboxes with name attribute matching 'input_name'
 * @see item_list.html
 */
function checkAll( input_name, input_checked ) {
    //alert( "checkAll( "+input_name+", "+input_checked+" )" );
    $("input[type='checkbox']").each( function () {
        if ($(this).prop("name") != input_name) { return; }
        $(this).prop( "checked", input_checked );
    });
}
