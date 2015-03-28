var settings = {
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    stepsOrientation: "vertical",
    labels: {
        finish: "Сгенерировать",
        next: "Далее",
        previous: "Назад"
    }
};

$(document).ready(function() {
    $("#steps").steps(settings);
});

function send_classes() {
    var classes = [];

    $('#classes_form .classname').each(function() {
        if ($(this).val() != '') {
           classes.push($(this).attr('name').split('_').join(''));
        }
    });
    console.log(classes)  // ["5а", "5б", "5в"]

    $.ajax({
      url: '/processing_data',
      type: "POST",
      data: JSON.stringify(classes),
      success: console.log('ok')
    });
}

function to_step(step) {
    if ($(step).hasClass('s1')) {
        $('.step1').show(); $('.s1 b').show();
        $('.step2').hide(); $('.s2 b').hide();
        $('.step3').hide(); $('.s3 b').hide();
        $('.s1').css('font-weight', 'bold');
        $('.s2').css('font-weight', 'normal');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(step).hasClass('s2')) {
        $('.step1').hide(); $('.s1 b').hide();
        $('.step2').show(); $('.s2 b').show();
        $('.step3').hide(); $('.s3 b').hide();
        $('.s1').css('font-weight', 'normal');
        $('.s2').css('font-weight', 'bold');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(step).hasClass('s3')) {
        $('.step1').hide(); $('.s1 b').hide();
        $('.step2').hide(); $('.s2 b').hide();
        $('.step3').show(); $('.s3 b').show();
        $('.s1').css('font-weight', 'normal');
        $('.s2').css('font-weight', 'normal');
        $('.s3').css('font-weight', 'bold');
    }
}

function next_step(step) {
    var current_step = $(step).parent();

    if ($(current_step).hasClass('step1')) {
        $('.step1').hide(); $('.s1 b').hide();
        $('.step2').show(); $('.s2 b').show();
        $('.step3').hide(); $('.s3 b').hide();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'bold'); $('.s3').css('font-weight', 'normal');
    }
    if ($(current_step).hasClass('step2')) {
        $('.step1').hide(); $('.s1 b').hide();
        $('.step2').hide(); $('.s2 b').hide();
        $('.step3').show(); $('.s3 b').show();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'normal'); $('.s3').css('font-weight', 'bold');
    }
}

function prev_step(step) {
    var current_step = $(step).parent();

    if ($(current_step).hasClass('step2')) {
        $('.step1').show(); $('.s1 b').show();
        $('.step2').hide(); $('.s2 b').hide();
        $('.step3').hide(); $('.s3 b').hide();
        $('.s1').css('font-weight', 'bold'); $('.s2').css('font-weight', 'normal'); $('.s3').css('font-weight', 'normal');
    }
    if ($(current_step).hasClass('step3')) {
        $('.step1').hide(); $('.s1 b').hide();
        $('.step2').show(); $('.s2 b').show();
        $('.step3').hide(); $('.s3 b').hide();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'bold'); $('.s3').css('font-weight', 'normal');
    }
}

function finish_step() {
    alert('Молодец, иди гуляй')
}