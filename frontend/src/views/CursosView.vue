<template>

    <nav class="fixed top-0 w-full z-50 bg-[#0f172a]/90 backdrop-blur-md border-b border-slate-800">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-extrabold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">Hello World</router-link>
        <div class="hidden md:flex gap-8 text-sm font-medium text-slate-400">
          <router-link to="/servicios" class="hover:text-white transition">Servicios</router-link>
          <router-link to="/portafolio" class="hover:text-white transition">Portafolio</router-link>
          <router-link to="/cursos" class="hover:text-white transition">Cursos</router-link>
        </div>
        <router-link to="/servicios" class="bg-violet-600 hover:bg-violet-700 text-white px-5 py-2 rounded-lg text-sm font-bold transition">Cotizar</router-link>
      </div>
    </nav>

  <div class="bg-[#0b0f19] text-white min-h-screen">
    <!-- Hero Header -->
    <section class="bg-[#121829] py-12 px-6">
      <div class="max-w-6xl mx-auto">
        <span class="text-orange-500 font-bold text-xs uppercase tracking-wider">Academia Hello World</span>
        <h1 class="text-4xl font-extrabold mt-2">Catálogo de cursos</h1>
        <p class="text-slate-400 mt-2">
          Aprende tecnología a tu ritmo, desde La Paz o desde donde estés. <strong class="text-white">{{ totalGratis }} cursos gratuitos</strong> disponibles hoy.[cite: 1]
        </p>

        <!-- Buscador -->
        <div class="mt-6 max-w-xl">
          <input
            v-model="busqueda"
            @input="cargarCursos"
            type="text"
            placeholder="Buscar cursos: Python, React, SQL, Git, IA..."
            class="w-full bg-[#1e293b] text-white placeholder-slate-400 px-4 py-3 rounded-lg border border-slate-700 focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>
    </section>

    <!-- Bar de Filtros -->
    <section class="max-w-6xl mx-auto px-6 py-6 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-6 flex-wrap">
        <div class="flex items-center gap-2">
          <span class="text-slate-400 text-sm font-medium">Nivel:</span>
          <button v-for="n in ['Todos', 'Principiante', 'Intermedio', 'Avanzado']" :key="n"
            @click="nivel = n; cargarCursos()"
            :class="[nivel === n ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700']"
            class="px-3 py-1.5 rounded-full text-xs font-semibold transition">
            {{ n }}
          </button>
        </div>

        <div class="flex items-center gap-2">
          <span class="text-slate-400 text-sm font-medium">Precio:</span>
          <button v-for="p in [{label:'Todos', val:'todos'}, {label:'Gratis', val:'gratis'}, {label:'De pago', val:'pago'}]" :key="p.val"
            @click="precioFiltro = p.val; cargarCursos()"
            :class="[precioFiltro === p.val ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700']"
            class="px-3 py-1.5 rounded-full text-xs font-semibold transition">
            {{ p.label }}
          </button>
        </div>
      </div>
    </section>

    <!-- Lista de Cursos -->
    <section class="max-w-6xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="curso in cursos" :key="curso.id_curso" class="bg-[#121829] rounded-xl overflow-hidden border border-slate-800 flex flex-col">
          <div class="relative">
            <img :src="curso.imagen_principal_url || 'https://via.placeholder.com/400x225'" :alt="curso.titulo" class="w-full h-44 object-cover" />
            <span v-if="curso.es_gratuito" class="absolute top-3 left-3 bg-emerald-500 text-black text-xs font-extrabold px-2.5 py-1 rounded">
              GRATIS
            </span>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs px-2.5 py-0.5 rounded-full font-medium">
                  {{ curso.nivel }}
                </span>
                <span class="text-amber-400 text-xs font-bold">★ 4.7</span>
              </div>
              <h3 class="text-lg font-bold text-white leading-snug">{{ curso.titulo }}</h3>
              <p class="text-slate-400 text-xs mt-1">Instructor asignado</p>
            </div>
            <div class="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between">
              <span class="text-slate-400 text-xs">{{ curso.total_estudiantes || 0 }} estudiantes</span>
              <router-link :to="`/cursos/${curso.slug}`" class="text-right">
                <span v-if="curso.es_gratuito" class="text-emerald-400 font-extrabold text-lg">Gratis</span>
                <span v-else class="text-white font-extrabold text-lg">Bs {{ curso.precio }}</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { getCursos } from '../services/api'

export default {
  name: 'CursosView',
  data() {
    return {
      cursos: [],
      busqueda: '',
      nivel: 'Todos',
      precioFiltro: 'todos',
      totalGratis: 0
    }
  },
  async mounted() {
    await this.cargarCursos()
  },
  methods: {
    async cargarCursos() {
      const filters = {}
      if (this.busqueda) filters.search = this.busqueda
      if (this.nivel !== 'Todos') filters.nivel = this.nivel
      if (this.precioFiltro === 'gratis') filters.es_gratuito = true
      if (this.precioFiltro === 'pago') filters.es_gratuito = false

      try {
        const data = await getCursos(filters)
        this.cursos = data
        this.totalGratis = data.filter(c => c.es_gratuito).length
      } catch (err) {
        console.error("Error al cargar cursos:", err)
      }
    }
  }
}
</script>