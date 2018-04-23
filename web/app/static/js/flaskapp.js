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


/**
 * load /item/browse into target div
 * @see item_index.html
 */
function getItemBrowser( target )
{
//alert("getItemBrowser('"+target+"')");

    var urlParams = new URLSearchParams(window.location.search);
    var post_data = {}
    if (urlParams.has('status')) { post_data['status'] = urlParams.get('status'); }
    if (urlParams.has('sort'))   { post_data['sort']   = urlParams.get('sort'); }
    if (urlParams.has('order'))  { post_data['order']  = urlParams.get('order'); }
    if (urlParams.has('page'))   { post_data['page']   = urlParams.get('page'); }
    if (urlParams.has('limit'))  { post_data['limit']  = urlParams.get('limit'); }

    $.ajax({
        type: "POST"
        , url: '/item/browse/'
        , data: post_data
        , success: function(data) {
            $('#'+target).html(data);
        }
        , error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            $('#'+target).html('<div class="error">AJAX Error:\n'+errorThrown+' - '+jqXHR.responseText+'</div>');
        }
    });
}

/**
 * load /item/detail into target div
 * @see item_detail.html
 */
function getItemDetail( item_id, target )
{
//alert("getItemDetail("+item_id+")",'"+target+"')");

    $.ajax({
        type: "GET"
        , url: '/item/detail/'+item_id
        , success: function(data) {
            $('#'+target).html(data);
        }
        , error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            $('#'+target).html('<div class="error">AJAX Error:\n'+errorThrown+' - '+jqXHR.responseText+'</div>');
        }
    });
}

