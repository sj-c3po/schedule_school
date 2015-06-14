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
    if ($(data).hasClass('wishes')) {
        var ban_hours = $(data).parent().attr('data-ban-hours');
        console.log('ban', ban_hours)
        var teacher_id = $(data).parent().attr('data-teacher-id');
        var teacher_name = $(data).parent().attr('data-teacher-lastname') + ' ' +
                           $(data).parent().attr('data-teacher-firstname') + ' ' +
                           $(data).parent().attr('data-teacher-middlename');
        open_modal('wishes');
        create_modalwin(ban_hours, teacher_name, teacher_id)
    }
}

function create_modalwin(ban_hourss, teacher_name, teacher_id) {
    var ban_hours = []

    // без этого фигня с commaseparated полем
    $(ban_hourss.split(',')).each(function (b) {
        ban_hours.push(parseInt(ban_hourss.split(',')[b]))
    });

    $('#wishes b').html(teacher_name);
    $('#wishes .save_changes').attr('data-teacher-id', teacher_id);

    var table =  "<tr><th>День недели</th><th colspan='7'>Номер урока</th></tr>";
    table += "<tr class='mon'>";
    table += "<td class='allday green' onclick='change_the_state(this);'>Понедельник</td>";
    for (var l=1; l<8; l++) {
        if (ban_hours.indexOf(l-1) != -1) {
            table += "<td class='hour-"+l+" red' data-index="+(l-1)+" onclick='change_the_state(this);'>"+l+"</td>";
        } else {
            table += "<td class='hour-"+l+" green' data-index="+(l-1)+" onclick='change_the_state(this);'>"+l+"</td>";
        }
    }
    table += "</tr>";
    table += "<tr class='tue'>";
    table += "<td class='allday green' onclick='change_the_state(this);'>Вторник</td>";
    for (var l=1; l<8; l++) {
        if (ban_hours.indexOf(l+6) != -1) {
            table += "<td class='hour-"+l+" red' data-index="+(l+6)+" onclick='change_the_state(this);'>"+l+"</td>";
        } else {
            table += "<td class='hour-"+l+" green' data-index="+(l+6)+" onclick='change_the_state(this);'>"+l+"</td>";
        }
    }
    table += "</tr>";
    table += "<tr class='wed'>";
    table += "<td class='allday green' onclick='change_the_state(this);'>Среда</td>";
    for (var l=1; l<8; l++) {
        if (ban_hours.indexOf(l+13) != -1) {
            table += "<td class='hour-"+l+" red' data-index="+(l+13)+" onclick='change_the_state(this);'>"+l+"</td>";
        } else {
            table += "<td class='hour-"+l+" green' data-index="+(l+13)+" onclick='change_the_state(this);'>"+l+"</td>";
        }
    }
    table += "</tr>";
    table += "<tr class='thu'>";
    table += "<td class='allday green' onclick='change_the_state(this);'>Четверг</td>/";
    for (var l=1; l<8; l++) {
        if (ban_hours.indexOf(l+20) != -1) {
            table += "<td class='hour-"+l+" red' data-index="+(l+20)+" onclick='change_the_state(this);'>"+l+"</td>";
        } else {
            table += "<td class='hour-"+l+" green' data-index="+(l+20)+" onclick='change_the_state(this);'>"+l+"</td>";
        }
    }
    table += "</tr>";
    table +=  "<tr class='fri'>";
    table += "<td class='allday green' onclick='change_the_state(this);'>Пятница</td>";
    for (var l=1; l<8; l++) {
        if (ban_hours.indexOf(l+27) != -1) {
            table += "<td class='hour-"+l+" red' data-index="+(l+27)+" onclick='change_the_state(this);'>"+l+"</td>";
        } else {
            table += "<td class='hour-"+l+" green' data-index="+(l+27)+" onclick='change_the_state(this);'>"+l+"</td>";
        }
    }
    table += "</tr>";
    $('#wishes table.wishes > tbody').html(table);

    var week = ['.mon ', '.tue ', '.wed ', '.thu ', '.fri '];
    $(week).each(function(day){
        var cnt = 0;
        for (var l=1; l<8; l++) {
            if ($(week[day]+' > .hour-'+l).hasClass('red')) {
                cnt++;
//                console.log(cnt, $(week[day]+' > .hour-'+l))
            }
        }
        if (cnt == 7) {
            $(week[day]+ '> .allday').removeClass('green');
            $(week[day]+ '> .allday').addClass('red');
        }
    });
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


function change_the_state(item) {
    var color = '';
    if ($(item).hasClass('green')) {
        $(item).removeClass('green');
        $(item).addClass('red');
        color = 'red';
    } else {
        $(item).removeClass('red');
        $(item).addClass('green');
        color = 'green'
    }

    if ($(item).hasClass('allday')) {
        var hours = $(item).parent().children();

        $.each(hours, function(key, val) {
            if (!$(val).hasClass('allday')) {
                if (color == 'red') {
                    $(val).removeClass('green');
                    $(val).addClass('red');
                } else {
                    $(val).removeClass('red');
                    $(val).addClass('green');
                }
            }
        });
    }
}

function save_change_the_state(data) {
    var ban = [];
    var mon = 0, tue = 7, wed = 14, thu = 21, fri = 28;

    add_to_ban_hours(ban, 0, 'mon');
    add_to_ban_hours(ban, 7, 'tue');
    add_to_ban_hours(ban, 14, 'wed');
    add_to_ban_hours(ban, 21, 'thu');
    add_to_ban_hours(ban, 28, 'fri');
    console.log(ban);

    var red = $('td.red');
    $.each(red, function(key, val) {
        if (!$(val).hasClass('allday') && $(val).parent().children().first().hasClass('green')) {
            ban.push(parseInt($(val).attr('data-index')));
        }
    });
    console.log(ban);

    $.post(
            '/new/save_ban_days',
            {
                'ban': ban,
                'id': $(data).attr('data-teacher-id')
            },
            function() {
                alert('Дни отправлены');
                location.reload();
            }
        ).fail(function() {
                alert( "Возникла ошибка :(" );
//                location.reload();
            });

}

function add_to_ban_hours(ban, num, selector) {
    if ($('.wishes tr.'+selector+' .allday').hasClass('red')) {
        for (var h=0; h<7; h++) {
            ban.push(h+num)
        }
    }
}

function save_schedule(schedule) {
    console.log($(schedule).attr('data-schedule'));
    $('#spinner img').show();

    $.post(
        '/save_schedule',
        {
            'data': $(schedule).attr('data-schedule')
        },
        function() {
            $('#spinner img').hide();
            alert('Расписание сохранено');
//            location.reload();
        }
    ).fail(function() {
            $('#spinner img').hide();
            alert( "Возникла ошибка :(" );
//                location.reload();
        });
}

function show_for_teachers(schedule) {

}