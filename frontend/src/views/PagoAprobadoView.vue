<template>
  <div class="bg-[#0b0f19] text-white min-h-screen flex items-center justify-center p-8">
    <div class="bg-[#121829] p-8 rounded-xl border border-slate-800 text-center max-w-md">
      <div class="text-emerald-400 text-5xl mb-4">✓</div>
      <h1 class="text-2xl font-bold mb-2">¡Pago Aprobado!</h1>
      <p class="text-slate-400 text-sm mb-6">Tu inscripción ha sido procesada con éxito.</p>
      <router-link to="/cursos" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-6 py-3 rounded-lg inline-block">
        Ir a Mis Cursos
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PagoAprobadoView'
}
</script>