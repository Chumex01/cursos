<template>
    <div>
        <!-- NAVBAR LIMPIO -->
        <nav class="fixed top-0 w-full z-50 bg-[#0f172a]/90 backdrop-blur-md border-b border-slate-800">
            <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                <router-link to="/"
                    class="text-2xl font-extrabold bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">Hello
                    World</router-link>
                <div class="hidden md:flex gap-8 text-sm font-medium text-slate-400">
                    <router-link to="/servicios" class="hover:text-white transition">Servicios</router-link>
                    <router-link to="/portafolio" class="hover:text-white transition">Portafolio</router-link>
                </div>
                <router-link to="/servicios"
                    class="bg-violet-600 hover:bg-violet-700 text-white px-5 py-2 rounded-lg text-sm font-bold transition">Cotizar</router-link>
                              <router-link to="/cursos" class="hover:text-white transition">Cursos</router-link>
            </div>
        </nav>

        <!-- HERO IMPACTANTE -->
        <section class="pt-36 pb-24 px-6 relative overflow-hidden">
            <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(139,92,246,0.15),transparent_60%)]">
            </div>
            <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-16 items-center relative z-10">
                <div>
                    <span
                        class="inline-block bg-violet-500/20 text-violet-300 font-bold px-4 py-1.5 rounded-full text-sm mb-6 tracking-wider">TECNOLOGÍA
                        & DESARROLLO</span>
                    <h1 class="text-6xl md:text-7xl font-extrabold leading-tight mb-8">
                        Impulsamos tu negocio con <span
                            class="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-400 bg-clip-text text-transparent">tecnología
                            real.</span>
                    </h1>
                    <p class="text-xl text-slate-400 mb-12 max-w-lg leading-relaxed">Software a medida, aplicaciones
                        móviles y consultoría técnica para empresas en Bolivia y la región.</p>
                    <div class="flex flex-col sm:flex-row gap-4">
                        <router-link to="/servicios"
                            class="bg-violet-600 hover:bg-violet-700 text-white px-10 py-4 rounded-xl font-bold text-lg transition shadow-xl shadow-violet-600/20 text-center">
                            Ver Servicios →
                        </router-link>
                        <router-link to="/portafolio"
                            class="border-2 border-slate-600 hover:border-white text-slate-300 hover:text-white px-10 py-4 rounded-xl font-bold text-lg transition text-center">
                            Nuestro Trabajo
                        </router-link>
                    </div>
                </div>
                <!-- Visual Hero -->
                <div class="hidden md:flex justify-center relative">
                    <div
                        class="w-full max-w-lg bg-slate-900 rounded-t-xl border-t-4 border-violet-500 p-5 shadow-2xl shadow-violet-900/30">
                        <div
                            class="bg-[#1e293b] rounded-lg p-6 font-mono text-sm text-green-400 h-72 overflow-hidden relative">
                            <span class="text-slate-500">import</span> { <span class="text-cyan-300">Project</span> }
                            <span class="text-violet-400">from</span> <span
                                class="text-yellow-300">'@hw/core'</span>;<br><br>
                            <span class="text-violet-400">const</span> <span class="text-blue-300">app</span> = <span
                                class="text-yellow-300">new</span> <span class="text-blue-300">Project</span>();<br>
                            <span class="text-slate-500">await</span> app.<span
                                class="text-cyan-300">deploy()</span>;<br><br>
                            <span class="text-green-300">// Status: Active ✅</span><br>
                            <span class="text-green-300">// Uptime: 99.9%</span>
                            <div class="absolute bottom-0 right-4 w-3 h-5 bg-slate-400 animate-pulse"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- BARRA DE ESTADÍSTICAS (La que pediste conservar) -->
        <div class="bg-slate-900/50 border-y border-slate-800 py-10">
            <div class="max-w-5xl mx-auto grid grid-cols-3 gap-10 text-center px-6">
                <div>
                    <p class="text-5xl font-extrabold text-white">+{{ stats.total_estudiantes || '...' }}</p>
                    <p class="text-sm text-slate-400 mt-2 uppercase tracking-widest font-semibold">Estudiantes activos
                    </p>
                </div>
                <div>
                    <p class="text-5xl font-extrabold text-white">{{ stats.total_cursos || '...' }}</p>
                    <p class="text-sm text-slate-400 mt-2 uppercase tracking-widest font-semibold">Cursos disponibles
                    </p>
                </div>
                <div>
                    <p class="text-5xl font-extrabold text-white">+{{ stats.total_proyectos || '...' }}</p>
                    <p class="text-sm text-slate-400 mt-2 uppercase tracking-widest font-semibold">Proyectos entregados
                    </p>
                </div>
            </div>
        </div>

        <!-- PREVIEW DE SERVICIOS (Solo 3 + Botón) -->
        <section class="py-24 px-6">
            <div class="max-w-7xl mx-auto flex justify-between items-end mb-16">
                <div>
                    <p class="text-violet-400 font-bold mb-2 tracking-widest uppercase text-sm">¿Qué hacemos?</p>
                    <h2 class="text-4xl font-extrabold">Servicios Principales</h2>
                </div>
                <router-link to="/servicios"
                    class="hidden md:block text-violet-400 hover:text-violet-300 font-bold text-lg transition group">
                    Ver todos los servicios
                    <span class="inline-block ml-2 group-hover:translate-x-1 transition-transform">→</span>
                </router-link>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <div v-for="serv in servicios" :key="serv.id_servicio"
                    class="bg-[#1e293b] border border-slate-800 rounded-2xl p-8 hover:border-violet-500/50 transition-all hover:-translate-y-1 group flex flex-col">
                    <div
                        class="w-14 h-14 bg-slate-800 group-hover:bg-violet-600 text-slate-400 group-hover:text-white rounded-xl flex items-center justify-center text-3xl mb-6 transition-all duration-300">
                        ⚙️</div>
                    <h3 class="text-xl font-bold text-white mb-3">{{ serv.nombre }}</h3>
                    <p class="text-slate-400 text-sm leading-relaxed flex-1 mb-6">{{ serv.descripcion.substring(0, 100)
                        }}...</p>
                    <div class="border-t border-slate-700 pt-6 mt-auto">
                        <p class="text-3xl font-extrabold text-white mb-1">{{ serv.moneda }} {{ serv.precio_base }}</p>
                        <p class="text-sm text-slate-500">Desde / {{ serv.carga_horaria }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CURSOS CON MAGIA -->
        <section class="py-24 px-6 bg-[#0b1120]">
            <div class="max-w-7xl mx-auto flex justify-between items-end mb-16">
                <div>
                    <p class="text-violet-400 font-bold mb-2 tracking-widest uppercase text-sm">Formación</p>
                    <h2 class="text-4xl font-extrabold">Aprende a tu ritmo</h2>
                </div>
            </div>
            <div class="max-w-7xl mx-auto grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                <div v-for="curso in cursos" :key="curso.id_curso"
                    class="magic-card relative bg-[#1e293b] rounded-2xl overflow-hidden border border-slate-800 transition-all hover:-translate-y-2 flex flex-col group">
                    <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                        style="background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(139, 92, 246, 0.2), transparent 60%);">
                    </div>
                    <div :class="getCourseBgClass(curso.nivel)"
                        class="h-40 flex flex-col items-center justify-center relative">
                        <span class="text-5xl mb-2 relative z-10">{{ getCourseIcon(curso.nivel) }}</span>
                        <span :class="getCourseBadgeClass(curso.nivel)"
                            class="absolute top-4 right-4 text-xs font-bold px-3 py-1 rounded-full z-10">
                            {{ curso.es_gratuito ? 'GRATIS' : curso.moneda + ' ' + curso.precio }}
                        </span>
                    </div>
                    <div class="p-5 flex flex-col flex-1 relative z-10">
                        <span
                            class="text-xs font-bold uppercase px-2 py-1 rounded bg-slate-700/50 text-slate-300 w-fit mb-2">{{
                            curso.nivel }}</span>
                        <h3 class="text-lg font-bold mb-2 text-white leading-tight">{{ curso.titulo }}</h3>
                        <p class="text-slate-400 text-sm mb-4 flex-1 line-clamp-2">{{ curso.descripcion }}</p>
                        <p class="text-xs text-slate-500 mb-4">👨‍💻 {{ curso.total_estudiantes }} estudiantes</p>
                        <router-link :to="`/cursos/${curso.slug}`"
                            class="w-full bg-slate-700 group-hover:bg-violet-600 text-white py-2.5 rounded-lg font-bold text-sm transition mt-auto">
                            Ver Curso
                        </router-link>
                    </div>
                </div>
            </div>
        </section>

        <!-- PREVIEW PORTAFOLIO (Solo 3 + Botón) -->
        <section class="py-24 px-6">
            <div class="max-w-7xl mx-auto flex justify-between items-end mb-16">
                <div>
                    <p class="text-violet-400 font-bold mb-2 tracking-widest uppercase text-sm">Portafolio</p>
                    <h2 class="text-4xl font-extrabold">Casos de Éxito</h2>
                </div>
                <router-link to="/portafolio"
                    class="hidden md:block text-violet-400 hover:text-violet-300 font-bold text-lg transition group">
                    Ver todos los proyectos
                    <span class="inline-block ml-2 group-hover:translate-x-1 transition-transform">→</span>
                </router-link>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
                <div v-for="proy in proyectos" :key="proy.id_proyecto"
                    class="bg-[#1e293b] rounded-2xl border border-slate-800 overflow-hidden group hover:border-violet-500/50 transition-all">
                    <div class="bg-slate-900 p-4 h-48 relative">
                        <div
                            class="w-full h-full bg-[#0d1117] rounded-lg p-4 font-mono text-xs text-slate-500 border border-slate-800 overflow-hidden relative">
                            <p class="text-violet-400">import</p> <span class="text-cyan-300">{{
                                proy.tecnologias[0]?.nombre || 'tech' }}</span><br>
                            <span class="text-slate-600">// {{ proy.titulo }}</span>
                            <div class="absolute bottom-2 right-2 flex gap-1">
                                <div class="w-2 h-4 bg-slate-600 rounded-sm"></div>
                                <div class="w-2 h-4 bg-slate-600 rounded-sm"></div>
                                <div class="w-2 h-4 bg-slate-600 rounded-sm"></div>
                            </div>
                        </div>
                    </div>
                    <div class="p-6">
                        <h3 class="text-xl font-bold text-white mb-2">{{ proy.titulo }}</h3>
                        <div class="flex flex-wrap gap-2">
                            <span v-for="tech in proy.tecnologias.slice(0, 3)" :key="tech.nombre"
                                class="bg-slate-700/50 text-slate-300 text-xs px-2.5 py-1 rounded-full font-medium">{{
                                tech.nombre }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- FOOTER -->
        <footer class="bg-[#0b1120] border-t border-slate-800 py-20 px-6 text-center">
            <div class="max-w-2xl mx-auto">
                <p
                    class="text-4xl font-extrabold mb-6 bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">
                    ¿Tienes un proyecto en mente?</p>
                <p class="text-slate-400 mb-10 text-lg">Agenda una reunión gratuita de 15 minutos y te damos una
                    propuesta de valor sin compromiso.</p>
                <router-link to="/servicios"
                    class="inline-block bg-violet-600 hover:bg-violet-700 text-white px-12 py-5 rounded-xl font-bold text-xl transition shadow-2xl shadow-violet-600/30 hover:shadow-violet-600/50 transform hover:-translate-y-1">
                    Solicitar Cotización Ahora
                </router-link>
            </div>
            <p class="text-slate-600 text-sm mt-20">© 2024 Hello World. Todos los derechos reservados.</p>
        </footer>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const API_URL = 'http://localhost:8000/public';
const stats = ref({});
const servicios = ref([]);
const cursos = ref([]);
const proyectos = ref([]);

const getCourseBgClass = (n) => n === 'Básico' ? 'bg-gradient-to-br from-emerald-800 to-emerald-950' : n === 'Intermedio' ? 'bg-gradient-to-br from-blue-800 to-blue-950' : 'bg-gradient-to-br from-violet-800 to-violet-950';
const getCourseBadgeClass = (n) => n === 'Básico' ? 'bg-emerald-500 text-white' : n === 'Intermedio' ? 'bg-blue-500 text-white' : 'bg-violet-500 text-white';
const getCourseIcon = (n) => n === 'Básico' ? '🌱' : n === 'Intermedio' ? '🚀' : '🎯';

onMounted(async () => {
    const [resStats, resServ, resCursos, resProy] = await Promise.all([
        fetch(`${API_URL}/estadisticas`),
        fetch(`${API_URL}/servicios`), // Llama al que trae solo 3
        fetch(`${API_URL}/cursos`),
        fetch(`${API_URL}/proyectos`)  // Llama al que trae solo destacados
    ]);

    stats.value = await resStats.json();
    servicios.value = await resServ.json();
    cursos.value = await resCursos.json();
    proyectos.value = await resProy.json();

    const handleMouseMove = (e) => {
        document.querySelectorAll('.magic-card').forEach(card => {
            const rect = card.getBoundingClientRect();
            card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
            card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
        });
    };
    window.addEventListener('mousemove', handleMouseMove);
    onUnmounted(() => window.removeEventListener('mousemove', handleMouseMove));
});
</script>

<style>
@import '../tailwind.css';

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>