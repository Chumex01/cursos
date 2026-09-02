<template>

    <nav class="fixed top-0 w-full z-50 bg-[#0f172a]/90 backdrop-blur-md border-b border-slate-800">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-extrabold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">Hello World</router-link>
        <div class="hidden md:flex gap-8 text-sm font-medium text-slate-400">
          <router-link to="/servicios" class="hover:text-white transition">Servicios</router-link>
          <router-link to="/portafolio" class="hover:text-white transition">Portafolio</router-link>
        </div>
        <router-link to="/servicios" class="bg-violet-600 hover:bg-violet-700 text-white px-5 py-2 rounded-lg text-sm font-bold transition">Cotizar</router-link>
                  <router-link to="/cursos" class="hover:text-white transition">Cursos</router-link>
      </div>
    </nav>

  <div class="pt-28 pb-24 px-6 min-h-screen bg-[#0f172a]">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-12">
        <p class="text-violet-400 font-bold mb-2 tracking-widest uppercase text-sm">Portafolio</p>
        <h2 class="text-5xl font-extrabold mb-6">Nuestro Trabajo</h2>
        <p class="text-slate-400 max-w-2xl mx-auto">Explora nuestros proyectos y filtros por tecnología o categoría.</p>
      </div>

      <!-- BUSCADOR Y FILTROS -->
      <div class="mb-16 bg-[#1e293b] rounded-2xl p-6 border border-slate-800 shadow-lg">
        <div class="flex flex-col md:flex-row gap-6">
          <!-- Input de Búsqueda -->
          <div class="flex-1 relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
            <input 
              v-model="busqueda" 
              type="text" 
              placeholder="Buscar proyecto por nombre..." 
              class="w-full bg-slate-900 border border-slate-700 rounded-xl pl-12 pr-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 transition"
            >
          </div>
          <!-- Filtros de Categoría -->
          <div class="flex flex-wrap gap-3 items-center">
            <button @click="filtroActual = null" :class="filtroActual === null ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/30' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'" class="px-5 py-3.5 rounded-xl text-sm font-bold transition">Todos</button>
            <button v-for="cat in categoriasUnicas" :key="cat" @click="filtroActual = cat" :class="filtroActual === cat ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/30' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'" class="px-5 py-3.5 rounded-xl text-sm font-bold transition">
              {{ cat }}
            </button>
          </div>
        </div>
      </div>

      <!-- GRID -->
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="proy in proyectosFiltrados" :key="proy.id_proyecto" class="bg-[#1e293b] rounded-2xl border border-slate-800 overflow-hidden group hover:border-violet-500/50 transition-all hover:-translate-y-1">
          <div class="bg-slate-900 p-4 h-56 relative">
            <div class="w-full h-full bg-[#0d1117] rounded-lg p-4 font-mono text-xs text-slate-500 border border-slate-800 overflow-hidden relative">
              <p class="text-violet-400">import</p> <span class="text-cyan-300">{{ proy.tecnologias[0]?.nombre || 'tech' }}</span> <span class="text-violet-400">from</span> <span class="text-green-400">'./lib'</span>;<br><br>
              <span class="text-slate-600">// {{ proy.titulo }}</span>
              <div class="absolute bottom-2 right-2 flex gap-1.5"><div class="w-2.5 h-5 bg-slate-700 rounded-sm"></div><div class="w-2.5 h-5 bg-slate-700 rounded-sm"></div><div class="w-2.5 h-5 bg-slate-700 rounded-sm"></div></div>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-bold text-white mb-2">{{ proy.titulo }}</h3>
            <p class="text-slate-400 text-sm mb-4 line-clamp-2">{{ proy.descripcion_corta }}</p>
            <div class="flex flex-wrap gap-2 mb-6">
              <span v-for="tech in proy.tecnologias" :key="tech.nombre" class="bg-slate-700/50 text-slate-300 text-xs px-2.5 py-1 rounded-full font-medium">{{ tech.nombre }}</span>
            </div>
            <div class="flex gap-3 border-t border-slate-700 pt-4">
              <a v-if="proy.url_demo" :href="proy.url_demo" target="_blank" class="text-sm text-violet-400 hover:text-violet-300 font-bold transition">Ver Demo →</a>
              <a v-if="proy.url_github" :href="proy.url_github" target="_blank" class="text-sm text-slate-500 hover:text-slate-300 font-bold transition">GitHub</a>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Estado vacío -->
      <div v-if="proyectosFiltrados.length === 0" class="text-center py-20">
        <p class="text-6xl mb-4">🔍</p>
        <p class="text-slate-500 text-xl">No se encontraron proyectos para "{{ busqueda || filtroActual }}"</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const API_URL = 'http://localhost:8000/public';
const proyectos = ref([]);
const filtroActual = ref(null);
const busqueda = ref('');

const proyectosFiltrados = computed(() => {
  let resultado = proyectos.value;
  
  // Filtro por texto
  if (busqueda.value) {
    const texto = busqueda.value.toLowerCase();
    resultado = resultado.filter(p => 
      p.titulo.toLowerCase().includes(texto) || 
      p.descripcion_corta.toLowerCase().includes(texto) ||
      p.tecnologias.some(t => t.nombre.toLowerCase().includes(texto))
    );
  }
  
  // Filtro por categoría
  if (filtroActual.value) {
    resultado = resultado.filter(p => p.tecnologias.some(t => t.categoria === filtroActual.value));
  }
  
  return resultado;
});

const categoriasUnicas = computed(() => {
  const cats = new Set(proyectos.value.flatMap(p => p.tecnologias.map(t => t.categoria)));
  return Array.from(cats);
});

onMounted(async () => {
  const res = await fetch(`${API_URL}/proyectos/todos`);
  proyectos.value = await res.json();
});
</script>

<style>
@import '../tailwind.css';
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>