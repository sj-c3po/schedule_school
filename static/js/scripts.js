$(document).ready(function() {
    $("#steps").steps({
        headerTag: "h3",
        bodyTag: "section",
        transitionEffect: "slideLeft",
        stepsOrientation: "vertical"
    });
});
var parallels_alphabet = [];
    function getData() {
        var alphabet = 'абвгдежзиклмнопрстуфхцчшщыэюя';
        for (var i=5; i<12; i++) {
            var last_letter_parallel = document.forms['classes_form'].elements['letters_last'+i].value
            parallels_alphabet[i] = alphabet.split(last_letter_parallel)[0]+last_letter_parallel
        }
        var parallels = [5, 6, 7, 8, 9, 10, 11];
        draw_table_classes(parallels_alphabet)
    }
    function draw_table_classes(colls_rows) {
        var table='', colspan, class_ = [], max_str;
        console.log(colls_rows);
        max_str = colls_rows[5];
        for (var key = 5; key < 12; key++) {
            if (colls_rows[key] < colls_rows[key + 1]) {
                max_str = colls_rows[key + 1]
            }
            class_[key] = colls_rows[key].split('');
        }
        colspan = max_str.length;
        table += '<table><tr>';
        table += '<th>Название<br>параллели</th>';
        table += '<th colspan="' + colspan + '">Классы в<br>параллели</th>';
        table += '</tr><tr>';
        for (var k in class_) {
            var current_class = class_[k].reverse();
            var length = current_class.length;
            table += '<td>' + k + '</td>'
            for (var i = 0; i < colspan; i++) {
                if (current_class.length == 0) {
                    table += '<td></td>';
                } else {
                    table += '<td>' + current_class.pop() + '</td>';
    //                console.log("Отрезаем: " + current_class)
                }
            }
            table += '</tr>'
        }
        table += '</table>';
        $('#classes_table').html(table);
    }

function sendData() {
    $.post(
    "/new/classes/",
        {
            data: JSON.stringify(parallels_alphabet)
        }

    );



//    $.ajax({ // отправка данных
//        type: "POST", // метод
//        url: "/new/classes/", // URL приемника
//        data: parallels_alphabet, // строка запроса, переменные разделены знаком &
//        cache: false, // отключить кеширование
//        success: function(){ // в случае успеха вызываем функцию
//            alert('Отправили!')
//        },
//        error:  function(){
//            alert('Возникла ошибка!');
//        }
//    });
}


   /* Сделать так, чтобы при нажатии на "Добавить список учителей", сама кнопка убиралась, а появлялось поле с выбором
    количества учителей (либо модальное окно), а потом таблица и кнопка "Добавить еще"
 function change_visible() {
    if ($('.change_visible').css('display') == 'none') {
        $('.change_visible').css('display') = 'block'
    } else {
         $('.change_visible').css('display') = 'none'
    }
}*/


//function getTcount(){
//t_count = document.forms["t_count"].elements["t_count"].value;
//alert(t_count);
//}

//     <form id="t_count">
//            Количество учителей: <input text="text" name="t_count" />
//            <input type="button" value="Ок" onClick="getTcount();" />
//        </form>
