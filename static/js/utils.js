
function on_download_button_clicked(url_for, data){
    $.ajax({
        url: url_for,
        type: 'POST',
        data: JSON.jsonify(data),
        headers: {"content-type": "application/json"}
        success: function (response) {
            console.log('success');
        }
        error: function (response) {
            console.log('success');

        }
    })

}