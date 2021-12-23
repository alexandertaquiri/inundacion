<template>
  <!-- <button @click="home">Ir a home</button> -->
  <ZonasPaginaActual />  
</template>

<script>

  import ZonasPaginaActual from "@/components/ZonasPagina.vue";

  export default{
    name: 'ZonasPagina',
    components: {
      ZonasPaginaActual
    }
  }

</script>