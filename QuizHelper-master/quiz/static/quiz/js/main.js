if (($(window).height() + 100) < $(document).height()) {
    $('#top-link-block').removeClass('hidden').affix({
        // how far to scroll down before link "slides" into view
        offset: {top: 100}
    });
}

var show_answer = true;
var exam_mode = false;
var flash_card_mode = false;
/**
 * change result panel color
 * @param correct_answer
 * @param user_choice
 * @param result_panel
 */
function change_result_panel_color(correct_answer, user_choice, result_panel) {
    if (correct_answer === user_choice) {
        result_panel.find('span').css('background-color', '#5cb85c');
        result_panel.find('span').css('color', '#fff');
        result_panel.find('span').css('border-color', '#4cae4c');
    }
    else {
        result_panel.find('span').css('background-color', '#d9534f');
        result_panel.find('span').css('color', '#fff');
        result_panel.find('span').css('border-color', '#d43f3a');
    }
}

$(document).ready(function () {

    /**
     * Show or hide answers.
     */
    $("#toggle-show-answer").click(function () {
        $('.quiz-answer').toggle(
            function () {
                if (!show_answer) {
                    $("#toggle-show-answer").text('Show all answers');
                }
                else {
                    console.log("in here");
                    $("#toggle-show-answer").text('Hide all answers');
                }
            });
        show_answer = !show_answer;
    });

    /**
     * Toggle exam mode.
     */
    $("#toggle-exam-mode").click(function () {
        exam_mode = !exam_mode;
        if (exam_mode) {
            $("#toggle-exam-mode").text('Learning mode');
            $(".answer-panel").hide();
        }
        else {
            $("#toggle-exam-mode").text('Exam mode');
            $(".answer-panel").show();
            $(".result-panel").hide();
        }

    });

    /**
     * Check if the user picks the correct answer
     */
    $(".choice-row").click(function () {
        // Clickable when it's in exam mode.
        if (exam_mode) {
            var containing_div = $(this).closest('div');
            var correct_answer = containing_div.find('ul.answer-panel li').text();
            var result_panel = containing_div.find('ul.result-panel');
            var user_choice = $(this).text();
            var user_choice_row = result_panel.find('li.user-answer');
            user_choice_row.text("You chose " + user_choice + ".");
            change_result_panel_color(correct_answer, user_choice, result_panel);

            result_panel.show();

        }
    });

    $('#toggle-flash-card-mode').click(function () {
        flash_card_mode = !flash_card_mode;
        console.log("inside flash");
        if (flash_card_mode) {
            $('.essay-question').hide();
            $('.flash-card-panel').show();
            $("#toggle-flash-card-mode").text('Turn off flash card mode');
        }
        else {
            $("#toggle-flash-card-mode").text('Turn on flash card mode');
            $('.essay-question').show();
            $('.flash-card-panel').hide();
        }
    });

    //Using rotate3Di api from https://github.com/zachstronaut/rotate3Di
    $('.flash-card-panel').click(function () {
        if (flash_card_mode) {
            $(this).rotate3Di(
                'toggle',
                'fast',
                {
                    sideChange: mySideChange,
                    complete: flipped
                }
            );
        }
    });


    /**
     * comment post form generation
     */
    $('#comments').on('click', '.reply', function (event) {
        event.preventDefault();
        var form = $('#comment-form').clone(true);

        form.find('.parent').val($(this).parent().parent().attr('id'));
        form.parent().remove('h2');
        $(this).parent().append(form);
    });
});

function mySideChange(front) {

}

/**
 * Change the flash card panel when flipped.
 */
function flipped() {
    var question_block = $(this).next('div.essay-question');
    question_body = question_block.find('ul li.question-body').text();
    quiz_answer = question_block.find('ul li.quiz-answer').text();
    var header = $(this).find('span').text();
    // show orginal question
    if (header === 'Correct Answer') {
        $(this).find('span').text('Question');
        $(this).find('li').text(question_body);
    }
    // show answer
    else {
        $(this).find('span').text('Correct Answer');
        $(this).find('li').text(quiz_answer);
    }

}

