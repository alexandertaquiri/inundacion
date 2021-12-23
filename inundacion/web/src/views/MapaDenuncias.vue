<template>
  <div>
    <br><br>
    <b style="font-size:25px;">Mapa de denuncias confirmadas</b><br><br>
   <div class="map-container">
    <div id="mapid">
      <l-map @ready="onReady" @locationfound="onLocationFound" :zoom="zoom" :center="center" >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div v-for="(denuncia, index) in denuncias" :key="denuncias - { index }">
          <div v-if="denuncia.estado != 'Sin confirmar'" >
            <l-marker  :lat-lng="[denuncia.latitud, denuncia.longitud]">
                <l-popup>
                <div> <b>Titulo:</b> {{ denuncia.titulo }} </div>
                <div> <b>Descripcion:</b> {{ denuncia.descripcion }} </div>   
                <div> <b>Estado:</b> {{ denuncia.estado }} </div>                                           
                </l-popup>
            </l-marker>
            </div>  
        </div>
      </l-map>
    </div>
    <br>
  </div>
  <br>
  <br>

  <div>
    <a type="button" class="btn btn-default" style="border: 1px solid #138496; padding: 6px 14px;
    margin-top: 6px;"  v-on:click="atras()">Volver</a>
  </div>  
  <br><br><br><br>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  methods: {
    onReady(mapObject) {
      mapObject.locate();
    },
    atras(){
            this.$router.push("/");
    },
    onLocationFound(location) {
      this.center = location.latlng;
    },
    mostrar: function (lat,long) {
        this.zoom = 15        
        this.center = [lat,long]
        console.log(lat,long);
      },
    volver: function () {
        this.zoom = 12        
        this.center = [-34.92149,-57.954597]
        
      }
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 12,
      center: [-34.92149, -57.954597],
      denuncias: [],
    };
  },
  created() {
    fetch('http://127.0.0.1:5000/api/denuncias/')
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        console.log(json);
        this.denuncias = json.denuncias;
      })
      .catch((e) => {
        console.log(e);
      });
  },
};
</script>

<style scoped>

#volver{
  justify-content: center
}
.map-container {
  display: flex;
  justify-content: center;
}

#mapid {
  height: 500px;
  width: 1200px;
}


ul{
text-align: left
}


</style>
