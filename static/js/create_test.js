var total_answers = [{value: 3}]
var total_question_form = 1;

function add_answer(id){

    var total_answers_HTMLel = document.getElementById("total_answers_" + id)
    total_answers_HTMLel.outerHTML = ''

    var add_answer_button = document.getElementById(id);

    if (total_answers[id - 1].value > 4) {
        total_answers[id - 1].value = total_answers[id - 1].value + 1;
        add_answer_button.outerHTML = '<p><input name="answer_' + id + '_' + total_answers[id - 1].value + '" type="text"><input type="checkbox"></p><input id="total_answers_' + id + '" name="total_answers_' + id + '" type="hidden" value="' + total_answers[id - 1].value + '">';
    }
    else {
        total_answers[id - 1].value = total_answers[id - 1].value + 1;
        add_answer_button.outerHTML = '<p><input name="answer_' + id + '_' + total_answers[id - 1].value + '" type="text"><input type="checkbox"></p><p><input id="' + id + '" type="button" value="Додати вiдповiдь" onclick="add_answer(id=' + id + ');"></p><input id="total_answers_' + id + '" name="total_answers_' + id + '" type="hidden" value="' + total_answers[id - 1].value + '">';
    }

}

function create_question_form(){

    total_question_form++;
    total_answers.push({value: 3});

    var button_new_question = document.getElementById('new_question');
    button_new_question.outerHTML = '<p>Запитання ' + total_question_form + '</p><input name="question_' + total_question_form + '" type="text"><p>Вiдповiдь</p><p><input name="answer_' + total_question_form + '_1" type="text"><input type="checkbox"></p><p><input name="answer_' + total_question_form + '_2" type="text"><input type="checkbox"></p><p><input name="answer_' + total_question_form + '_3" type="text"><input type="checkbox"></p><input id="total_answers_' + total_question_form + '" name="total_answers_' + total_question_form + '" type="hidden" value="3"><input id="' + total_question_form + '" type="button" value="Додати вiдповiдь" onclick="add_answer(id=' + total_question_form + ');"><p><input value="Додати запитання" onclick="create_question_form();" id="new_question" type="button"></p>';

    var input_total_question = document.getElementById('total_questions')
    input_total_question.outerHTML = '<input type="hidden" name="total_questions" id="total_questions" value="' + total_question_form + '">'
}