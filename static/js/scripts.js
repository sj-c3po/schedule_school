var remember_changed_load = [];

//function send_classes() {
//    var classes = [];
//
//    $('#classes_form .classname').each(function() {
//        if ($(this).val() != '') {
//           classes.push($(this).attr('name').split('_').join(''));
//        }
//    });
//    console.log(classes)  // ["5а", "5б", "5в"]
//
//    $.ajax({
//      url: '/add_subject',
//      type: "POST",
//      data: JSON.stringify(classes),
//      success: console.log('ok')
//    });
//}

function to_step(elem, step) {
    if ($(elem).hasClass('s1') || step == 1) {
        $('.step1').show(); $('.s1 b').show(); $('.desc1').show();
        $('.step2').hide(); $('.s2 b').hide(); $('.desc2').hide();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'bold');
        $('.s2').css('font-weight', 'normal');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(elem).hasClass('s2') || step == 2) {
        $('.step1').hide(); $('.s1 b').hide(); $('.desc1').hide();
        $('.step2').show(); $('.s2 b').show(); $('.desc2').show();
        $('.step3').hide(); $('.s3 b').hide(); $('.desc3').hide();
        $('.s1').css('font-weight', 'normal');
        $('.s2').css('font-weight', 'bold');
        $('.s3').css('font-weight', 'normal');
    }
    if ($(elem).hasClass('s3') || step == 3) {
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

function prepare_for_generate() {
//    alert('Молодец, иди гуляй')

//    var data = $('.step2 table th').text();
    var counter = 0;
    var classes = [];
//    console.log(data)

    $($('.step2 table th')).each(function() {
        counter++;
        if (counter >= 3) {
            console.log('Привет', counter)
            console.log($(this).innerText);
            $(classes).append($(this));
        }
    });

    console.log(classes)



}

function add(data) {
    if ($(data).hasClass('add_subject')) {
        open_modal('modal_add_subject');
    }
    if ($(data).hasClass('add_teacher')) {
        open_modal('modal_add_teacher');
    }
}
function del(data) {

    var delete_id = [];
    if ($("input:checkbox:checked")) {
        $("input:checkbox:checked").each(function() {
            delete_id.push($(this).attr('data-subject-id'))

        });
        console.log(delete_id)
        $.post(
            '/new/delete_object',
            {id: delete_id},
            function() {
//                alert('Изменения приняты')
            }
        ).fail(function() {
                alert( "Возникла ошибка :(" )
                location.reload();
            });
    }
}

function remember_load(load) {
    remember_changed_load.push({ 'sclass': $(load).attr('data-class-id'), 'subject': $(load).attr('data-subject-id'), 'newval': $(load).val() });
}

function save_changes() {
    $.post(
        '/new',
        {'changes': remember_changed_load},
        function() {alert('Изменения приняты')}
    ).fail(function() {
            alert( "Нет, так проставлять нельзя. Только через базу." )
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

function add_subj(window) {
    var subject_name = $('#modal_add_subject input[name=subject_name]').val();
    var classes = [];
    var weekload = [];

    $("input:checkbox:checked").each(function() {
        classes.push(($(this).attr('data-class-id')))
    });
    console.log(classes);

    $("input[name=week_load]").each(function() {
        if ($(this).val() != '') {
            weekload.push(($(this).val()))
        }
    });
    console.log(weekload);

//    var week_load = [];
//    $('#modal_add_subject input[name=week_load]').each(function() {
//         week_load.push($(this).val())
//    });
//
//    console.log(subject_name, classes, week_load)

    $.post(
        '/add_subject',
        {'subject_name': subject_name , 'classes': classes, 'weekload': weekload},
        function() {
//            alert('Изменения приняты')
//            close_modal(window)
        }
    ).fail(function() {
        alert( "Косяк :с" )
    });
}
