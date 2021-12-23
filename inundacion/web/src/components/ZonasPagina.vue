<template>

    <div>        
        <br><br>
        <div>
          <!-- <b>Pagina actual: {{ $route.params.page }}</b><br><br> -->
          <b>Pagina actual: {{ actual }}</b><br><br>
          <div id="example-1" style="">
            <div v-if="actual > 1">
                <button style="float:left; margin-left:500px; margin-bottom:20px; height:3rem; width:6rem; background:#00aec3; color:white;" v-on:click="zona(actual -= 1)">Anterior</button>
            </div>
            <div v-if="siguiente != false">
                <button style="float:rigth; margin-rigth:500px; margin-bottom:20px; height:3rem; width:6rem; background:#00aec3; color:white;" v-on:click="zona(actual += 1)">Siguiente</button>
            </div>
          </div>
        </div>
        <br><br>
        
        <!-- Mapa -->
        <div>
          <l-map @ready="onReady" style="height: 400px;" :zoom="zoom" :center="center" :options="{zoomControl: true}">
            <l-tile-layer :url="url"></l-tile-layer>
            <div v-for="(zona, index) in zonas_all[0].zonas" :key="index">
            <l-polygon :lat-lngs="[zona.coordenadas]" :color="zona.color" :fill="true" :fillColor="zona.color" :fillOpacity="0.5" @click="onClick">
              <l-popup>Nombre: {{zona.nombre}} </l-popup>
            </l-polygon>
            </div>
          </l-map>
        </div>    

        <!-- Formulario -->
        <div id="nav">
          <table class="table" style="border:1px solid #ccc; position:center; width:90%; height:20rem;">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripcion</th>
                <th>Coordenadas</th>
                <th>Accion</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(zona,index) in zonas_all[0].zonas" :key="index">
                <td>
                  {{zona.nombre}}
                </td>
                <td>
                  {{zona.descripcion}}
                </td>
                <td>
                  {{zona.coordenadas}}
                </td>
                <td v-if="zona.nombre != 'Sin zonas'">
                  <a v-bind:href="'/zonas_inundable/'+ zona.id" style="color:blue; text-decoration: none;">
                    <img src="../assets/LupaZona.png" alt="Icono para ver el detalle de la zona" style='height:20px; with:50px;'>
                  </a>
                </td>
                <td v-else>
                  Sin acciones
                </td>
              </tr>    
            </tbody>
          </table>
        </div>
      <br><br>
    </div>
</template>

<script>
import {LMap, LTileLayer, LPolygon, LPopup} from '@vue-leaflet/vue-leaflet';

export default {
    name:'ZonasPaginaActual',
    
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPopup,
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 11,
      center: [-34.92145, -57.95453],
    //   markerLatLng: [-34.92145, -57.95453],
      zonas_all: [],
      actual: 1,
      siguiente: false
    };
  },
  created(){
    this.reiniciarZonas()
    this.zona(this.actual)
  },
  // created(){
  //     fetch('http://127.0.0.1:5000/api/zonas-inundables-all/'+ (this.actual)).then((response) => {
  //       if(response.ok){
  //             return response.json()
  //       } else {
  //             alert("No hay zonas inundables para mostrar en este momento. Ingrese mas tarde")
  //             window.location.href = "/";
  //       }
  //     }).then((json) => {
  //         console.log(json)
  //         this.zonas_all = json
  //         console.log("Probando " + json[0])
  //     }).catch((e) => {
  //         console.log(e)
  //     }) 
  // },
  methods: {
    reiniciarZonas: function(){
      this.zonas_all = [
          {
            "pagina": "Sin zonas", 
            "total": "Sin zonas", 
            "zonas": [
              {
                "color": "Sin zonas", 
                "coordenadas": [0,0], 
                "descripcion": "Sin zonas", 
                "id": "Sin zonas", 
                "nombre": "Sin zonas"
              }
            ]
          }]
    },
    zona: function(valor){
      fetch('http://127.0.0.1:5000/api/zonas-inundables-all/' + valor).then((response) => {
          if(response.ok){
              this.siguiente = true
              return response.json()              
          } else {
              this.siguiente = false
              this.actual = 1
              if (valor != 1){
                this.zona(this.actual)
              }
//          } else  {
              //alert("El servidor retorna " + response.status + " : " + response.statusText);
//              console.log(response.json())
              //window.location.href = "/zonas_inundables";
          }  
      }).then((json) => {
          this.zonas_all = json
          if (this.siguiente == false){
            this.reiniciarZonas()
          }
      }).catch((e) => {
          console.log(e);
          alert("La pagina no existe. Usted sera redirigido");
          window.location.href = "/";
      }) 
    }
  }
}
</script>

<style>

table {
    font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
    font-size: 12px;
    margin: 45px;
    width: 480px; 
    text-align: left;    
    border-collapse: collapse; 
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