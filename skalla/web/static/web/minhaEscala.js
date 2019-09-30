Vue.filter('datahora', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY hh:mm')
  }
});

Vue.filter('data', function(value) {
  if (value) {
    return moment(String(value)).format('DD/MM/YYYY hh:mm')
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
  },
   created: function() {
    this.minhasEscalas();
    console.log("Criado");
  },
  methods: {
    minhasEscalas: function() {

        this.carregando = true;

        this.$http.get(`/api/escala-colaborador/?colaborador=${userId}`)
        .then( response =>  {
          this.total = response.body.count;
          this.escalas = response.body.results.map(x => {
            return x;
          });
          console.log(escalas);

        }).catch( erro => {
            console.log(erro);
        })
        .finally(() => {
            this.carregando = false;
        });


    },



    abreModalRequisicao: function(escala){
        this.mensagemSucesso = '';
        this.mensagemErro = '';

        alert(escala);
        if(Math.floor(Math.random() * 101) % 2 == 0 ){ // metodo pra gerar sucesso ou erro aleatoriamente
            this.mensagemErro = "Deu Erro";
        }else{
            this.mensagemSucesso = "Deu Certo";
        }
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
