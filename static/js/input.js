function hidden_input(company){
    $(".hidden-input").on('keydown', function(e){
        if (company == true)
        {
        if (e.keyCode == 13)
        {
            jQuery(this).blur();
            return false;
        }
    }
    else return false;
    });
}