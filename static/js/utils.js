
function onButtonClicked(url_for, selected_row_details){
    let data = {"torrent_details": selected_row_details};
    $.ajax({
        url: url_for,
        type: 'POST',
        processData: false,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            $("body").html(response);
            console.log('success');
        },
        error: function (response) {
            $("body").html(response);
            console.log('error');

        }
    })

}