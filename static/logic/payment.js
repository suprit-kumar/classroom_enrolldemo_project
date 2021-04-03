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
                console.log(data);
                /* var options = {
                 "key": "rzp_test_acwK6v5DquQz6l",
                 "amount": data.amount,
                 "currency": "INR",
                 "name": "Transaction Corp",
                 "description": "Test Transaction",
                 "image": "https://example.com/your_logo",
                 "order_id":data.my_payment['id'],
                 "handler": function (response) {
                 console.log(response.razorpay_payment_id);
                 console.log(response.razorpay_order_id);
                 console.log(response.razorpay_signature)
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
                 var rzp1 = new Razorpay(options);
                 rzp1.on('payment.failed', function (response) {
                 console.log(response.error.code);
                 console.log(response.error.description);
                 console.log(response.error.source);
                 console.log(response.error.step);
                 console.log(response.error.reason);
                 console.log(response.error.metadata.order_id);
                 console.log(response.error.metadata.payment_id);
                 });
                 document.getElementById('rzp-button1').onclick = function (e) {
                 rzp1.open();
                 e.preventDefault();
                 }*/
            }, error: function (error) {

            }
        })
    }
}