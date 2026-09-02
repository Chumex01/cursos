<template>
  <div class="bg-[#0b0f19] text-white min-h-screen py-12 px-4 flex items-center justify-center">
    <!-- Estado de Carga -->
    <div v-if="cargando" class="text-center text-slate-400">
      <p>Cargando datos de la orden...</p>
    </div>

    <!-- Estado de Error -->
    <div v-else-if="error" class="bg-[#121829] p-8 rounded-xl border border-red-500/30 text-center max-w-md w-full">
      <h2 class="text-xl font-bold text-red-400 mb-2">Error al procesar</h2>
      <p class="text-slate-300 text-sm mb-6">{{ error }}</p>
      <router-link to="/cursos" class="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition">
        Volver a Cursos
      </router-link>
    </div>

    <!-- Formulario de Checkout -->
    <div v-else-if="curso" class="max-w-xl w-full bg-[#121829] border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl">
      <div class="border-b border-slate-800 pb-6 mb-6">
        <span class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Resumen del Pedido</span>
        <h1 class="text-2xl font-extrabold mt-1">{{ curso.titulo }}</h1>
        <p class="text-slate-400 text-sm mt-1">Nivel: {{ curso.nivel }}</p>
      </div>

      <div class="bg-[#1e293b]/50 p-4 rounded-xl border border-slate-700/50 mb-6 flex justify-between items-center">
        <span class="text-slate-300 text-sm font-medium">Total a pagar:</span>
        <span class="text-2xl font-black text-emerald-400">
          {{ curso.moneda }} {{ curso.precio }}
        </span>
      </div>

      <form @submit.prevent="procesarPago" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Nombre completo</label>
          <input 
            v-model="formulario.nombre" 
            type="text" 
            required
            placeholder="Ej. Juan Pérez" 
            class="w-full bg-[#1e293b] border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
          />
        </div>

        <div>
          <label class="block text-xs font-medium text-slate-300 mb-1">Correo electrónico</label>
          <input 
            v-model="formulario.email" 
            type="email" 
            required
            placeholder="juan@ejemplo.com" 
            class="w-full bg-[#1e293b] border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" 
          />
        </div>

        <button 
          type="submit" 
          :disabled="procesando"
          class="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white font-bold py-3.5 rounded-xl transition duration-200 mt-6 shadow-lg shadow-emerald-900/20"
        >
          {{ procesando ? 'Procesando pago...' : 'Confirmar y Pagar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { getCursoBySlug } from '../services/api'

export default {
  name: 'CheckoutView',
  data() {
    return {
      curso: null,
      cargando: true,
      procesando: false,
      error: null,
      formulario: {
        nombre: '',
        email: ''
      }
    }
  },
  async mounted() {
    await this.cargarCurso()
  },
  methods: {
    async cargarCurso() {
      this.cargando = true
      this.error = null
      try {
        const slug = this.$route.params.slug
        this.curso = await getCursoBySlug(slug)
      } catch (err) {
        this.error = err.message || 'No se pudo obtener la información del curso.'
      } finally {
        this.cargando = false
      }
    },
    async procesarPago() {
      this.procesando = true
      // Simulación de procesamiento de pasarela de pago
      setTimeout(() => {
        this.procesando = false
        this.$router.push('/pago-aprobado')
      }, 1500)
    }
  }
}
</script>