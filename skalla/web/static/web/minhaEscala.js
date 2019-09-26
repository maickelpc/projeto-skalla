var app = new Vue({
  el: '#minhaescala',
  data: {
      message: 'Hello Vue!',
      escalas: [],
      total: 0,
      loading: false,
  },
   created: function() {
    this.greetings();
    console.log("Criado");
  },
  methods: {
    greetings: function() {
      console.log('Howdy my good fellow!');
    },


    buscar: function(){

    this.loading = true;

    this.$http.get("/api/escalas/")
        .then( response =>  {
          this.total = response.body.count;
          this.escalas = response.body.results;

        }).catch( erro => {
            console.log(erro);
        })
        .finally(() => {
            this.loading = false;
        });


    }


  },
  mounted () {

  },
  delimiters: ["[[", "]]"]
});



