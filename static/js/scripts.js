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