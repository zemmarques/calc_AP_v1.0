// função mudança do campo ano_letivo na form
$("#id_name").change(function () {

    var url = $("#feriadoForm").attr("data-feriados-url");      // get the url of the `load_feriados` view
    var ano_letivoId = $(this).val();                           // get the selected 'ano letivo' ID from the HTML input

    var grade = $("#id_grade").val()                            // get the 'grade' ID from the input field
    var url2 = $("#feriadoForm").attr("date-fim_ano-url");      // get the url of the `load_fim_ano` view

    var url3 = $("#feriadoForm").attr("date-inicio_ano-url");      // get the url of the `load_inicio_ano` view




    $.ajax({                                     // initialize an AJAX request
        url: url,                                       // set the url of the request (= localhost:8000/ajax/load-feriados/)
        data: {
            'ano_letivo': ano_letivoId                  // add the ano letivo id to the GET parameters
        },
        success: function (data) {                      // `data` is the return of the `load_feriados` view function
            $("#id_feriado_movel").html(data);          // replace the contents of the feriado input with the data that came from the server
        }
    });

    $.ajax({                                 // initialize an AJAX request
        url: url2,                                  // set the url of the request (= localhost:8000/ajax/load--fim-ano/)
        data: {
            'ano_letivo': ano_letivoId,             // add the ano letivo id to the GET parameters
            'grade': grade                          // add the grade id to the GET parameters
        },
        success: function (data) {                              // `data` is the return of the `load_fim_ano` view function
            $("#id_fim_ano").html(data).attr("value", data);    // replace the contents of the feriado input with the data that came from the server
        }
    });

    $.ajax({                                 // initialize an AJAX request
        url: url3,                                  // set the url of the request (= localhost:8000/ajax/load--fim-ano/)
        data: {
            'ano_letivo': ano_letivoId,             // add the ano letivo id to the GET parameters
        },
        success: function (data) {                                  // `data` is the return of the `load_inicio_ano` view function
            $("#id_inicio_ano").html(data).attr("value", data);     // replace the contents of the feriado input with the data that came from the server
        }
    });

});

// função mudança do campo grade (nível de ensino) na form
$("#id_grade").change(function () {
    var url = $("#feriadoForm").attr("date-fim_ano-url");           // get the url of the `load_fim_ano` view
    var grade = $(this).val();                                      // get the 'grade' ID from the input field
    var ano_letivoId = $("#id_name").val()                          // get the selected 'ano letivo' ID from the HTML input

    $.ajax({                                                 // initialize an AJAX request
        url: url,                                                   // set the url of the request (= localhost:8000/ajax/load-fim-ano/)
        data: {
            'ano_letivo': ano_letivoId,                             // add the ano letivo id to the GET parameters
            'grade': grade
        },
        success: function (data) {                                  // `data` is the return of the `load_feriados` view function
            $("#id_fim_ano").html(data).attr("value", data);        // replace the contents of the fim de ano input with the data that came from the server

        }
    });
});

// função mudança do campo disciplina (annual/semestral) na form
$("#id_disciplina").change(function (qualifiedName, value) {

    // mostra/esconde div com campos de data de início e fim de disciplina semestral
    if($("#id_disciplina_0").is(':checked')) {      // disciplina anual
        $("#disciplina_div").hide();
    }
    if($("#id_disciplina_1").is(':checked')) {      // disciplina semestral
        $("#disciplina_div").show();
    }

});

// função click em botão "calcular" do formulário
$("#calculaP").click(function (eventObj) {

    // Se disciplina=anual atribui uma data fictícia aos campos #id_fim_1s e #id_fim_1s
    // faz isto por estes campos serem obrigatórios. As datas são descartadas no backend.
    if($("#id_disciplina_0").is(':checked')) {
        $("#id_fim_1s").val("1974-1-31")
        $("#id_inicio_2s").val("1974-1-1");
    }
});

// função de inicialização de formulário
$( document ).ready(function() {
    // Faz isto porque se o formulário for submetido com erros, ao recarregar tem que mostrar
    // a div com os campos das datas das disciplinas semestrais
    if($("#id_disciplina_1").is(':checked')) {
        $("#disciplina_div").show();
    }
});