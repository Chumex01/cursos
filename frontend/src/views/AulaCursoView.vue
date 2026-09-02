<template>
  <div v-if="curso" class="bg-[#0b0f19] text-white min-h-screen flex flex-col">
    <header class="bg-[#121829] px-6 py-4 border-b border-slate-800 flex justify-between items-center">
      <router-link to="/cursos" class="text-slate-400 hover:text-white text-sm">← Volver</router-link>
      <h1 class="font-bold text-lg">{{ curso.titulo }}</h1>
      <span class="text-xs bg-indigo-900 text-indigo-300 px-3 py-1 rounded-full">{{ progresoGeneral }}% Completado</span>
    </header>

    <div class="flex-1 flex flex-col md:flex-row">
      <!-- Sidebar Lecciones -->
      <aside class="w-full md:w-80 bg-[#121829] border-r border-slate-800 p-4 space-y-2">
        <h3 class="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Contenido</h3>
        <button
          v-for="leccion in curso.lecciones" :key="leccion.id_leccion"
          @click="seleccionarLeccion(leccion)"
          :class="[leccionActual?.id_leccion === leccion.id_leccion ? 'bg-indigo-600 text-white' : 'hover:bg-slate-800 text-slate-300']"
          class="w-full text-left p-3 rounded-lg text-sm flex items-center justify-between transition">
          <span class="truncate">{{ leccion.orden }}. {{ leccion.titulo }}</span>
          <span class="text-xs opacity-75">{{ leccion.duracion_minutos }}m</span>
        </button>
      </aside>

      <!-- Panel Contenido -->
      <main class="flex-1 p-8 bg-[#0b0f19] max-w-4xl">
        <div v-if="leccionActual" class="space-y-6">
          <h2 class="text-2xl font-extrabold">{{ leccionActual.titulo }}</h2>
          <div class="bg-[#121829] p-6 rounded-xl border border-slate-800 text-slate-300 leading-relaxed">
            {{ leccionActual.contenido }}
          </div>
          <button @click="completarLeccion" class="bg-indigo-600 hover:bg-indigo-500 font-bold px-6 py-3 rounded-lg">
            Marcar como completada y continuar →
          </button>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { getCursoBySlug, actualizarProgresoLeccion } from '../services/api'

export default {
  name: 'AulaCursoView',
  data() {
    return {
      curso: null,
      leccionActual: null,
      completadas: new Set()
    }
  },
  computed: {
    progresoGeneral() {
      if (!this.curso?.lecciones?.length) return 0
      return Math.round((this.completadas.size / this.curso.lecciones.length) * 100)
    }
  },
  async mounted() {
    this.curso = await getCursoBySlug(this.$route.params.slug)
    if (this.curso?.lecciones?.length) {
      this.leccionActual = this.curso.lecciones[0]
    }
  },
  methods: {
    seleccionarLeccion(leccion) {
      this.leccionActual = leccion
    },
    async completarLeccion() {
      if (!this.leccionActual) return
      this.completadas.add(this.leccionActual.id_leccion)
      
      try {
        await actualizarProgresoLeccion(1, this.leccionActual.id_leccion, 100)
      } catch (e) {
        console.error(e)
      }

      const index = this.curso.lecciones.findIndex(l => l.id_leccion === this.leccionActual.id_leccion)
      if (index < this.curso.lecciones.length - 1) {
        this.leccionActual = this.curso.lecciones[index + 1]
      }
    }
  }
}
</script>