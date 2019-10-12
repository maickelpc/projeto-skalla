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
      filtroStatus: 0,
      filtroId: null,
      filtroDataInicial: moment().format("YYYY-MM-DD"),
      filtroDataFinal: moment().add(1, 'M').format("YYYY-MM-DD"),
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
        let url = `/api/escala-colaborador/?colaborador=${userId}&page=${this.paginacao.page}&status=${this.filtroStatus}`;

        if(this.filtroId)
            url += `&id=${this.filtroId}`;

        if(this.filtroDataInicial)
            url += `&dataInicial=${this.filtroDataInicial}`;

        if(this.filtroDataFinal)
            url += `&dataFinal=${this.filtroDataFinal}`;

        this.$http.get(url)
        .then( response =>  {
          this.paginacao = this.gerarPaginacao( response.body.count, this.paginacao.page);
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
        //console.log(p);
        return p;
    },

     confirmaEscala: function(escala) {

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
  watch : {
       filtroId: function(val) {
          this.filtroDataInicial = null;
          this.filtroDataFinal = null;
          this.filtroId = val;
       },
       filtroDataInicial : function (val) {
          this.filtroId = null;
          this.filtroDataInicial = val;
       },
       filtroDataFinal : function (val) {
          this.filtroId = null;
          this.filtroDataFinal = val;
       }
  },
  mounted () {

  },
  delimiters: ["[[", "]]"]
});
