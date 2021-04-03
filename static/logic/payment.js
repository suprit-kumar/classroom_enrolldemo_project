$(document).ready(function () {

    $("#init_payment").click(function () {
        makePayment();
    });

});

function makePayment() {
    const itemName = $('#item_name').val();
    const itemPrice = $('#price').val();

    if (!itemName) {
        swal('Enter Item name');
        return false;
    } else if (!itemPrice) {
        swal('Enter Item Price');
        return false;
    } else {
        $.ajax({
            type: 'POST',
            url: '/generate_payment_order/',
            data: {'itemName': itemName, 'itemPrice': itemPrice},
            success: function (data) {
                processPayment(data)
            }, error: function (error) {
                console.log(error);
            }
        })
    }
}


function processPayment(data) {
    var options = {
        "key": "rzp_test_acwK6v5DquQz6l",
        "amount": data.amount,
        "currency": "INR",
        "name": "Transaction Corp",
        "description": "Test Transaction",
        "image": "https://example.com/your_logo",
        "order_id": data.my_payment['id'],
        "handler": function (response) {
            saveToDb(response);
        },
        "prefill": {
            "name": "Suprit Kumar",
            "email": "supritkumar98@gmail.com",
            "contact": "9999999999"
        },
        "notes": {
            "address": "Razorpay Corporate Office"
        },
        "theme": {
            "color": "#3399cc"
        }
    };
    var raz_pay = new Razorpay(options);
    raz_pay.open();
    /*   raz_pay.on('payment.failed', function (response) {
     console.log(response.error.code);
     console.log(response.error.description);
     console.log(response.error.source);
     console.log(response.error.step);
     console.log(response.error.reason);
     console.log(response.error.metadata.order_id);
     console.log(response.error.metadata.payment_id);
     });*/
}


function saveToDb(response) {
    $.ajax({
        type: 'POST',
        url: '/update_transaction_db/',
        data: {
            'razorpay_payment_id': response.razorpay_payment_id,
            'razorpay_order_id': response.razorpay_order_id,
            'razorpay_signature': response.razorpay_signature,
        },
        success: function (response) {
            if (response.result === 'success') {
                swal("Success", "Payment Successfull!", "success");
                setTimeout(function () {
                    window.location.reload();
                }, 2500);
            }
        }, error: function (error) {
            console.log('Error in saveToDb ', error);
        }
    });
}