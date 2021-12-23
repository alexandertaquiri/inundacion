<template>
  <div>
    <div v-bind:style="{ backgroundColor: colorNav }" id="nav">
      <router-link :to="{ name: 'Home' }">Home</router-link> |
      <router-link to="/cargardenuncia">¿Quiere realizar una denuncia?</router-link> |
      <router-link to="/mapadenuncias">Mapa de denuncias confirmadas</router-link> |
      <router-link to="/zonas_inundables">Zonas Inundables </router-link> |
      <router-link to="/recorridosYPuntos">Recorridos y Puntos</router-link> |
    </div>
    <div v-bind:style="{ backgroundColor: colorBody }" id="cuerpo">
      <router-view/>
    </div>
    <div v-bind:style="{ backgroundColor: colorFooter }" id="footer">
      <h5><span>© 2021 Copyright | Grupo 09 | Todos los derechos reservados La Plata, Argentina</span></h5>
      <h5><span><strong style="font-weight: bold;">{{ configuracion }}</strong></span></h5>
    </div>
  </div>
</template>


<script>
  export default {
    data(){
      return{
        colorNav: '#e3eee3',
        colorFooter: '#9d9f9f',
        colorBody: '#bdf5de',
        configuracion: ' '
    };
    },
    created(){    
      fetch('http://127.0.0.1:5000/api/configuracion-api/').then((response) => { 
          if(response.ok){
              return response.json()    
          } else{
              this.configuracion = 'No se estan utilizando los colores de la configuración'
         }                
      })
      .then((json) => {
          this.colorNav = json.colores_publicos[0][0];
          this.colorFooter = json.colores_publicos[0][1];
          this.colorBody = json.colores_publicos[0][2];
          this.configuracion = 'Se estan utilizando los colores de la configuracion';
          console.log("el json es: "+ json.colores_publicos[0][2]); 
      })
      .catch((err) => {
          console.log(err);
      });
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  min-height: 30px;
  border-top: 1px solid rgba(50, 50, 50, 0.3);
  bottom: 0; 
  width: 100vw;
}

#nav a {
  font-weight: bold;
  padding: 20px;

  /* color: blue ;  --- aca poner el color de los botones */
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#footer {
  min-height: 5px;
  border-top: 1px solid rgba(50, 50, 50, 0.3);
  width: 100vw;
  /* position: fixed; */
  bottom: 0;
}

#cuerpo {
  width: 100vw;
  height: 100vw;
}

#cuerpo a {
  padding: 20px;
}


</style>
