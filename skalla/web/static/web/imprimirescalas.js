
Vue.filter('datahora', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

Vue.filter('data', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY HH:mm')
  }
});

Vue.config.lang = 'pt-br';

var app = new Vue({
  el: '#buscaescala',
  data: {
      // vuetify: new Vuetify(),
      picker: new Date().toISOString().substr(0, 10),

      mensagemErro:'',
      mensagemSucesso: '',
      escalas: [],
      colaboradores: [],
      escalaModal: {},
      colaboradorModal: {},
      escalaColaboradorModalAdicionar: {},
      escalasColaborador: null,
      escalaColaboradorModal: null,
      dias:[],
      tipoImpressao: '',
      mostrarCanceladas: false,
      diaModal: moment(),
      horas:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
      carregando: false,
      filtroColaboradorId: null,
      filtroPontoAlocacaoId: null,
      filtroClienteId: null,
      filtroEmpresaId: null,
      filtroStatus: 0,
      filtroDataInicial: moment().format("YYYY-MM-DD"),
      filtroDataFinal: moment().add(7, 'd').format("YYYY-MM-DD"),
      paginacao: {page: 1},
      total: 0,
      diaSemana: ['Domingo','Segunda-feira', 'Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado'],
      mesAno: ['','Janeiro','Fevereiro', 'Março','Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro','Dezembro']
  },
   created: function() {
    // this.buscar();
  },
  // components: {
  // 	v-date-picker
  // },
  methods: {

    imprimir: function(){
      let url = `/imprimirescala/?dataInicial=${this.filtroDataInicial}&dataFinal=${this.filtroDataFinal}`;

      switch (this.tipoImpressao) {
        case 'empresa':
          url += `&empresa=${this.filtroEmpresaId}`;

        break;
        case 'colaborador':
          url += `&colaborador=${this.filtroColaboradorId}`;

        break;
        case 'cliente':
          url += `&cliente=${this.filtroClienteId}`;

        break;
        case 'ponto':
          url += `&pontoalocacao=${this.filtroPontoAlocacaoId}`
        break;
      }
      url += `&tipo=${this.tipoImpressao}`;

      let win = window.open(url, '_blank');
      win.focus();
      this.mensagemSucesso = "Escala gerada na aba ao lado!"

      setTimeout(function(){ location.reload(); }, 500);
    },

    formInvalid(){
      if(this.filtroDataFinal < this.filtroDataInicial){
        return true;
      }

      if(!this.tipoImpressao){
        return true;
      }else{

        switch (this.tipoImpressao) {
          case 'empresa':
            console.log(this.filtroEmpresaId);
            if(this.filtroEmpresaId <= 0){
              console.log("Empresa")
              return true;
            }

          break;
          case 'colaborador':
            if(this.filtroColaboradorId <= 0){
              console.log("Empresa")
              return true;
            }

          break;
          case 'cliente':
            if(this.filtroClienteId  <= 0){
              console.log("Cliente");
              return true;
            }

          break;
          case 'ponto':
            if(this.filtroPontoAlocacaoId <= 0){
              console.log("Ponto")
              return true;
            }

          break;
        }
      }
      console.log("False");
      return false;
    },

    gerarPaginacao: function(total, pagina){
        let p = {
            page: pagina,
            totalItens: total,
            totalPaginas: Math.ceil(total / 20),
            paginas: []
        };
        for(let i = 1; i <= p.totalPaginas; i++){
            p.paginas.push(i);
        }
        return p;
    },


    limpaErros: function(){
        this.mensagemErro = '';
    },

    limpaSucesso: function(){
        this.mensagemSucesso = '';
    },


  },
  mounted () {

  },

  delimiters: ["[[", "]]"]
});








$(document).ready(function(){

  $("#id_empresa").select2({
   ajax: {
    url: "/admin/empresa/empresa/autocomplete/",
    type: "get",
    dataType: 'json',
    delay: 250,
    data: function (params) {
     return { term: params.term }; // search term
    },
    processResults: function (response) {
      return { results: response.results };
    },
    cache: true
   }
  });

  $('#id_empresa').on('select2:select', function (e) {
     app.filtroEmpresaId = e.params.data.id;

  });

 $("#id_colaborador").select2({
  ajax: {
   url: "/admin/empresa/colaborador/autocomplete/",
   type: "get",
   dataType: 'json',
   delay: 250,
   data: function (params) {
    return { term: params.term }; // search term
   },
   processResults: function (response) {
     return { results: response.results };
   },
   cache: true
  }
 });

 $('#id_colaborador').on('select2:select', function (e) {
    app.filtroColaboradorId = e.params.data.id;
 });



 $("#id_cliente").select2({
  ajax: {
   url: "/admin/cliente/cliente/autocomplete/",
   type: "get",
   dataType: 'json',
   delay: 250,
   data: function (params) {
    return { term: params.term };// search term
   },
   processResults: function (response) {
     return { results: response.results };
   },
   cache: true
  }
 });

 $('#id_cliente').on('select2:select', function (e) {
    app.filtroClienteId = e.params.data.id;

    // Preeche as opções do select de pontos de alocação
        let $el = $("#id_pontoalocacao");
        $el.empty(); // remove old options
        $el.append($("<option></option>")
                 .attr("value", -1).text(" -- Selecione um item -- "));

        $.ajax({
          url:  `/api/ponto-alocacao/?cliente=${e.params.data.id}`,
          context: document.body
        }).then(function(dados) {
            console.log(dados.results);
            $.each(dados.results, function(key,value) {
              $el.append($("<option></option>")
                 .attr("value", value.id).text(value.nome));
            });
        });



  // $( "#dataEntrada" ).datepicker();
  // $( "#dataSaida" ).datepicker();

  // $(".data").datepicker({
  //     dateFormat: 'dd/mm/yy',
  //     dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
  //     dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
  //     dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
  //     monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
  //     monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
  //     nextText: 'Próximo',
  //     prevText: 'Anterior'
  // });

 });



}); // Fim do $(document).ready(function(){
