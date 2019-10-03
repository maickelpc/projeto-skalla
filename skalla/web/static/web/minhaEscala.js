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
      filtro: {},
      escalaConfirma: {}
  },
   created: function() {
    this.buscar();
    console.log("Criado");
  },
  methods: {

    buscar: function() {
        this.carregando = true;
        let agora = moment();
        this.$http.get(`/api/escala-colaborador/?colaborador=${userId}`)
        .then( response =>  {
          this.total = response.body.count;
          this.escalas = response.body.results.map(x => {
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


     confirmaEscala: function(escala) {

        console.log(escala);
        this.carregando = true;

        let headers = {
            'Content-Type': 'application/json',
            "X-CSRFToken": token
          };
        this.$http.post(`/api/escala-colaborador/confirma/`, escala, {headers})
        .then( response =>  {
            escala.status = 1;
            escala.dataConfirmacao = moment();


        }).catch( erro => {
            console.log(erro);
        })
        .finally(() => {
            this.carregando = false;
        });
    },


    enviaSolicitacao: function(escala){
        this.carregando = true;

        let headers = {
            'Content-Type': 'application/json',
            "X-CSRFToken": token
          };
        this.$http.post(`/api/escala-colaborador/registrasolicitacao/`, escala, {headers})
        .then( response =>  {
            escala.statusSolicitacao = 1;
            escala.dataSolicitacaoAlteracao = moment();
            escala.statusSolicitataoFormatado = 'Pendente';

        }).catch( erro => {

            console.log(erro);
        })
        .finally(() => {
            this.carregando = false;
        });

    },


    abreModal: function(escala){
        this.mensagemSucesso = '';
        this.mensagemErro = '';
//        alert("adasd");
        this.escalaConfirma = escala;
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
