var remember_changed_load = [];

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
        $('.step1').show(); $('.s1 b').show(); $('.desc1').show();
        $('.step2').hide(); $('.s2 b').hide(); $('.desc2').hide();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'bold');
        $('.s2').css('font-weight', 'normal');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(step).hasClass('s2')) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').show(); $('.s2 b').show(); $('.desc2').show();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'normal');
        $('.s2').css('font-weight', 'bold');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(step).hasClass('s3')) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').hide(); $('.s2 b').hide(); $('.desc2').hide();
        $('.step3').show(); $('.s3 b').show(); $('.desc3').show();
        $('.s1').css('font-weight', 'normal');
        $('.s2').css('font-weight', 'normal');
        $('.s3').css('font-weight', 'bold');
    }
}

function next_step(step) {
    var current_step = $(step).parent().parent();

    if ($(current_step).hasClass('step1')) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').show(); $('.s2 b').show(); $('.desc2').show();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'bold'); $('.s3').css('font-weight', 'normal');
    }
    if ($(current_step).hasClass('step2')) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').hide(); $('.s2 b').hide(); $('.desc2').hide();
        $('.step3').show(); $('.s3 b').show(); $('.desc3').show();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'normal'); $('.s3').css('font-weight', 'bold');
    }
}

function prev_step(step) {
    var current_step = $(step).parent().parent();

    if ($(current_step).hasClass('step2')) {
        $('.step1').show(); $('.s1 b').show(); $('.desc1').show();
        $('.step2').hide(); $('.s2 b').hide(); $('.desc2').hide();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'bold'); $('.s2').css('font-weight', 'normal'); $('.s3').css('font-weight', 'normal');
    }
    if ($(current_step).hasClass('step3')) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').show(); $('.s2 b').show(); $('.desc2').show();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'normal'); $('.s2').css('font-weight', 'bold'); $('.s3').css('font-weight', 'normal');
    }
}

function finish_step() {
    alert('Молодец, иди гуляй')
}

function add(data) {
    if ($(data).hasClass('add_subject')) {
        open_modal('modal_add_subject');
    }
    if ($(data).hasClass('add_cabinet')) {
        open_modal('modal_add_cabinet');
    }
    if ($(data).hasClass('add_teacher')) {
        open_modal('modal_add_subject');
    }
}
function del(data) {
    if ($('input[type=checkbox]').attr('checked')) {
        if ($(data).hasClass('del_subject')) {
            console.log($('input[type=checkbox]').attr("checked"))
        }
    } else {
        console.log('Нечего)')
    }
}

function remember_load(load) {
    remember_changed_load.push({ 'sclass': $(load).attr('data-class'), 'subject': $(load).attr('data-subject'), 'newval': $(load).val() });
}

function save_changes() {
    $.post(
        '/new',
        {'changes': remember_changed_load},
        function() {alert('Изменения приняты')}
    ).fail(function() {
            alert( "Возникла ошибка :(" )
            location.reload();
        });
}


function choose_all_subjects(box) {
    if (box.checked) {
        $("input[type=checkbox]").attr('checked', true);
    } else {
        $("input[type=checkbox]").attr('checked', false);
    }
}

//function change_checkbox_value(box) {
//    if ($(box).attr('checked')==true) {
//        $(box).attr('checked', false)
//    } else {
//        $(box).attr('checked', true)
//    }
//}