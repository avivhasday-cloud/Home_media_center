
function onButtonClicked(url_for, selected_row_details, method){
    let data = {"torrent_details": selected_row_details};
    console.log(method);
    $.ajax({
        url: url_for,
        type: method,
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