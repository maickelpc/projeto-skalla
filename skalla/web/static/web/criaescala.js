$(document).ready(function(){
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
            this.escala.turnoPonto = val;
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
            this.horasDesdeUltimaEscala(colaborador.id)
            this.escalaColaboradorList.push(this.escalaColaborador);
            this.escalaColaborador = {
                dataInicio: null,
                dataFim: null,
                colaborador: {}
            };
            // for(let i = 0; i < this.colaboradoresDisponiveis.length; i++) {
            //     if(this.colaboradoresDisponiveis[i].id === colaborador.id) {
            //         this.colaboradoresDisponiveis.splice(i, 1);
            //     }
            // }
            console.log(this.escalaColaboradorList);
        },
        colaboradorEstaDisponivelData(colaborador, data) {
            var disponivel = true;
            data = moment(data);
            for(let i = 0; i < this.escalaColaboradorList.length; i++) {
                if((data.diff(moment(this.escalaColaboradorList[i].dataInicio), 'h') < this.turno.horasDescanso) &&
                    (colaborador.id === this.escalaColaboradorList[i].colaborador.id)) {
                    console.log(disponivel);
                    disponivel = false;
                }
            }
            return disponivel;
        },
        retornaColaboradoresDisponiveisData(data) {
            return(this.colaboradoresDisponiveis.filter(
                y => this.colaboradorEstaDisponivelData(y, data)
            ));
        },
        abreModalColaboradores(dataInicial, dia, horaInicio, horaFim) {
            let dataEscala = moment(dataInicial).add(dia - 1, 'days').format('YYYY-MM-DD');
            this.escalaColaborador.dataInicio = moment(dataEscala + " " + horaInicio);
            this.escalaColaborador.dataFim = moment(dataEscala + " " + horaFim);
        },
        getIntervaloHoras: function(horaInicio, horaFim) {
            let inicio = moment(horaInicio, "HH:mm");
            let fim = moment(horaFim, "HH:mm");

            return fim.diff(inicio, 'hours');
        },
        async getColaboradores() {
          this.loading = true;
          this.$http.get('/api/colaborador/')
              .then((response) => {
                this.colaboradoresDisponiveis = response.data.results;
                this.setHorasDescansoColaboradores();
                this.loading = false;
              })
              .catch((err) => {
               this.loading = false;
               console.log(err);
              })
         },
        setHorasDescansoColaboradores() {
            for(let i = 0; i < this.colaboradoresDisponiveis.length; i++) {
                this.horasDesdeUltimaEscala(
                    this.colaboradoresDisponiveis[i]
                );
            }
            console.log(this.colaboradoresDisponiveis);
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
        horasDesdeUltimaEscala(colaborador){
            let headers = {
                'Content-Type': 'application/json',
                "X-CSRFToken": token
              };
            this.$http.get(`/api/escala-colaborador/horasdesdeultimaescala/?idcolaborador=`+colaborador.id)
            .then( response =>  {
                resposta = response.data;
                console.log(resposta);
                colaborador.horasDescanso = resposta.horasDescanso >= 0 ? resposta.horasDescanso : 0;
                //this.mensagemSucesso = `Horas Recuperadas com sucesso.`;

            }).catch( erro => {
                //this.mensagemErro = `Erro ao recuperar horas do colaborador.`;
                colaborador.horasDescanso = 1000;
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
            let dataEscala = moment(this.escala.dataInicio).add(dia - 1, 'days').format('YYYY-MM-DD');
            let horas = this.turno.turno.horaInicio.split(':');
            let horaEscala = moment({hour: horas[0], minute: horas[1]}).add(hora, 'h').format('HH:mm');
            let dataCelula = moment(dataEscala + ' ' + horaEscala);
            return this.escalaColaboradorList.filter(
                y => this.dataEstaPeriodo(y.dataInicio.format('YYYY-MM-DD HH:mm'),
                                     y.dataFim.format('YYYY-MM-DD HH:mm'),
                                     dataCelula.format('YYYY-MM-DD HH:mm'))
            );
        },
    }
});