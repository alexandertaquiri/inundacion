<template>
<div>
    <div id="botones">
       <div v-if="actual == 1">
         <button style="height: 3rem; width: 6rem; color: #ACADAC;" :disabled='isDisabled'>Anterior</button>
       </div>

       <div v-if="actual > 1">
         <button style="height: 3rem; width: 6rem; background: #00AEC3; color: white;" v-on:click="recorridosPuntos(actual -= 1)">Anterior</button>
       </div>

       <div v-if="encontroSiguiente == true">
         <button style="height: 3rem; width: 6rem; background: #00AEC3; color: white;" v-on:click="recorridosPuntos(actual += 1)">Siguiente</button>
       </div>

      <p>Página actual: <strong>{{ actual }}</strong></p>
    </div>

    <div>
       <l-map style="height: 400px;" :zoom="zoom" :center="center">
        <l-tile-layer :url="url"></l-tile-layer>
        <div v-for="(recorrido, index) in recorridos_all[0].recorridos" :key="index">
         <l-polyline :lat-lngs="[recorrido.coordenadas]" :fillOpacity="0.5">
          <l-popup><strong>Nombre:</strong> {{recorrido.nombre}}, <strong>Descripción:</strong> {{recorrido.descripcion}}</l-popup>
         </l-polyline> 
        </div>

        <div v-for="(punto, index2) in puntos_encuentro_all[0].puntos_encuentro" :key="index2">
          <l-marker :lat-lng="[punto.lat, punto.long]" >
            <l-popup><strong>Nombre:</strong> {{punto.nombre}}, <strong>Dirección:</strong> {{punto.direccion}}, <strong>Teléfono:</strong> {{punto.telefono}}, <strong>Email:</strong> {{punto.email}}</l-popup>
          </l-marker>
        </div> 
       </l-map>
    </div>

     <h1 style="margin-top: 30px; color: #333333; text-align: left; margin-left: 45px;"> Recorridos de Evacuación </h1>
     <div id="nav">
      <table class="table" style="border: 1px solid #CCC; border-radius: 10px;">
        <thead>
          <tr>
            <th style="max-width: 300px; min-width: 200px;"><strong>Nombre</strong></th>
            <th style="max-width: 300px; min-width: 200px;"><strong>Descripción</strong></th>
            <th style="max-width: 300px; min-width: 300px;"><strong>Coordenadas</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(recorrido,index) in recorridos_all[0].recorridos" :key="index">
            <td>{{recorrido.nombre}}</td>
            <td>{{recorrido.descripcion}}</td>
            <td v-if="recorrido.coordenadas[0] != 0">{{recorrido.coordenadas}}</td>
            <td v-if="recorrido.coordenadas[0] == 0">No registra</td>
          </tr>    
        </tbody>
      </table>
    </div>

    <h1 style="margin-top: 30px; color: #333333; text-align: left; margin-left: 45px;"> Puntos de Encuentro </h1>
    <div id="nav">
      <table class="table" style="border: 1px solid #CCC; border-radius: 10px;">
        <thead>
          <tr>
            <th style="max-width: 150px; min-width: 150px;"><strong>Nombre</strong></th>
            <th style="max-width: 150px; min-width: 150px;"><strong>Dirección</strong></th>
            <th style="max-width: 300px; min-width: 300px;"><strong>Coordenadas</strong></th>
            <th style="max-width: 150px; min-width: 150px;"><strong>Teléfono</strong></th>
            <th style="max-width: 150px; min-width: 150px;"><strong>Email</strong></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(punto,index) in puntos_encuentro_all[0].puntos_encuentro" :key="index">
            <td>{{punto.nombre}}</td>
            <td>{{punto.direccion}}</td>
            <td v-if="punto.lat != 0">{{punto.lat}}, {{punto.long}}</td>
            <td v-if="punto.lat == 0">No registra</td>  
            <td>{{punto.telefono}}</td>
            <td>{{punto.email}}</td>
          </tr>    
        </tbody>
      </table>
    </div>
</div>
</template>



<script>
import {LMap, LTileLayer, LPolyline, LMarker, LPopup} from '@vue-leaflet/vue-leaflet';

export default {
  name:'RecorridosYPuntosActual',

  components: {
    LMap,
    LTileLayer,
    LPolyline,
    LMarker,
    LPopup
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 11,
      center: [-34.92145, -57.95453],//[]
      recorridos_all: [],
      puntos_encuentro_all: [],
      actual: 1,
      encontroSiguiente: false
      // dominio: Vue.prototype.$hostname="http://127.0.0.1:5000/api/"
    };
  },
  created(){
      this.reiniciarRecorridos()
      this.reiniciarPuntos()
      this.recorridosPuntos(this.actual)
  },
   methods: {
    reiniciarRecorridos: function(){
      this.recorridos_all = [{ "pagina": "No registra", 
                         "total": "No registra", 
                         "recorridos": [ { "coordenadas": [0, 0], 
                                           "descripcion": "No registra", 
                                           "id": "No registra", 
                                           "nombre": "No registra" } ] }]
    },
    reiniciarPuntos: function(){
      this.puntos_encuentro_all = [{ "pagina": "No registra", 
                               "total": "No registra",
                               "puntos_encuentro": [ { "direccion": "No registra", 
                                                       "email": "No registra", 
                                                       "id": "No registra", 
                                                       "lat": 0, 
                                                       "long": 0, 
                                                       "nombre": "No registra", 
                                                       "telefono": "No registra" } ] }]
    },
    recorridosPuntos: function(valor){
      fetch('http://127.0.0.1:5000/api/recorridos-evacuacion/' + valor).then((response) => {
          if(response.ok){
              this.encontroSiguiente = true
              return response.json()
          }   
          else {
              this.encontroSiguiente = false
              this.actual = 1
              if (valor != 1) {
                this.recorridosPuntos(this.actual)
              }
          } 
      }).then((json) => {
          this.recorridos_all = json
          if (this.encontroSiguiente == false) {
            this.reiniciarRecorridos()
          }
      }).catch((e) => {
          console.log(e);
          alert("La página harcodeada no existe. Usted será redirigido");
          window.location.href = "/";
      })
      
      fetch('http://127.0.0.1:5000/api/puntos-encuentro/' + valor).then((response2) => {
          if(response2.ok){
              this.encontroSiguiente = true
              return response2.json()    
          }   
          else {
              this.encontroSiguiente = false
              this.actual = 1
              if (valor != 1) {
                this.recorridosPuntos(this.actual)
              }
          } 
      }).then((json2) => {
          this.puntos_encuentro_all = json2
          if (this.encontroSiguiente == false) {   
              this.reiniciarPuntos()
          }
      }).catch((e) => {
          console.log(e);
          alert("La pagina harcodeada no existe. Usted será redirigido");
          window.location.href = "/";
      })  
    }
  }
}
</script>

<style>
#nav {
    padding-top: 0px;
    padding-bottom: 0px;
}

#botones {
    padding-top: 30px;
}

table {
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 20px;
    width: 480px; 
    text-align: left;    
    border-collapse: collapse; 
    min-width: 1000px;
}

th {
  font-size: 13px;     
  font-weight: normal;     
  padding: 8px;     
  background: #b9c9fe;
  border-top: 4px solid #aabcfe;    
  border-bottom: 1px solid #fff; 
  color: #039; 
}

td {padding: 8px;
    background: #e8edff;
    border-bottom: 1px solid #fff;
    color: #669;    
    border-top: 1px solid transparent; 
}

tr:hover td { 
  background: #d0dafd; 
  color: #339; 
}
</style>
