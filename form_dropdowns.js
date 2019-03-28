$(document).ready(function(){
  $(".a-add-prjct").click(function(){
    $(".a-add-prjct").hide();
    $(".prjct-form").show();
  });
});

$(document).ready(function(){
  $(".prjct-frm-btn").click(function(){
    $(".a-add-prjct").show();
    $(".prjct-form").hide();
  });
});



$(document).ready(function(){
  $(".a-add-task").click(function(){
    $(".a-add-task").hide();
    $(".task-form").show();
  });
});

$(document).ready(function(){
  $(".task-frm-btn").click(function(){
    $(".a-add-task").show();
    $(".task-form").hide();
  });
});