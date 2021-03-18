$(document).ready(function () {
    fetchAllClassDetails();
    fetchMyEnrolledClasses();
});

function fetchAllClassDetails() {
    let clsDetails;
    $.ajax({
        type: 'POST',
        url: '/fetch_all_class_details/',
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
                        "<td><button class='btn btn-sm btn-primary enroll-class' id='" + details.class_id + "'>Enroll</button></td>" +
                        "</tr>";
                    $('#display_cls_details>tbody').append(clsDetails);
                    count++;
                });

                $('.enroll-class').click(function () {
                    const clsId = $(this).attr('id');
                    $.ajax({
                        type: 'POST',
                        url: '/enroll_class/',
                        data: {'clsId': clsId},
                        success: function (response) {
                            if (response.result === 'success') {
                                fetchAllClassDetails();
                                fetchMyEnrolledClasses();
                            } else if (response.result === 'failed') {
                                swal(response.msg);
                            }
                        }, error: function (error) {
                            console.log("Error in class enroll function -->", error);
                        }
                    })
                })


            } else if (response.result === 'failed') {
                swal(response.msg);
            }
        }, error: function (error) {
            console.log("Error in fetchClassDetails function -->", error);
        }
    })
}


function fetchMyEnrolledClasses() {
    let clsDetails;
    $.ajax({
        type: 'POST',
        url: '/fetch_my_enrolled_classes/',
        success: function (response) {
            if (response.result === 'success') {
                let count = 1;
                $('#my_enrolled_classes>tbody').empty();
                response.cls_details.forEach(function (details) {
                    clsDetails = "<tr>" +
                        "<td>" + count + "</td>" +
                        "<td>" + details.class_name + "</td>" +
                        "<td>" + details.class_subject + "</td>" +
                        "<td>" + details.class_date + "</td>" +
                        "<td>" + details.class_time + "</td>" +
                        "<td>" + details.number_of_students + "</td>" +
                        "<td><button class='btn btn-sm btn-danger' id='" + details.class_id + "' disabled>Enrolled</button></td>" +
                        "</tr>";
                    $('#my_enrolled_classes>tbody').append(clsDetails);
                    count++;
                });

            } else if (response.result === 'failed') {
                swal(response.msg);
            }
        }, error: function (error) {
            console.log("Error in fetchMyEnrolledClasses function -->", error);
        }
    })
}