
$(document).ready(function(){

    $("html").keydown(function(e){
      pagnation_total_count = $( "#pagnation_total_count" ).val();
      switch(e.which) {
       case 37: // left
        new_page_number = 1;
        the_url = $(location).attr('href').split('?')[0];//with query strings
        page_number = the_url.substr(the_url.lastIndexOf('/') + 1);
        if(page_number > 1){
          new_page_number = new Number(page_number)-1;
        }
        new_url = the_url.replace(page_number,'');
        new_url = new_url+new_page_number;
        window.location.href = new_url;
        break;

        /*case 38: // up
        alert("up")
        break;*/

        case 39: // right
        new_page_number = 1;
        the_url = $(location).attr('href').split('?')[0];//with query strings
        page_number = the_url.substr(the_url.lastIndexOf('/') + 1);
        if(new Number(page_number) < new Number(pagnation_total_count)){ 
          new_page_number = new Number(page_number) + 1;
          new_url = the_url.replace('/'+page_number,'/');
          new_url = new_url+new_page_number;
          window.location.href = new_url;
        }else{
          new_page_number = page_number;
          alert("last page!!!");
          $("#pagnation_message").html("<b style='color:red;'>This is the last page!</b>");
        }
        break;

        /*case 40: // down
        alert("down")
        break;*/

        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
    });



});
