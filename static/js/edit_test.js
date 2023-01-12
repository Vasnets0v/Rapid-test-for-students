function remove_question(id){

    if (confirm("Ви впевнені що хочете видалати запитання " + id) == true) {

        var deleteDiv = document.getElementById('question_' + id);
        // list of deleted questions
        var deletedQuestion = document.getElementById('delete_question').value;
        // real index in the database
        var IndexInDataBase = document.getElementById('database_table_id_' + id).value;

        deletedQuestion += IndexInDataBase + '_';
        document.getElementById('delete_question').value = deletedQuestion;
        deleteDiv.remove(); 
      }
}