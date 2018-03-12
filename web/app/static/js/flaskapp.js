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

