var total_answers = [{value: 3}]
var total_question_form = 1;

function add_answer(id){

    var total_answers_HTMLel = document.getElementById("total_answers_" + id);
    total_answers_HTMLel.innerHTML = ''

    var add_answer_button = document.getElementById(id);

    if (total_answers[id - 1].value > 4) {
        total_answers[id - 1].value = total_answers[id - 1].value + 1;
        add_answer_button.innerHTML = '<div class="row align-items-center"><div class="col-sm-7"><input name="answer_' + id + '_' + total_answers[id - 1].value + '" type="text" class="form-control"></div><div class="col-sm-4"><input type="file" id="image_' + id + '_' + total_answers[id - 1].value + '" name="image_' + id + '_' + total_answers[id - 1].value + '" accept=".jpg, .jpeg, .png" class="form-control"></div><div class="col-sm-1"><input name="checkbox_' + id + '_' + total_answers[id - 1].value + '" type="checkbox" class="form-check-input mt-0"></div></div><input type="hidden" id="total_answers_' + id + '" name="total_answers_' + id + '" value="' + total_answers[id - 1].value + '">';
    }
    else {
        total_answers[id - 1].value = total_answers[id - 1].value + 1;
        add_answer_button.outerHTML = '<div class="row align-items-center"><div class="col-sm-7"><input name="answer_' + id + '_' + total_answers[id - 1].value + '" type="text" class="form-control"></div><div class="col-sm-4"><input type="file" id="image_' + id + '_' + total_answers[id - 1].value + '" name="image_' + id + '_' + total_answers[id - 1].value + '" accept=".jpg, .jpeg, .png" class="form-control"></div><div class="col-sm-1"><input name="checkbox_' + id + '_' + total_answers[id - 1].value + '" type="checkbox" class="form-check-input mt-0"></div></div><div class="button_centre" id="' + id + '"><input type="button" value="Додати вiдповiдь" onclick="add_answer(id=' + id + ');" class="btn btn-success"></div><input type="hidden" id="total_answers_' + id + '" name="total_answers_' + id + '" value="' + total_answers[id - 1].value + '">';
    }

}

function create_question_form(){

    total_question_form++;
    total_answers.push({value: 3});

    var button_new_question = document.getElementById('new_question');
    button_new_question.outerHTML = '<h5>Запитання №'+ total_question_form +'</h5><div class="row align-items-center"><div class="col-sm-7"><input name="question_'+ total_question_form +'" type="text" required class="form-control"></div><div class="col-sm-5"><input type="file" id="q_image_'+ total_question_form +'" name="q_image_'+ total_question_form +'" accept=".jpg, .jpeg, .png" class="form-control"></div></div><h5>Відповіді</h5><div class="row align-items-center"><div class="col-sm-7"><input name="answer_' + total_question_form + '_1" type="text" class="form-control"></div><div class="col-sm-4"><input type="file" id="image_' + total_question_form + '_1" name="image_'+ total_question_form +'_1" accept=".jpg, .jpeg, .png" class="form-control"></div><div class="col-sm-1"><input name="checkbox_' + total_question_form + '_1" type="checkbox" class="form-check-input mt-0"></div></div><div class="row align-items-center"><div class="col-sm-7"><input name="answer_' + total_question_form + '_2" type="text" class="form-control"></div><div class="col-sm-4"><input type="file" id="image_' + total_question_form + '_2" name="image_' + total_question_form + '_2" accept=".jpg, .jpeg, .png" class="form-control"></div><div class="col-sm-1"><input name="checkbox_' + total_question_form + '_2" type="checkbox" class="form-check-input mt-0"></div></div><div class="row align-items-center"><div class="col-sm-7"><input name="answer_' + total_question_form + '_3" type="text" class="form-control"></div><div class="col-sm-4"><input type="file" id="image_' + total_question_form + '_3" name="image_' + total_question_form + '_3" accept=".jpg, .jpeg, .png" class="form-control"></div><div class="col-sm-1"><input name="checkbox_' + total_question_form + '_3" type="checkbox" class="form-check-input mt-0"></div></div><div class="button_centre" id="' + total_question_form + '"><input type="button" value="Додати вiдповiдь" onclick="add_answer(id=' + total_question_form + ');" class="btn btn-success"></div><hr class="my-4"><input type="hidden" id="total_answers_' + total_question_form + '" name="total_answers_' + total_question_form + '" value="3"><div class="button_centre" id="new_question"><input type="button" value="Додати запитання" onclick="create_question_form();" class="btn btn-secondary"></div>';

    var input_total_question = document.getElementById('total_questions')
    input_total_question.outerHTML = '<input type="hidden" name="total_questions" id="total_questions" value="' + total_question_form + '">'
}