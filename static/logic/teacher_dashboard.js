$(document).ready(function () {
    fetchClassDetails();
    $('#save_cls_details').click(function () {
        saveClassDetails();
    })
});


function saveClassDetails() {
    const className = $('#cls_name').val();
    const classSubject = $('#sub_name').val();
    const classDate = $('#cls_date').val();
    const classTime = $('#cls_time').val();

    if (!(className && classSubject && classDate && classTime)) {
        swal('Please fill all the fields');
        return false;
    } else {
        const details = {
            'className': className,
            'classSubject': classSubject,
            'classDate': classDate,
            'classTime': classTime
        };
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            type: 'POST',
            url: '/save_class_details/',
            headers: {'X-CSRFToken': csrftoken},
            data: details,
            success: function (response) {
                if (response.result === 'success') {
                    swal(response.msg);
                } else if (response.result === 'invalid_request') {
                    swal(response.msg);
                } else if (response.result === 'failed') {
                    swal(response.msg);
                }
                resetForm();
                fetchClassDetails();
            }, error: function (error) {
                console.log("Error in saveClassDetails function -->", error);
            }
        })
    }
}


function resetForm() {
    $('#cls_name,#sub_name,#cls_date,#cls_time').val('')
}


function fetchClassDetails() {
    let clsDetails;
    $.ajax({
        type: 'POST',
        url: '/fetch_class_details/',
        success: function (response) {
            if (response.result === 'success') {
                let count = 1;
                $('#display_cls_details>tbody').empty();
                response.cls_details.forEach(function (details) {
                    clsDetails = "<tr>" +
                        "<td>" + count + "</td>" +
                        "<td>" + details.class_name + "</td>" +
                        "<td>" + details.class_subject + "</td>" +
                        "<td>" + details.class_date + "</td>" +
                        "<td>" + details.class_time + "</td>" +
                        "<td>" + details.number_of_students + "</td>" +
                        "</tr>";
                    $('#display_cls_details>tbody').append(clsDetails);
                    count++;
                });
            } else if (response.result === 'failed') {
                swal(response.msg);
            }
        }, error: function (error) {
            console.log("Error in fetchClassDetails function -->", error);
        }
    })
}