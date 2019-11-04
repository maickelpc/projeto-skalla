var filtroColaboradorId = 0;
var filtroClienteId = 0;
var filtroPontoAlocacaoId = 0;


$(document).ready(function(){

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
    filtroColaboradorId = e.params.data.id;
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
    filtroClienteId = e.params.data.id;

    // Preeche as opções do select de pontos de alocação
        let $el = $("#id_pontoalocacao");
        $el.empty(); // remove old options
        $el.append($("<option></option>")
                 .attr("value", -1).text(" -- Selecione um item -- "));

        $.ajax({
          url:  `/api/ponto-alocacao/?cliente=${filtroClienteId}`,
          context: document.body
        }).then(function(dados) {
            console.log(dados.results);
            $.each(dados.results, function(key,value) {
              $el.append($("<option></option>")
                 .attr("value", value.id).text(value.nome));
            });
        });



  $( "#dataEntrada" ).datepicker();
  $( "#dataSaida" ).datepicker();

  $(".data").datepicker({
      dateFormat: 'dd/mm/yy',
      dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
      dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
      dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
      monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
      monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
      nextText: 'Próximo',
      prevText: 'Anterior'
  });

 });



// $("#id_pontoalocacao").select2({
//  ajax: {
//   url: "/admin/cliente/pontoalocacao/autocomplete  /",
//   type: "get",
//   dataType: 'json',
//   delay: 250,
//   data: function (params) { return { term: params.term };  },// search term
//   processResults: function (response) {
//     return { results: response.results };
//   },
//   cache: true
//  }
// });
//
// $('#id_pontoalocacao').on('select2:select', function (e) {
//    filtroPontoAlocacaoId = e.params.data.id;
// });


}); // Fim do $(document).ready(function(){



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
      vuetify: new Vuetify(),
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
      diaModal: moment(),
      horas:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
      total: 0,
      carregando: false,
      filtroId: null,
      filtroColaboradorId: null,
      filtroPontoAlocacaoId: null,
      filtroClienteId: null,
      filtroStatus: 0,
      filtroDataInicial: moment().format("YYYY-MM-DD"),
      filtroDataFinal: moment().add(7, 'd').format("YYYY-MM-DD"),
      paginacao: {page: 1},
      mostrarColaboradores: false,
      diaSemana: ['Domingo','Segunda-feira', 'Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado'],
      mesAno: ['','Janeiro','Fevereiro', 'Março','Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro','Dezembro']
  },
   created: function() {
    this.buscar();
  },
  // components: {
  // 	v-date-picker
  // },
  methods: {

    buscar: function(pagina = null) {

        if(pagina){
            this.paginacao.page = pagina;
        };
        this.carregando = true;
        let agora = moment();
        let url = `/api/escala/?`;

        if(this.filtroId)
            url += `id=${this.filtroId}&`;

        if(this.filtroDataInicial)
            url += `dataInicial=${this.filtroDataInicial}&`;

        if(this.filtroDataFinal)
            url += `dataFinal=${this.filtroDataFinal}&`;

        if(filtroColaboradorId > 0)
            url += `colaborador=${filtroColaboradorId}&`;

        if(filtroClienteId > 0)
            url += `cliente=${filtroClienteId}&`;

        if(this.filtroPontoAlocacaoId > 0)
            url += `pontoalocacao=${this.filtroPontoAlocacaoId}&`;

        if(this.filtroStatus >= 0)
            url += `status=${this.filtroStatus}&`;

        this.$http.get(url)
        .then( response =>  {
          this.paginacao = this.gerarPaginacao( response.body.count, this.paginacao.page);
          this.total = response.body.count;
          this.escalas = response.body.results.map(x => {
            x.dataInicio = moment(x.dataInicio);
            x.dataFim = moment(x.dataFim);
            x.horas = moment.duration(x.dataFim.diff(x.dataInicio)).asHours();
            x.executada = x.dataFim.diff(agora) < 0 && x.status == 0;
            x.executando = x.dataInicio.diff(agora) < 0 && !x.executada && x.status == 0;
            x.programada = !x.executada && !x.executando && x.status == 0;
            x.escalaColaborador = x.escalaColaborador.map(y => {
                y.dataInicio = moment(y.dataInicio);
                y.dataFim = moment(y.dataFim);
                return y;
                });
            return x;
          });

          this.dias = [];
          let inicio = moment(this.filtroDataInicial);
          let final = moment(this.filtroDataFinal);
          let dias = final.diff(inicio, 'days');

          for(let i = 0; i < dias; i++){
            this.dias.push( moment(this.filtroDataInicial).add(i,'days') );
          }

        }).catch( erro => {
            console.log(erro);
        }).finally(() => {
            this.carregando = false;
        });


    },

    toogleMostrarColaboradores: function(){
        this.mostrarColaboradores = !this.mostrarColaboradores;
    },

    abreModalCancelarEscala: function(escala){
        this.mostrarColaboradores = false;
        this.mensagemSucesso = '';
        this.mensagemErro = '';
        this.escalaModal = escala;

    },

    abreModalAdicionarColaborador: function(escala, dia){
        this.escalaColaboradorModalAdicionar = {colaborador: {}};
        this.escalaColaboradorModalAdicionar.horaInicio = escala.turnoPonto.turno.horaInicio;
        this.escalaColaboradorModalAdicionar.horaFim = escala.turnoPonto.turno.horaFim;
        this.escalaColaboradorModalAdicionar.dia = dia;
        this.escalaColaboradorModalAdicionar.adicionado = false;
        this.escalasColaborador = {};
        this.escalaModal = escala;
        this.diaModal = dia;
        this.colaboradorModal = {};
        this.carregando = true;
        this.mensagemErro = '';
        this.mensagemSucesso = '';
        console.log(escala);
        this.$http.get(`/api/colaborador/?data=${this.diaModal.format('YYYY-MM-DD')}`)
        .then( response => {
            console.log(response);
            this.colaboradores = response.body.results;
        }).catch(erro => {
            console.log(this.erro);
            this.mensagemErro = 'Erro ao Buscar os colaboradores.';
        }).finally(() => {this.carregando = false; })

    },

    cancelarEscala: function(escala){
        this.mensagemSucesso = '';
        this.mensagemErro = '';
        this.escalaModal = escala;
        this.carregando = true;
        this.$http.get(`/api/escala/${escala.id}/cancelarescala/`)
        .then(dados => {
            console.log(dados);
            let escalaRetorno = dados.body;
            this.escalaModal.status = escalaRetorno.status;
            this.escalaModal.dataCancelamento = moment(escalaRetorno.dataCancelamento);
            this.escalaModal.executada = false;
            this.escalaModal.executando = false;
            this.escalaModal.programada = false;

            this.mensagemSucesso = `Escala ${this.escalaModal.id} foi cancelada com sucesso!`;


        }).catch(erros => {
            console.log(erros);
            this.mensagemErro = erros.bodyText;

        })
        .finally(()=>{
            this.carregando = false;
        });
    },

    removerColaborador: function(escalaColaborador){
        this.mensagemSucesso = '';
        this.mensagemErro = '';
        this.colaboradorModal = escalaColaborador;
        this.carregando = true;
        this.$http.get(`/api/escala-colaborador/${escalaColaborador.id}/cancelar/`)
        .then(dados => {
            console.log(dados);
            let retorno = dados.body;
            this.colaboradorModal.status = 3;
            this.colaboradorModal.dataCancelamento = moment(retorno.dataCancelamento)

            this.mensagemSucesso = `Escala ${this.escalaModal.id} foi cancelada com sucesso!`;


        }).catch(erros => {
            console.log(erros);
            this.mensagemErro = erros.bodyText;

        })
        .finally(()=>{
            this.carregando = false;
        });
    },

    abreModalRemoveColaborador: function(escala, colaborador){
        this.mensagemSucesso = '';
        this.mensagemErro = '';
        this.mostrarColaboradores = false;

        this.colaboradorModal = colaborador;
        if(this.colaboradorModal.dataSolicitacaoAlteracao){
            this.colaboradorModal.dataSolicitacaoAlteracao = moment(this.colaboradorModal.dataSolicitacaoAlteracao);
        }
        if(this.colaboradorModal.dataRetornoSolicitacaoAlteracao){
            this.colaboradorModal.dataRetornoSolicitacaoAlteracao = moment(this.colaboradorModal.dataRetornoSolicitacaoAlteracao);
        }
        this.escalaModal = escala;


    },


    acidionarColaborador: function(escalaColaborador){

      let obj = {
        escalaId: this.escalaModal.id,
        colaboradorId: escalaColaborador.colaborador.id,
        dia: escalaColaborador.dia.format("YYYY-MM-DD"),
        horaInicio: escalaColaborador.colaborador.horaInicio,
        horaFim: escalaColaborador.colaborador.horaFim
      };

      console.log(obj);


      this.carregando = true;
      let headers = {
          'Content-Type': 'application/json',
          "X-CSRFToken": token
        };

      this.$http.post(`/api/escala/${obj.escalaId}/adicionarcolaborador/`, obj, {headers})
      .then(dados => {
          console.log(dados);

          let retorno = dados.body;
          this.escalaColaboradorModalAdicionar.adicionado = true;
          this.mensagemSucesso = `Colaborador ${this.escalaColaboradorModalAdicionar.colaborador.first_name} foi adicionado à escala com sucesso!`;


      }).catch(erros => {
          console.log(erros);
          this.mensagemErro = erros.bodyText;

      })
      .finally(()=>{
          this.carregando = false;
      });


    },

    carregaUltimasEscalas: function(colaborador, dia){

        this.carregando = true;
        this.mensagemErro = '';
        this.escalasColaborador = null;
        this.$http.get(`/api/escala-colaborador/ultimas/?colaborador=${colaborador.id}&data=${dia.format('YYYY-MM-DD')}`)
        .then(response => {
            console.log(response.body);
            let dados = response.body;

            this.escalasColaborador = dados.map(x => {
                x.dataInicio = moment(x.dataInicio);
                x.dataFim = moment(x.dataFim);
                x.horasCorridas = Math.round(moment.duration(x.dataFim.diff(x.dataInicio)).asHours());

                return x;
            });

        }).catch(erro => {
            console.log(erro);
            this.mensagemErro = 'Erro ao buscar as ultimas escalas do colaborador';
        }).finally(() => this.carregando = false);


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


    escalasDia: function(dia){
        return this.escalas.filter( x => x.escalaColaborador.filter(y => y.dataInicio.format('YYYYMMDD') === dia.format('YYYYMMDD')).length > 0 );
    },

    colaboradoresDia: function(escala, dia){
        return escala.escalaColaborador.filter(y => y.dataInicio.format('YYYYMMDD') === dia.format('YYYYMMDD'));
    },

    limpaErros: function(){
        this.mensagemErro = '';
    },

    limpaSucesso: function(){
        this.mensagemSucesso = '';
    }

  },
  mounted () {

  },

  delimiters: ["[[", "]]"]
});
