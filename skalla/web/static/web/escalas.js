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

var app = new Vue({
  el: '#buscaescala',
  data: {
      mensagemErro:'',
      mensagemSucesso: '',
      escalas: [],
      total: 0,
      carregando: false,
      filtroId: null,
      filtroColaboradorId: null,
      filtroPontoAlocacaoId: null,
      filtroClienteId: null,
      filtroStatus: -1,
      filtroDataInicial: moment().format("YYYY-MM-DD"),
      filtroDataFinal: moment().add(7, 'd').format("YYYY-MM-DD"),
      paginacao: {page: 1},
  },
   created: function() {
    this.buscar();
  },
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
            x.executada = x.dataInicio.diff(agora) < 0;
            return x;
          });
        }).catch( erro => {
            console.log(erro);
        }).finally(() => {
            this.carregando = false;
        });
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

//    enviarRetornoSolicitacao: function() {
//        this.carregando = true;
//
//        this.escalaConfirma.statusSolicitacao = this.aceitarSolicitacao ? 2 : 3;
//        let aceita = this.aceitarSolicitacao ? "Aceita" : "Recusada";
//        this.escalaConfirma.retornoSolicitacao = this.retornoSolicitacao;
//        this.escalaConfirma.dataRetornoSolicitacaoAlteracao = moment().format();
//
//        let headers = {
//            'Content-Type': 'application/json',
//            "X-CSRFToken": token
//          };
//
//        this.$http.post(`/api/escala-colaborador/retornosolicitacao/`, this.escalaConfirma, {headers})
//        .then( response =>  {
//          this.mensagemSucesso = `Solicitação ${this.escalaConfirma.id} ${aceita} com sucesso`;
//
//        }).catch( erro => {
//            this.mensagemErro = `Erro ao registrar retorno da solicitação ${this.escalaConfirma.id}`;
//            this.escalaConfirma.statusSolicitacao = 1;
//
//            delete this.escalaConfirma.retornoSolicitacao;
//            delete this.escalaConfirma.dataRetornoSolicitacaoAlteracao;
//            console.log(erro);
//        })
//        .finally(() => {
//            this.carregando = false;
//        });
//    },

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
