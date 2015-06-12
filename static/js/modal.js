function open_modal(which) {
    $('#overlay').fadeIn(300, // сначала плавно показываем темную подложку
    function () { // после выполнения предыдущей анимации
        $('#'+which)
            .css('display', 'block') // убираем у модального окна display: none;
            .animate({opacity: 1, top: '50%'}, 200); // плавно прибавляем прозрачность одновременно со съезжанием вниз
    });
}
function close_modal(data) {
    $('#'+$(data).parent().attr('id'))
        .animate({opacity: 0, top: '45%'}, 200,  // плавно меняем прозрачность на 0 и одновременно двигаем окно вверх
        function () { // после анимации
            $(this).css('display', 'none'); // делаем ему display: none;
            $('#overlay').fadeOut(300); // скрываем подложку
        }
    );
}