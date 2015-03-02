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

