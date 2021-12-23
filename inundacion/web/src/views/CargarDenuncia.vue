<template>
<div class="container">
  <br><br>
    <h3 style="color:darkblue;">Realizar denuncia</h3> 
      <div class="mt-5">  

    <form style="padding:10px;" class="p-fluid" @submit.prevent="handleSubmit(!v$.$invalid)">
              <div class="form-row mb-2">
                    <div class="input-group">
                        <div class="form-group col-md-6 pr-2 left">
                            <br>
                           <label for="input-name" style="margin-top: 0px; margin-right: 100px">Información del denunciante:</label>
                           <br>
                            <div class="input-group mt-2">
                                <div class="form-group col-md-6 pr-2">
                                    <label class="form-label" :class="{'p-error':v$.nombre_denunciante.$invalid && submitted}">Nombre:</label>
                                    <input type="text" placeholder="nombre" class="form-control" name="nombre_denunciante" id="nombre_denunciante" aria-describedby="inputGroup-sizing-default" v-model="form.nombre_denunciante"/>
                                    <small v-if="(v$.nombre_denunciante.$invalid && submitted) || v$.nombre_denunciante.$pending.$response" class="p-error" style="color:blue">{{v$.nombre_denunciante.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                                <br>
                                <div class="form-group col-md-6 pr-2">
                                    <label class="form-label" :class="{'p-error':v$.apellido_denunciante.$invalid && submitted}">Apellido:</label>
                                    <input type="text" placeholder="apellido" class="form-control" name="apellido_denunciante" id="apellido_denunciante" aria-describedby="inputGroup-sizing-default" v-model="form.apellido_denunciante">
                                    <small v-if="(v$.apellido_denunciante.$invalid && submitted) || v$.apellido_denunciante.$pending.$response" class="p-error" style="color:blue">{{v$.apellido_denunciante.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                                <br>
                                <div class="form-group col-md-6 pr-2 left">
                                    <label class="form-label" :class="{'p-error':v$.tel_cel_denunciante.$invalid && submitted}">Teléfono de contacto:</label>
                                    <input type="text" placeholder="telefono" class="form-control" name="tel_cel_denunciante" id="tel_cel_denunciante" aria-describedby="inputGroup-sizing-default" v-model="form.tel_cel_denunciante">
                                    <small v-if="(v$.tel_cel_denunciante.$invalid && submitted) || v$.tel_cel_denunciante.$pending.$response" class="p-error" style="color:blue">{{v$.tel_cel_denunciante.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                                <br>
                                <div class="form-group col-md-6 pr-2">
                                    <label class="form-label" :class="{'p-error':v$.email_denunciante.$invalid && submitted}">Correo electrónico:</label>
                                    <input type="email" placeholder="email" class="form-control" name="email_denunciante" id="email_denunciante" aria-describedby="emailHelp" v-model="form.email_denunciante">
                                    <small v-if="(v$.email_denunciante.$invalid && submitted) || v$.email_denunciante.$pending.$response" class="p-error" style="color:blue">{{v$.email_denunciante.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                            </div>
                           

                            <div class="input-group mt-3">
                                 <label for="input-name" style="margin-top: 0px; margin-right: 100px">Información de la denuncia:</label>
                                 <br>
                                <div class="form-group col-md-6 pr-2 left">
                                    <br>
                                    <label class="form-label" :class="{'p-error':v$.titulo.$invalid && submitted}">Titulo:</label>
                                    <input type="text" placeholder="titulo" class="form-control" name="titulo" id="titulo" aria-describedby="inputGroup-sizing-default" v-model="form.titulo">
                                    <small v-if="(v$.titulo.$invalid && submitted) || v$.titulo.$pending.$response" class="p-error" style="color:blue">{{v$.titulo.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                                <br>

                                <div class="form-group col-md-6 pr-2">
                                    <label class="form-label" :class="{'p-error':v$.categoria_id.$invalid && submitted}">Categoria:</label>
                                    <select class="form-select" v-model="form.categoria_id">
                                        <option v-for="(categoria,index) in categorias" :key="index" :value="categoria.id_categoria">
							                                  {{categoria.nombre}}
						                            </option>
                                    </select>
                                    <small v-if="(v$.categoria_id.$invalid && submitted) || v$.categoria_id.$pending.$response" class="p-error" style="color:blue">{{v$.categoria_id.required.$message.replace('Value', 'Name')}}</small>
                                </div>
                                <br>
                                <div class="form-group col-md-12 pr-2 left">
                                    <label class="form-label" :class="{'p-error':v$.descripcion.$invalid && submitted}">Descripción:</label>
                                    <input type="text"  size="60" placeholder="descripcion" class="form-control" name="descripcion" id="descripcion" aria-describedby="inputGroup-sizing-default" v-model="form.descripcion">
                                    <small v-if="(v$.descripcion.$invalid && submitted) || v$.descripcion.$pending.$response" class="p-error" style="color:blue">{{v$.descripcion.required.$message.replace('Value', 'Name')}}</small>
                                </div>                    
                            </div>
                            <br>
                            
                            <div class="form-group col-md-3 pr-2">
                                <label for="latitud">Coordenadas:</label>&nbsp;
                                 <small v-if="(v$.latitud.$invalid && submitted) || v$.latitud.$pending.$response" class="p-error" style="color:blue">{{v$.latitud.required.$message.replace('Value', 'Name')}}</small>
                                <div class="input-group">
                                    <input type="text" name="lat" id="lat" v-model="form.latitud">
                                    <input type="text" name="lat" id="lng" v-model="form.longitud">
                                    <div class="map-container">
                                        <div id="mapid">
                                            <l-map style="height: 200px" @ready="onReady" :zoom="zoom" :center="center" @click="get_point">>
                                                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>                                                       
                                                <l-marker :lat-lng="markerLatLng" :draggable="true" ></l-marker>
                                            </l-map>
                                        </div>   
                                    </div>
                                </div>
                            </div>
                     

                        </div>                      
                        
                    </div>
                </div>

            <div style="margin-right: 900px; margin-top: -300px">
              <a type="button" style="border: 1px solid #138496;"  v-on:click="cancel()">Cancelar</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <button type="reset" class="btn btn-warning" style="background-color: orange;">Limpiar</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <button  style="background-color: blue; color: white" >Guardar</button> 
            </div>   
    </form>
</div>
</div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet';
import axios from 'axios'
import {required, email, numeric, helpers, alpha} from '@vuelidate/validators'
import useValidate from "@vuelidate/core";
import { reactive, computed, ref } from 'vue'



export default {
    name: "CargaDenuncia", 
    
    setup() {
      
      const form = reactive({
          apellido_denunciante: '',
          categoria_id: null,
          descripcion: '',
          email_denunciante: '',
          latitud: '',
          longitud: '',
          nombre_denunciante: '',
          tel_cel_denunciante: null,
          titulo: '', 
      })

      const rules = computed(() => {
            return{
            apellido_denunciante: { required: helpers.withMessage ("Campo requerido", required), alpha },
            categoria_id: { required: helpers.withMessage("Campo requerido", required) },
            descripcion: { required: helpers.withMessage("Campo requerido", required) },
            email_denunciante: { required: helpers.withMessage("Campo requerido", required), email },
            nombre_denunciante: { required: helpers.withMessage("Campo requerido", required), alpha },
            tel_cel_denunciante: { required: helpers.withMessage("Campo requerido", required), numeric}, 
            titulo: { required: helpers.withMessage("Campo requerido", required) },
            latitud: { required:  helpers.withMessage("Seleccione un punto en el mapa",  required) },
            }
      })
      const submitted = ref(false);
      const showMessage = ref(false);
      const v$ = useValidate(rules, form)
      const handleSubmit = (isFormValid) => {
          submitted.value = true;
          form.latitud = document.getElementById("lat").value;
          console.log(form.latitud)
          if(!isFormValid){
              alert('Debe completar los campos necesarios')
              return;
          } 
          toggleDialog();
          
          axios.post("http://127.0.0.1:5000/api/denuncias/", form);             
          alert('Se creo denuncia exitosamente')
          window.location.href='/';
        }

        const toggleDialog = () => {
            showMessage.value = !showMessage.value;
            if(!showMessage.value) {
                resetForm();
            }
        }
        const resetForm = () => {
            form.apellido_denunciante = '';
            form.categoria_id = null;
            form.descripcion = '';
            form.email_denunciante = '';
            form.latitud = '';
            form.longitud = '';
            form.nombre_denunciante = '';
            form.tel_cel_denunciante = null;
            form.titulo = '';
            submitted.value = false;
        }
        
        return { form, v$, handleSubmit, toggleDialog, submitted, showMessage}

    },
    data(){
        return{
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          zoom: 12,
          center: [-34.92145, -57.95453],
          markerLatLng: [51.504, -0.159],
          categorias: [] // Lista de categorias                 
        }
    },

    created() {
    fetch('http://127.0.0.1:5000/api/categorias/')
      .then((response2) => {
        if (response2.ok){
             return response2.json();
        }
      })
      .then((json2) => {
        console.log(json2);
        this.categorias = json2.categorias;
      })
      .catch((e1) => {
        console.log(e1);
      });
    },
        
    components: {
        LMap,
        LTileLayer,
        LMarker,
    },
    methods: {
        onReady (mapObject) {
        mapObject.locate();
        },
        onLocationFound(location){
        this.center = location.latlng
        },
        cancel(){
            this.$router.push("/");
        },
        get_point(e) {
          if (e.latlng) {
            this.punto = e.latlng;
            this.markerLatLng = e.latlng;
            this.form.latitud = this.punto["lat"];
            this.form.longitud = this.punto["lng"];
          }
          console.log("Form Coordenadas");
          console.log(this.form.latitud , this.form.longitud);
        },     
    }
}
</script>


<style scoped>

@media(max-width: 576px){
    #mapid{
        height: 500px;
        width: 450px;
    }
}
  @media(min-width: 576px){
    #mapid{
        height: 500px;
        width: 600px;
    }
}

#lat, #lng{
    display:  none;        
}

label{
    color: green;
    font-weight: bold;
}


.contenido{
  min-height: calc(100vh - 70px - 90px);
}

.content-page{
  margin: 1rem;
}

.centered {
  padding-left: 30% !important;
}

.text-center{
  text-align: center;
}

.right{
text-align: right;
}

.left{
  text-align: left;
}

#submitButton{
  border: none !important;
  background: none !important;
}

.btn-primary {
  background-color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}
.btn-primary:hover{
  background-color: var(--primary-color) !important;
  filter: brightness(95%);
}
.border-botton-dotted{
  border-bottom: 2px solid var(--primary-color) !important;;
  width: 30%;
  padding: 1rem;
}
.ml-1{
  margin-left: 1rem;
}
.ml-2{
  margin-left: 2rem;
}
.ml-3{
  margin-left: 3rem;
}
.ml-4{
  margin-left: 4rem;
}
.ml-5{
  margin-left: 5rem;
}
.mr-1{
  margin-right: 1rem;
}
.mr-2{
  margin-right: 2rem;
}
.mr-3 {
  margin-right: 3rem;
}
.mr-4 {
  margin-right: 4rem;
}
.mr-5 {
  margin-right: 5rem;
}
.mr-6 {
  margin-right: 6rem;
}
.mr-7 {
  margin-right: 7rem;
}
.mr-8 {
  margin-right: 8rem;
}
.mr-9 {
  margin-right: 9rem;
}
.mr-10 {
  margin-right: 10rem;
}
.mr-20 {
  margin-right: 20rem;
}
.mt-1{
  margin-top: 1rem;
}
.mt-2{
  margin-top: 2rem;
}
.mt-3{
  margin-top: 3rem;
}
.mt-4{
  margin-top: 4rem;
}
.mt-5{
  margin-top: 5rem;
}
.mb-1{
  margin-bottom: 1rem;
}
.mb-2{
  margin-bottom: 2rem;
}
.mb-3{
  margin-bottom: 3rem;
}
.mb-4{
  margin-bottom: 4rem;
}
.mb-5{
  margin-bottom: 5rem;
}
.pl-1 {
  padding-left: 1rem;
}
.pl-2 {
  padding-left: 2rem;
}
.pl-3 {
  padding-left: 3rem;
}
.pl-4 {
  padding-left: 4rem;
}
.pl-5 {
  padding-left: 5rem;
}
.pr-1{
  padding-right: 1rem;
}
.pr-2{
  padding-right: 2rem;
}
.pr-3{
  padding-right: 3rem;
}
.pr-4{
  padding-right: 4rem;
}
.pr-5{
  padding-right: 5rem;
}
.pt-1{
  padding-top: 1rem;
}
.pt-2{
  padding-top: 2rem;
}
.pt-3{
  padding-top: 3rem;
}
.pt-4{
  padding-top: 4rem;
}
.pt-5{
  padding-top: 5rem;
}
.pb-1{
  padding-bottom: 1rem;
}
.pb-2{
  padding-bottom: 2rem;
}
.pb-3{
  padding-bottom: 3rem;
}
.pb-4{
  padding-bottom: 4rem;
}
.pb-5{
  padding-bottom: 5rem;
}
.checkbox-1x {
  transform: scale(1.5);
  -webkit-transform: scale(1.5);
}
.checkbox-2x {
  transform: scale(2);
  -webkit-transform: scale(2);
}
</style>
