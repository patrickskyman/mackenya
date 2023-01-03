function prepareDocument(){
     //code to prepare page here.
     jQuery("form#search").submit(function(){
          text = jQuery("#q").val();
            if (text == "" || text == "Search"){
// if empty, pop up alert 
            alert("Enter a search term."); 
            // halt submission of form 
            return false;
} });
} 

jQuery(document).ready(prepareDocument);



$(document).ready(function(){ 
    //code to prepare page here.
    $("form#search").submit(function(){
        text = $("").val();
          if (text == "" || text == "Search"){
// if empty, pop up alert 
          alert("Enter a search term."); 
          // halt submission of form 
          return false;
} });  
});
