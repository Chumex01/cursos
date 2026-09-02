import { createRouter, createWebHistory } from 'vue-router'

// Importación de Vistas
import InicioView from '../views/InicioView.vue'
import ServiciosView from '../views/ServiciosView.vue'
import PortafolioView from '../views/PortafolioView.vue'
import CursosView from '../views/CursosView.vue'
import CursoDetalleView from '../views/CursoDetalleView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import PagoAprobadoView from '../views/PagoAprobadoView.vue'
import AulaCursoView from '../views/AulaCursoView.vue'

const routes = [
  {
    path: '/',
    name: 'Inicio',
    component: InicioView
  },
  {
    path: '/servicios',
    name: 'Servicios',
    component: ServiciosView
  },
  {
    path: '/portafolio',
    name: 'Portafolio',
    component: PortafolioView
  },
  {
    path: '/cursos',
    name: 'Cursos',
    component: CursosView
  },
  {
    path: '/cursos/:slug',
    name: 'CursoDetalle',
    component: CursoDetalleView
  },
  {
    path: '/checkout/:slug',
    name: 'Checkout',
    component: CheckoutView
  },
  {
    path: '/pago-aprobado',
    name: 'PagoAprobado',
    component: PagoAprobadoView
  },
  {
    path: '/aula/:slug',
    name: 'AulaCurso',
    component: AulaCursoView
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/cursos'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router