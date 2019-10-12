var filtroColaboradorId = 0;

$(document).ready(function(){

 $("#id_colaborador").select2({
  ajax: {
   url: "/admin/empresa/colaborador/autocomplete/",
   type: "get",
   dataType: 'json',
   delay: 250,
   data: function (params) {
    return {
      term: params.term // search term
    };
   },
   processResults: function (response) {
     return {
        results: response.results
     };
   },
   cache: true
  }
 });



 $('#id_colaborador').on('select2:select', function (e) {
 console.log(e);
  filtroColaboradorId = e.params.data.id;
});


});



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
  el: '#minhaescala',
  data: {
      mensagemErro:'',
      mensagemSucesso: '',
      escalas: [],
      total: 0,
      carregando: false,
      aceitarSolicitacao: false,
      retornoSolicitacao:'',
      filtroId: null,
      filtroColaboradorId: null,
      filtroStatus: 1,
      filtroDataInicial: moment().add(-7, 'd').format("YYYY-MM-DD"),
      filtroDataFinal: moment().format("YYYY-MM-DD"),
      escalaConfirma: {},
      paginacao: {page: 1},
  },
   created: function() {
    this.buscar();
//    console.log("Criado");
  },
  methods: {

    buscar: function(pagina = null) {

        if(pagina){
            this.paginacao.page = pagina;
        };
        this.carregando = true;
        let agora = moment();
        let url = `/api/escala-colaborador/solicitacoes/?`;

        if(this.filtroId)
            url += `id=${this.filtroId}&`;

        if(this.filtroDataInicial)
            url += `dataInicial=${this.filtroDataInicial}&`;

        if(this.filtroDataFinal)
            url += `dataFinal=${this.filtroDataFinal}&`;

        if(filtroColaboradorId > 0)
            url += `colaborador=${filtroColaboradorId}&`;
        if(this.filtroStatus > 0)
            url += `statusSolicitacao=${this.filtroStatus}&`;

        this.$http.get(url)
        .then( response =>  {
          //this.paginacao = this.gerarPaginacao( response.body.count, this.paginacao.page);
          //this.total = response.body.count;
          this.escalas = response.body.map(x => {
            x.dataInicio = moment(x.dataInicio);
            x.dataFim = moment(x.dataFim);
            x.horas = moment.duration(x.dataFim.diff(x.dataInicio)).asHours();
            x.executada = x.dataInicio.diff(agora) < 0;
            x.statusSolicitataoFormatado = (x.statusSolicitacao === 1) ? 'Pendente' : ((x.statusSolicitacao === 2) ? 'Aceito' : 'Recusado' )
            return x;
          });

        }).catch( erro => {
            console.log(erro);
        })
        .finally(() => {
            this.carregando = false;
        });
    },


    abreModalAceitar: function(escala){
        this.retornoSolicitacao = '';
        this.mensagemSucesso = '';
        this.mensagemErro = '';
//        alert("adasd");
        this.escalaConfirma = escala;
        this.aceitarSolicitacao = true;
    },

    abreModalRejeitar: function(escala){
        this.retornoSolicitacao = '';
        this.mensagemSucesso = '';
        this.mensagemErro = '';
//        alert("adasd");
        this.escalaConfirma = escala;
        this.aceitarSolicitacao = false;
    },

    enviarRetornoSolicitacao: function() {
        this.carregando = true;

        this.escalaConfirma.statusSolicitacao = this.aceitarSolicitacao ? 2 : 3;
        let aceita = this.aceitarSolicitacao ? "Aceita" : "Recusada";
        this.escalaConfirma.retornoSolicitacao = this.retornoSolicitacao;
        this.escalaConfirma.dataRetornoSolicitacaoAlteracao = moment().format();

        let headers = {
            'Content-Type': 'application/json',
            "X-CSRFToken": token
          };

        this.$http.post(`/api/escala-colaborador/retornosolicitacao/`, this.escalaConfirma, {headers})
        .then( response =>  {
          this.mensagemSucesso = `Solicitação ${this.escalaConfirma.id} ${aceita} com sucesso`;

        }).catch( erro => {
            this.mensagemErro = `Erro ao registrar retorno da solicitação ${this.escalaConfirma.id}`;
            this.escalaConfirma.statusSolicitacao = 1;

            delete this.escalaConfirma.retornoSolicitacao;
            delete this.escalaConfirma.dataRetornoSolicitacaoAlteracao;
            console.log(erro);
        })
        .finally(() => {
            this.carregando = false;
        });
    },

    limpaErros: function(){
        this.mensagemErro = '';
    },

    limpaSucesso: function(){
        this.mensagemSucesso = '';
    }

  },
//  watch : {
//       filtroId: function(val) {
//          this.filtroDataInicial = null;
//          this.filtroDataFinal = null;
//          this.filtroId = val;
//       },
//       filtroDataInicial : function (val) {
//          this.filtroId = null;
//          this.filtroDataInicial = val;
//       },
//       filtroDataFinal : function (val) {
//          this.filtroId = null;
//          this.filtroDataFinal = val;
//       }
//  },
  mounted () {

  },
  delimiters: ["[[", "]]"]
});
