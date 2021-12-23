<template>
    <div>

        <!-- Info basica de zona -->
        <br>
        <h3>Usted esta en la zona "{{ nom }}"</h3>
        <br>
        <div>
            <button style="float:left; margin-left:45%; margin-bottom:20px; height:5rem; width:14rem; background:#00aec3; color:white; font-size:25px;" v-on:click="zona($route.params.id)">Centrar Mapa</button><br>
        </div>

        <!-- Mapa -->
        <div>
        <l-map style="height: 400px;" :zoom="zoom" :center="center">
            <l-tile-layer :url="url"></l-tile-layer>
            <div v-for="(zona, index) in zonas_all.atributos" :key="index">
            <l-polygon :lat-lngs="[zona.coordenadas]" :color="zona.color" :fill="true" :fillColor="zona.color" :fillOpacity="0.5" @click="onClick">
            <l-popup>
                        <strong>Nombre:</strong> {{zona.nombre}} <br>
                        <strong>Descripcion:</strong> {{zona.descripcion}}
            </l-popup>
            </l-polygon>
            </div>
        </l-map>
        </div>    

    <!-- Formulario -->
        <br>
        <div style="margin-left:30%;">
             <div style="" v-for="(zona,index) in zonas_all.atributos" :key="index">
                <p style="height:3rem; width:43rem;"><strong>Nombre de zona: </strong></p>
                <p class="box1">{{zona.nombre}}</p>
                <p style="height:3rem; width:43rem;"><strong>Descripcion: </strong></p>
                <p class="box1">{{zona.descripcion}}</p>
                <p style="height:3rem; width:43rem;"><strong>Coordenadas: </strong></p>
                <p class="box1" style="height:6rem;">{{zona.coordenadas}}</p>
                <br><br>
                <div> 
                    <a v-bind:href="'/zonas_inundables/'" style="color:blue; text-decoration:none;">
                        <div style="">    
                            <img src="../assets/volverZona.png" alt="Volver atras" style='height:60px; with:60px;'><br>
                            <button @click="Volver">Volver</button>
                        </div>
                    </a>

                </div>
            </div>
        </div>
        <br><br><br>
    </div>
</template>

<script>
    import {LMap, LTileLayer, LPolygon, LPopup} from '@vue-leaflet/vue-leaflet';

    export default {
        name:'Zona',

    components: {
        LMap,
        LTileLayer,
        LPolygon,
        LPopup,
    },
    data () {
        return {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        zoom: 14,
        center: [-34.92145, -57.95453],
        //   markerLatLng: [-34.92145, -57.95453],
        //center: [],
        zonas_all: [],
        nom: ' ',
        coordenadas: []
        };
    },
    created(){
      fetch('http://127.0.0.1:5000/api/zonas-inundables/'+ (this.$route.params.id)).then((response) => {
            console.log(response)
            return response.json();              
        }).then((json) => {
            console.log(json)
            this.zonas_all = json
            this.coordenadas = json.atributos[0].coordenadas[1]
            this.center = json.atributos[0].coordenadas[1]
            this.nom = json.atributos[0].nombre
            console.log('Esto ver: ' + this.center)
//            alert(this.center);
        }).catch((e) => {
            console.log(e)
        }) 
    },
    methods: {
        zona: function(valor) {
            fetch('http://127.0.0.1:5000/api/zonas-inundables/'+ valor).then((response) => {
                console.log(response)
                return response.json();  
            }).then((json) => {
                console.log(json)
                this.zonas_all = json
                this.center = json.atributos[0].coordenadas[1]
                this.nom = json.atributos[0].nombre
                console.log('Esto ver: ' + this.center)
            }).catch((e) => {
                console.log(e)
            }) 
    },
        anterior(){
        this.$router.go(-1)
        }
    }
}
</script>

<style>
    p {
        background-color:#f0f0f0;
        color:#000;
    }

    p.box1 {
        width:40rem;
        height: 3rem;
        padding:20px;
        font-size:italic;
        background-color:#cfc;
        color:#000;
    }
</style>