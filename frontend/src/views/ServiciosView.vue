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

  <div class="min-h-screen bg-[#0f172a]">
    <!-- HEADER -->
    <div class="bg-gradient-to-br from-indigo-950 via-violet-900 to-slate-900 pt-32 pb-24 px-6 border-b border-slate-700/50">
      <div class="max-w-4xl mx-auto text-center">
        <span class="bg-violet-500/20 text-violet-300 text-sm font-bold px-5 py-1.5 rounded-full">SERVICIOS</span>
        <h1 class="text-5xl font-extrabold mt-8 mb-6">Soluciones digitales a tu medida</h1>
        <p class="text-xl text-slate-300 max-w-2xl mx-auto mb-4">Desarrollamos software, aplicaciones y sistemas diseñados específicamente para las necesidades de tu empresa.</p>
        <p class="text-violet-300 font-semibold text-lg">{{ serviciosFiltrados.length }} servicios disponibles</p>
      </div>
    </div>

    <!-- BUSCADOR Y FILTROS -->
    <div class="max-w-7xl mx-auto px-6 -mt-16 mb-16 relative z-10">
      <div class="bg-[#1e293b] rounded-2xl p-6 border border-slate-800 shadow-xl flex flex-col md:flex-row gap-6">
        <div class="flex-1 relative">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🔍</span>
          <input 
            v-model="busqueda" 
            type="text" 
            placeholder="Buscar servicio por nombre..." 
            class="w-full bg-slate-900 border border-slate-700 rounded-xl pl-14 pr-4 py-4 text-white placeholder-slate-500 focus:outline-none focus:border-violet-500 transition text-lg"
          >
        </div>
        <div class="flex flex-wrap gap-3 items-center">
          <button @click="filtroActual = null" :class="filtroActual === null ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/30' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'" class="px-6 py-4 rounded-xl text-sm font-bold transition">Todos</button>
          <button v-for="serv in categoriasUnicas" :key="serv" @click="filtroActual = serv" :class="filtroActual === serv ? 'bg-violet-600 text-white shadow-lg shadow-violet-600/30' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'" class="px-6 py-4 rounded-xl text-sm font-bold transition capitalize">
            {{ serv }}
          </button>
        </div>
      </div>
    </div>

    <!-- GRID DE SERVICIOS -->
    <div class="max-w-7xl mx-auto px-6 pb-24">
      <div class="grid md:grid-cols-2 gap-8">
        <div v-for="serv in serviciosFiltrados" :key="serv.id_servicio" class="bg-[#1e293b] rounded-3xl border border-slate-800 hover:border-violet-500/50 transition-all duration-300 overflow-hidden group flex flex-col shadow-lg hover:shadow-2xl hover:shadow-violet-900/10">
          <div class="bg-gradient-to-r from-violet-600/10 to-cyan-600/10 p-8 border-b border-slate-800">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 bg-slate-800 group-hover:bg-violet-600 text-slate-400 group-hover:text-white rounded-2xl flex items-center justify-center text-3xl transition-all duration-300 shadow-inner">⚙️</div>
              <div>
                <h3 class="text-2xl font-bold text-white group-hover:text-violet-300 transition-colors">{{ serv.nombre }}</h3>
                <p v-if="serv.carga_horaria" class="text-sm text-slate-400 mt-1">⏱ {{ serv.carga_horaria}}</p>
              </div>
            </div>
          </div>
          
          <div class="p-8 flex-1 flex flex-col">
            <p class="text-slate-400 leading-relaxed flex-1 mb-8 text-base">{{ serv.descripcion }}</p>
            
            <div class="mt-auto pt-6 border-t border-slate-700">
              <div class="flex justify-between items-end">
                <div>
                  <p class="text-xs text-slate-500 uppercase font-bold tracking-wider">Inversión inicial</p>
                  <p class="text-4xl font-extrabold text-white mt-1">{{ serv.moneda }} <span class="text-violet-400">{{ serv.precio_base }}</span></p>
                </div>
              </div>
              <button @click="abrirModal(serv)" class="w-full mt-8 bg-slate-800 hover:bg-violet-600 text-white py-4 rounded-xl font-bold text-base transition shadow-lg hover:shadow-violet-600/20 flex items-center justify-center gap-2">
                Solicitar cotización 
                <span class="group-hover:translate-x-1 transition-transform">→</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-if="serviciosFiltrados.length === 0" class="text-center py-24">
        <p class="text-6xl mb-4">🔍</p>
        <p class="text-slate-500 text-xl">No se encontraron servicios para "{{ busqueda || filtroActual }}"</p>
      </div>
    </div>

    <!-- MODAL DE CONTACTO -->
    <div v-if="modalAbierto" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm" @click.self="cerrarModal">
      <div class="bg-[#1e293b] border border-slate-700 rounded-2xl p-8 w-full max-w-lg shadow-2xl relative animate-fade-in">
        <button @click="cerrarModal" class="absolute top-4 right-4 text-slate-400 hover:text-white text-2xl">✕</button>
        <h3 class="text-2xl font-bold text-white mb-2">Solicitar Cotización</h3>
        <p class="text-slate-400 text-sm mb-6">Servicio: <span class="text-violet-400 font-semibold">{{ servicioSeleccionado?.nombre }}</span></p>
        
        <form @submit.prevent="enviarSolicitud" class="space-y-4">
          <div>
            <label class="text-sm text-slate-300 block mb-1">Nombre completo *</label>
            <input v-model="form.nombre" type="text" required class="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-violet-500 transition" placeholder="Juan Pérez">
          </div>
          <div>
            <label class="text-sm text-slate-300 block mb-1">Correo electrónico *</label>
            <input v-model="form.email" type="email" required class="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-violet-500 transition" placeholder="juan@empresa.com">
          </div>
          <div>
            <label class="text-sm text-slate-300 block mb-1">Empresa</label>
            <input v-model="form.empresa" type="text" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-violet-500 transition" placeholder="Mi Empresa S.A. (Opcional)">
          </div>
          <div>
            <label class="text-sm text-slate-300 block mb-1">Cuéntanos sobre tu proyecto *</label>
            <textarea v-model="form.mensaje" required rows="4" class="w-full bg-slate-900 border border-slate-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-violet-500 transition resize-none" placeholder="Necesitamos un sistema para..."></textarea>
          </div>
          
          <button type="submit" :disabled="enviando" class="w-full bg-violet-600 hover:bg-violet-700 disabled:bg-violet-800 text-white font-bold py-3.5 rounded-lg transition">
            {{ enviando ? 'Enviando...' : 'Enviar Solicitud por Correo' }}
          </button>
          <p v-if="mensajeExito" class="text-green-400 text-sm text-center mt-3 font-semibold">✅ {{ mensajeExito }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const API_URL = 'http://localhost:8000/public';
const servicios = ref([]);
const filtroActual = ref(null);
const busqueda = ref('');
const modalAbierto = ref(false);
const servicioSeleccionado = ref(null);
const enviando = ref(false);
const mensajeExito = ref('');
const form = ref({ nombre: '', email: '', empresa: '', mensaje: '' });

// Lógica de Filtros y Búsqueda
const serviciosFiltrados = computed(() => {
  let resultado = servicios.value;
  
  if (busqueda.value) {
    const texto = busqueda.value.toLowerCase();
    resultado = resultado.filter(s => s.nombre.toLowerCase().includes(texto) || s.descripcion.toLowerCase().includes(texto));
  }
  
  if (filtroActual.value) {
    resultado = resultado.filter(s => s.nombre.toLowerCase().includes(filtroActual.value.toLowerCase()));
  }
  
  return resultado;
});

// Extraer categorías únicas (en este caso, como no hay tabla de categorías, sacamos la primera palabra del nombre)
const categoriasUnicas = computed(() => {
  const palabras = new Set(servicios.value.map(s => s.nombre.split(' ')[0]));
  return Array.from(palabras);
});

const abrirModal = (serv) => {
  servicioSeleccionado.value = serv;
  form.value.mensaje = `Hola, estoy interesado/a en el servicio de "${serv.nombre}". Me gustaría obtener más información y una cotización detallada.`;
  modalAbierto.value = true;
};
const cerrarModal = () => { modalAbierto.value = false; mensajeExito.value = ''; };

const enviarSolicitud = async () => {
  enviando.value = true;
  try {
    const res = await fetch(`${API_URL}/contacto/servicio`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form.value, servicio_solicitado: servicioSeleccionado.value.nombre })
    });
    const data = await res.json();
    if (res.ok) { mensajeExito.value = data.mensaje; setTimeout(cerrarModal, 2500); }
    else { alert('Error: ' + data.detail); }
  } catch { alert('Error de conexión con el servidor'); }
  finally { enviando.value = false; }
};

onMounted(async () => {
  const res = await fetch(`${API_URL}/servicios/todos`);
  servicios.value = await res.json();
});
</script>

<style>
@import '../tailwind.css';
@keyframes fade-in { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.animate-fade-in { animation: fade-in 0.3s ease-out; }
</style>