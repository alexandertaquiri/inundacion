<template>

  <div>
    <br><br>

    <div class="col-sm-12">
      <b>¡Bienvenidos!</b>
      <h3>En ésta página web encontraras toda la informacion referente a las denuncias realizadas por los visitantes reflejadas en un mapa. Crear una solicitud de carga de una nueva denuncia. 
      Ver puntos de encuentros y recorridos de evacuacion en el mapa. Ver zonas inundables en el mapa.</h3>
    </div>

    <div class="container">

        <div style="margin-left: 600px; margin-top: 100px">
          <div class="col">
            <h2 style="font-family: 'Monoton'; color: blue"><b>¿Quiere realizar una denuncia?</b></h2>
            <img src="../assets/denuncia.jpg" alt="Icono que denota los puntos de encuentro" style='height:200px; with:200px; border-radius: 150px' >
            <div>
                <br>
                <router-link to="/CargarDenuncia" type="button" class="btn btn-default" style="border: 1px solid #138496; margin-right: 10px; color: green">Ver detalles</router-link>
                <br><br>
            </div>
          </div> 
        </div>

         <div style="margin-right: 600px; margin-top:-325px; ">

                <div class="col">
                    <h2 style="font-family: 'Monoton'; color: blue"><b>Recorridos de Evacuacion y Puntos de Encuentro</b></h2>
                    <img src="../assets/recorrido.jpg" alt="Icono que denota los puntos de encuentro" style='height:200px; with:200px; border-radius: 150px'>
                    <div>
                        <br>
                        <router-link to="/recorridosYPuntos" type="button" class="btn btn-default" style="border: 1px solid #138496; margin-right: 10px; color: green">Ver detalles</router-link>
                        <br><br>
                    </div>
                </div>

                <div class="col">
                    <h2 style="font-family: 'Monoton'; color: blue"><b>Mapas de Zonas Inundables</b></h2>
                    <img src="../assets/mapa.jpg" alt="Icono que denota los puntos de encuentro" style='height:200px; with:200px; border-radius: 150px'>
                    <div>
                        <br>
                        <!-- <router-link to="/zonas_inundables/1" type="button" class="btn btn-default" style="border: 1px solid #138496; margin-right: 10px; color: green">Ver detalles</router-link> -->
                          <!-- <a v-bind:href="'/zonas_inundable/'+ 1" style="color:blue; text-decoration: none;">   -->
                        <router-link :to="{ name: 'ZonasInundables'}">Ver detalles</router-link>

                        <br><br>
                    </div>
                </div>
              </div>
    </div>
  </div>


</template>

<script>
export default {
  data(){
    return{
      zonaInicial: 1
    }
  }
}
</script>