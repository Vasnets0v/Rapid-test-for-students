function confirm_delete_topic(topic, id){
    if (confirm("Ви впевнені що хочете видалати тему " + topic) == true) {
        document.getElementById('delete_button_' + id).click();
    }
}