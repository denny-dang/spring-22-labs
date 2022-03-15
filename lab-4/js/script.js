$(function(){

  $('#add-button').click(function () {
    let num1 = $("#add-num1").val()
    let num2 = $("#add-num2").val()

    $.ajax(
      { url:"http://localhost:8000/add",
        type: "GET",
        data: {"num1": num1, "num2": num2},
        dataType:"json"
      })
      .done(function (data){
        console.log(data.answer)
        $("#add-answer").val(data.answer);
      });
  });

  $('#sub-button').click(function () {
    let num1 = $("#sub-num1").val()
    let num2 = $("#sub-num2").val()

    $.ajax(
      { url:"http://localhost:8000/sub",
        type: "POST",
        data: {"num1": num1, "num2": num2},
        contentType: "application/x-www-form-urlencoded",
        dataType:"json"
      })
      .done(function (data) {
        console.log(data.answer)
        $("#sub-answer").val(data.answer);
      });
  });

  $('#mult-button').click(function () {
    let num1 = $("#mult-num1").val()
    let num2 = $("#mult-num2").val()

    $.ajax(
      { url:"http://localhost:8000/mult",
        type: "POST",
        data: JSON.stringify({"num1": num1, "num2": num2}),
        contentType: "application/json",
        dataType:"json"
      })
      .done(function (data) {
        console.log(data.answer)
        $("#mult-answer").val(data.answer);
      });
  });

});
