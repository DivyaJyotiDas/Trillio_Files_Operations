$(document).ready(function(){
  debugger;
  $("#part_id").empty()
  var ip_inp;
  var passwd_input;
  var loaded = false;
  $("#ip").keyup(function() {

   ip_inp = $('#ip').val().substring(0,8);

});

  $("#root_passwd_id").keyup(function() {

   passwd_input = $('#root_passwd_id').val().substring(0,8);


});

    $.ajax({
            url: 'api/partitions/list?hostname=10.1.2.216&password=@four123',
            type: 'get',
            dataType: 'json',
            success:function(response){
              let i = 0
              for (index = 0; index < response.length; index++) {
                console.log(response[index]);
                $("#part_id").append("<option value='"+index+"'>"+response[index]+"</option>");
              }


                console.log(response)
                if (loaded)
                  return;
                alert('Suscess')
                loaded = true;
            }
        });

});

$("backup_id").click(function(e) {
  alert('Hii')
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/pages/test/",
        data: {
            id: $(this).val(), // < note use of 'this' here
            access_token: $("#access_token").val()
        },
        success: function(result) {
            alert('ok');
        },
        error: function(result) {
            alert('error');
        }
    });
});