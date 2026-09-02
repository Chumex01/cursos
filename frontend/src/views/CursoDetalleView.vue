<template>
  <div v-if="curso" class="bg-[#0b0f19] text-white min-h-screen">
    <div class="bg-[#121829] py-10 px-6 border-b border-slate-800">
      <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
        <div class="md:col-span-2">
          <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs px-2.5 py-0.5 rounded-full font-medium">
            {{ curso.nivel }}
          </span>
          <h1 class="text-3xl font-extrabold mt-3">{{ curso.titulo }}</h1>
          <p class="text-slate-300 mt-2">{{ curso.descripcion }}</p>
          <div class="flex items-center gap-4 mt-4 text-sm text-slate-400">
            <span>★ 4.5 (1,876 estudiantes)</span>
            <span>⏱ {{ totalHoras }} horas</span>
            <span>📚 {{ curso.lecciones?.length || 0 }} lecciones</span>
          </div>
        </div>

        <div class="bg-[#1e293b] p-6 rounded-xl border border-slate-700 text-center">
          <img :src="curso.imagen_principal_url" class="rounded-lg mb-4 w-full h-40 object-cover" />
          <div class="text-3xl font-black text-white mb-4">
            {{ curso.es_gratuito ? 'Gratis' : `Bs ${curso.precio}` }}
          </div>
          <button @click="procesarAccion" class="w-full bg-orange-600 hover:bg-orange-500 font-bold py-3 rounded-lg transition">
            {{ curso.es_gratuito ? 'Empezar gratis' : 'Adquirir curso' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Contenido y Lecciones -->
    <main class="max-w-6xl mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="md:col-span-2 space-y-8">
        <section class="bg-[#121829] p-6 rounded-xl border border-slate-800">
          <h2 class="text-xl font-bold mb-4">Contenido del curso</h2>
          <div class="space-y-3">
            <div v-for="leccion in curso.lecciones" :key="leccion.id_leccion" class="flex justify-between items-center p-3 bg-[#1e293b] rounded-lg">
              <div class="flex items-center gap-3">
                <span class="text-slate-400 font-mono text-sm">{{ leccion.orden }}.</span>
                <span>{{ leccion.titulo }}</span>
                <span v-if="leccion.es_preview" class="text-xs bg-indigo-900 text-indigo-300 px-2 py-0.5 rounded">Vista previa</span>
              </div>
              <span class="text-xs text-slate-400">{{ leccion.duracion_minutos }} min</span>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import { getCursoBySlug, inscribirCursoGratis } from '../services/api'

export default {
  name: 'CursoDetalleView',
  data() {
    return { curso: null }
  },
  computed: {
    totalHoras() {
      if (!this.curso?.lecciones) return 0
      const min = this.curso.lecciones.reduce((acc, l) => acc + l.duracion_minutos, 0)
      return (min / 60).toFixed(1)
    }
  },
  async mounted() {
    const slug = this.$route.params.slug
    this.curso = await getCursoBySlug(slug)
  },
  methods: {
    async procesarAccion() {
      if (this.curso.es_gratuito) {
        await inscribirCursoGratis(this.curso.id_curso, { id_estudiante: 1 })
        this.$router.push(`/aula/${this.curso.slug}`)
      } else {
        this.$router.push(`/checkout/${this.curso.slug}`)
      }
    }
  }
}
</script>