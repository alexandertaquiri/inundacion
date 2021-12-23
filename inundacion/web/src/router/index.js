//se definen las diferentes rutas y que componente se va a renderizar para cada ruta
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MapaDenuncias from '../views/MapaDenuncias.vue'
import ZonasInundables from '../views/ZonasInundables.vue'
import ZonaInundable from '../views/ZonaInundable.vue'
import RecorridosYPuntos from '../views/RecorridosYPuntos.vue'
import CargarDenuncia from '../views/CargarDenuncia.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/cargardenuncia',
    name: 'CargarDenuncia',
    component: CargarDenuncia
  },
  {
    path: '/mapadenuncias',
    name: 'MapaDenuncias',
    component: MapaDenuncias
  },
  {
    path: '/zonas_inundables',
    name: 'ZonasInundables',
    component: ZonasInundables
  },
  {
    path: '/zonas_inundable/:id',
    name: 'ZonaInundable',
    component: ZonaInundable
  }, 
  {
    path: '/recorridosYPuntos',
    name: 'RecorridosYPuntos',
    component: RecorridosYPuntos
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
