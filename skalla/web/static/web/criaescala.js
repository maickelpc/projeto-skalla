$(document).ready(function(){
    $('.adicionaColaborador').click(function(){
        $("#modalColaboradores").modal("hide")
    });
});

var app = new Vue({
    el : '#content-main',
    data: {
        picker: new Date().toISOString().substr(0, 10),

        mensagemErro:'',
        mensagemSucesso: '',
        dataInicio: null,
        colaboradoresDisponiveis: [],
        colaboradoresEscalados: [],
        loading: false,
        colaborador: {},
        message: null,
        perfis: [],
        perfil: {},
        pontos: [],
        ponto: {},
        clientes: [],
        cliente: {},
        turnos: [],
        turno: {},
        carregando: false,
        escalaColaborador: {
            dataInicio: null,
            dataFim: null,
            colaborador: {}
        },
        escalaColaboradorList: [],
        escala : {
            "dataInicio": null,
            "dataFim": null,
            "dataDuplicacao": null,
            "dataCancelamento": null,
            "status": null,
            "escalaColaboradorList": [],
            "perfil": {
                "descricao": "",
                "tipo": "",
                "dias": null,
                "duplicar": false,
                "horasAntecedenciaDuplicacao": null
            },
            "turnoPonto": {
                "turno": {
                    "descricao": "",
                    "periodo": "",
                    "horasTrabalhadas": null,
                    "horasDescanso": null,
                    "horaInicio": null,
                    "horaFim": null,
                    "ativo": false
                },
                "pontoAlocacao": {
                    "cliente": {
                        "nomeFantasia": ""
                    },
                    "nome": "",
                    "descricao": "",
                    "endereco": null
                },
                "qtdeColaboradores": null
            }
        }
    },
    delimiters: ["[[", "]]"],
    mounted: function () {
        this.getColaboradores();
        this.getPerfisJornada();
        this.getClientes();
    },
    watch: {
        cliente: function(val) {
            this.getPontosAlocacao(val.id);
            this.escala.turnoPonto.pontoAlocacao.cliente = val;
        },
        ponto: function(val) {
            this.getTurnosPonto(val.id);
            this.escala.turnoPonto.pontoAlocacao = val;
        },
        turno: function(val) {
            this.escala.turnoPonto.turno = val;
        },
        perfil: function(val) {
            this.escala.perfil = val;
            if (this.escala.dataInicio) {
                moment.locale('pt-BR');
                this.escala.dataFim = moment(this.escala.dataInicio);
                this.escala.dataFim.add((this.escala.perfil.dias - 1), 'd');
                console.log(this.escala);
            }
        },
        dataInicio: function(val) {
            moment.locale('pt-BR');
            this.escala.dataInicio = moment(val, 'YYYY-MM-DD');
            this.escala.dataFim = moment(val, 'YYYY-MM-DD');
            this.escala.dataFim.add((this.escala.perfil.dias - 1), 'd');
            //console.log(this.escala);
        }
    },
    filters: {
      moment: function (date, d) {
          moment.locale('pt-BR');
          //console.log(date);
          return moment(date).add(d, 'days').format('dddd, DD/MM/YYYY');
      },
      horas: function (date, d) {
          moment.locale('pt-BR');
          horas = date.split(':');
          return moment({hour: horas[0], minute: horas[1]}).add(d, 'h').format('HH:mm')
                    + ' - '
                    + moment({hour: horas[0], minute: horas[1]}).add(d + 1, 'h').format('HH:mm');
      }
    },
    methods: {
        adicionaColaboradorEscala(colaborador) {
            this.escalaColaborador.colaborador = colaborador;
            this.escalaColaboradorList.push(this.escalaColaborador);
            this.escalaColaborador = {
                dataInicio: null,
                dataFim: null,
                colaborador: {}
            };

            console.log(this.escalaColaboradorList);
        },
        abreModalColaboradores(dataInicial, dia, horaInicio, horaFim) {
            let dataEscala = moment(dataInicial).add(dia - 1, 'days').format('DD/MM/YYYY');
            this.escalaColaborador.dataInicio = moment(dataEscala + " " + horaInicio);
            this.escalaColaborador.dataFim = moment(dataEscala + " " + horaFim);
            //this.escalaColaboradorList.push(escalaColaborador);
            //console.log(this.escalaColaborador);
        },
        getIntervaloHoras: function(horaInicio, horaFim) {
            let inicio = moment(horaInicio, "HH:mm");
            let fim = moment(horaFim, "HH:mm");

            return fim.diff(inicio, 'hours');
        },
        getColaboradores: function() {
          this.loading = true;
          this.$http.get('/api/colaborador/')
              .then((response) => {
                this.colaboradoresDisponiveis = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        getPerfisJornada: function() {
          this.loading = true;
          this.$http.get('/api/perfil-jornada/')
              .then((response) => {
                this.perfis = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        getPerfilJornada: function(id) {
          this.loading = true;
          this.$http.get('/api/perfil-jornada/'+id+'/')
              .then((response) => {
                this.perfil = response.data;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
         getPontosAlocacao: function(cliente) {
          this.loading = true;
          this.$http.get('/api/ponto-alocacao?cliente='+cliente)
              .then((response) => {
                this.pontos = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        getTurnosPonto: function(val) {
          this.loading = true;
          this.$http.get('/api/turno-ponto?pontoAlocacao='+val)
              .then((response) => {
                this.turnos = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        getClientes: function() {
          this.loading = true;
          this.$http.get('/api/cliente/')
              .then((response) => {
                this.clientes = response.data.results;
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        salvaEscala() {

            let headers = {
                'Content-Type': 'application/json',
                "X-CSRFToken": token
              };
            this.escala.escalaColaboradorList = this.escalaColaboradorList;
            this.$http.post(`/api/escala/`, this.escala, {headers})
            .then( response =>  {
              this.mensagemSucesso = `Escala salva com sucesso.`;

            }).catch( erro => {
                this.mensagemErro = `Erro ao registrar escala`;
                console.log(erro);
            })
            .finally(() => {
                this.carregando = false;
            });
        },
        dataEstaPeriodo(inicio, fim, dataCelula) {
            return moment(moment(dataCelula).add(1, 'm')).isBetween(inicio, fim);
        },
        colaboradoresDia: function(dia, hora){
            let dataEscala = moment(this.escala.dataInicio).add(dia - 1, 'days').format('DD/MM/YYYY');
            let horas = this.turno.turno.horaInicio.split(':');
            let horaEscala = moment({hour: horas[0], minute: horas[1]}).add(hora, 'h').format('HH:mm');
            let dataCelula = moment(dataEscala + ' ' + horaEscala);
            //console.log(this.escalaColaboradorList);
            return this.escalaColaboradorList.filter(
                y => this.dataEstaPeriodo(y.dataInicio.format('DD/MM/YYYY HH:mm'),
                                     y.dataFim.format('DD/MM/YYYY HH:mm'),
                                     dataCelula.format('DD/MM/YYYY HH:mm'))
            );
        },
    }
});