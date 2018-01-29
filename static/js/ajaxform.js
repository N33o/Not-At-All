$(".ajax-send").on('blur', function(){
    let id = this.id;
    $.ajax({
        type:'POST',
        url:'ajax/company/'+id,
        error: function(){
            console.log(".error-banner[for="+id+"]")
            $(".error-banner[for="+id+"]").show();
        },
        success:function(){
            $(".error-banner[for="+id+"]").hide();
        }
    });
});
