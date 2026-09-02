<script setup>
import {
  ref,
  computed,
  onMounted
} from "vue"

import {
  BookOpen,
  Users,
  GraduationCap,
  Wallet,
  TrendingUp,
  Layers,
  Award
} from "lucide-vue-next"

import {
  Line,
  Bar,
  Doughnut
} from "vue-chartjs"

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Filler
} from "chart.js"

import KpiCard from "./KpiCard.vue"
import ReportCard from "./ReportCard.vue"

import {
  getCursosDashboard,
  getCursosFiltros
} from "../services/api"


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
  Filler
)


const colors = [
  "#5574E8",
  "#7651D8",
  "#D25896",
  "#EB9350",
  "#47B98A",
  "#52A6D8",
  "#D2A33E",
  "#8490E8"
]


const dashboard = ref(null)

const filterOptions = ref({
  niveles: [],
  tipos: [],
  cursos: []
})


const filters = ref({
  desde: "",
  hasta: "",
  nivel: "",
  es_gratuito: "",
  id_curso: ""
})


const loading = ref(false)

const error = ref(null)


function formatNumber(value) {
  return new Intl.NumberFormat(
    "es-BO"
  ).format(value || 0)
}


function formatMoney(value) {
  return `Bs. ${Number(
    value || 0
  ).toLocaleString(
    "es-BO",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }
  )}`
}


function buildFilters() {

  return {
    ...filters.value,

    es_gratuito:
      filters.value.es_gratuito === ""
        ? ""
        : filters.value.es_gratuito
  }
}


async function loadFilters() {

  try {

    filterOptions.value =
      await getCursosFiltros()

  } catch (err) {

    console.error(err)

  }
}


async function loadDashboard() {

  loading.value = true
  error.value = null

  try {

    dashboard.value =
      await getCursosDashboard(
        buildFilters()
      )

  } catch (err) {

    console.error(err)

    error.value =
      err.message ||
      "No se pudo cargar el reporte."

  } finally {

    loading.value = false

  }
}


async function applyFilters() {
  await loadDashboard()
}


async function clearFilters() {

  filters.value = {
    desde: "",
    hasta: "",
    nivel: "",
    es_gratuito: "",
    id_curso: ""
  }

  await loadDashboard()
}


const evolutionChart = computed(() => {

  const data =
    dashboard.value?.inscripciones_por_mes
    || []

  return {

    labels: data.map(
      item => item.periodo
    ),

    datasets: [
      {
        label: "Inscripciones",

        data: data.map(
          item => item.valor
        ),

        borderColor: "#5574E8",

        backgroundColor:
          "rgba(85, 116, 232, .10)",

        borderWidth: 3,

        tension: .35,

        fill: true,

        pointRadius: 3,

        pointHoverRadius: 6
      }
    ]
  }
})


const coursesChart = computed(() => {

  const data =
    dashboard.value?.por_curso
    ?.slice(0, 10)
    || []

  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [
      {
        data: data.map(
          item => item.cantidad
        ),

        backgroundColor:
          colors.slice(0, data.length),

        borderRadius: 7,

        borderSkipped: false
      }
    ]
  }
})


const revenueChart = computed(() => {

  const data =
    dashboard.value?.ingresos_por_curso
    ?.slice(0, 8)
    || []

  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [
      {
        data: data.map(
          item => item.ingresos
        ),

        backgroundColor:
          colors.slice(0, data.length),

        borderRadius: 7,

        borderSkipped: false
      }
    ]
  }
})


const typeChart = computed(() => {

  const data =
    dashboard.value?.gratuito_vs_premium
    || []

  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [
      {
        data: data.map(
          item => item.cantidad
        ),

        backgroundColor:
          [
            "#5574E8",
            "#7651D8"
          ],

        borderColor: "#ffffff",

        borderWidth: 3,

        hoverOffset: 7
      }
    ]
  }
})


const levelChart = computed(() => {

  const data =
    dashboard.value?.por_nivel
    || []

  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [
      {
        data: data.map(
          item => item.cantidad
        ),

        backgroundColor:
          colors.slice(0, data.length),

        borderRadius: 7,

        borderSkipped: false
      }
    ]
  }
})


const progressChart = computed(() => {

  const data =
    dashboard.value?.progreso_estudiantes
    || []

  return {

    labels: data.map(
      item => item.rango
    ),

    datasets: [
      {
        data: data.map(
          item => item.cantidad
        ),

        backgroundColor:
          colors.slice(0, data.length),

        borderRadius: 7,

        borderSkipped: false
      }
    ]
  }
})


const lineOptions = {

  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false
    }
  },

  scales: {
    x: {
      grid: {
        display: false
      }
    },

    y: {
      beginAtZero: true,

      grid: {
        color: "#edf0f6"
      }
    }
  }
}


const barOptions = {
  ...lineOptions
}


const doughnutOptions = {

  responsive: true,

  maintainAspectRatio: false,

  cutout: "64%",

  plugins: {

    legend: {
      position: "bottom"
    }
  }
}


onMounted(async () => {

  await loadFilters()

  await loadDashboard()

})
</script>


<template>

  <div class="business-dashboard">

    <!-- HEADER -->

    <div class="business-intro">

      <div>

        <div class="business-kicker">
          NEXBYTE ACADEMY
        </div>

        <h2>
          Academia y Formación
        </h2>

        <p>
          Analiza cómo los estudiantes descubren,
          consumen y completan nuestros cursos.
        </p>

      </div>

      <BookOpen
        :size="35"
        class="business-header-icon"
      />

    </div>


    <!-- FILTROS -->

    <section class="filters-card">

      <div class="filters-grid">

        <label class="filter-field">

          <span>
            Desde
          </span>

          <input
            type="datetime-local"
            v-model="filters.desde"
          />

        </label>


        <label class="filter-field">

          <span>
            Hasta
          </span>

          <input
            type="datetime-local"
            v-model="filters.hasta"
          />

        </label>


        <label class="filter-field">

          <span>
            Nivel
          </span>

          <select
            v-model="filters.nivel"
          >

            <option value="">
              Todos
            </option>

            <option
              v-for="nivel in filterOptions.niveles"
              :key="nivel"
              :value="nivel"
            >
              {{ nivel }}
            </option>

          </select>

        </label>


        <label class="filter-field">

          <span>
            Modalidad
          </span>

          <select
            v-model="filters.es_gratuito"
          >

            <option value="">
              Todas
            </option>

            <option
              value="true"
            >
              Gratuitos
            </option>

            <option
              value="false"
            >
              Premium
            </option>

          </select>

        </label>

      </div>


      <div class="filter-actions">

        <button
          class="button secondary"
          @click="clearFilters"
        >
          Limpiar
        </button>

        <button
          class="button primary"
          @click="applyFilters"
        >
          Aplicar filtros
        </button>

      </div>

    </section>


    <!-- ERROR -->

    <div
      v-if="error"
      class="state-card error-state"
    >

      {{ error }}

    </div>


    <!-- LOADING -->

    <div
      v-else-if="loading"
      class="state-card"
    >

      <div class="spinner"></div>

      Cargando Academia...

    </div>


    <template
      v-else-if="dashboard"
    >

      <!-- KPI -->

      <section class="kpi-grid">

        <KpiCard
          title="Cursos activos"
          :value="
            formatNumber(
              dashboard.kpis.cursos_activos
            )
          "
          subtitle="Catálogo disponible"
          :icon="BookOpen"
        />

        <KpiCard
          title="Estudiantes"
          :value="
            formatNumber(
              dashboard.kpis.estudiantes_inscritos
            )
          "
          subtitle="Alumnos inscritos"
          :icon="Users"
        />

        <KpiCard
          title="Completados"
          :value="
            formatNumber(
              dashboard.kpis
                .inscripciones_completadas
            )
          "
          subtitle="Formaciones terminadas"
          :icon="GraduationCap"
        />

        <KpiCard
          title="Ingresos"
          :value="
            formatMoney(
              dashboard.kpis
                .ingresos_registrados
            )
          "
          subtitle="Pagos registrados"
          :icon="Wallet"
        />

      </section>


      <!-- GRAFICOS -->

      <section class="reports-grid">

        <ReportCard
          title="Evolución de inscripciones"
          subtitle="Crecimiento de la Academia"
          span="full"
        >

          <div class="chart-lg">

            <Line
              :data="evolutionChart"
              :options="lineOptions"
            />

          </div>

        </ReportCard>


        <ReportCard
          title="Cursos más populares"
          subtitle="Por cantidad de inscripciones"
        >

          <div class="chart-md">

            <Bar
              :data="coursesChart"
              :options="barOptions"
            />

          </div>

        </ReportCard>


        <ReportCard
          title="Ingresos por curso"
          subtitle="Cursos con mayor aportación"
        >

          <div class="chart-md">

            <Bar
              :data="revenueChart"
              :options="barOptions"
            />

          </div>

        </ReportCard>


        <ReportCard
          title="Modelo de Academia"
          subtitle="Gratuito vs Premium"
        >

          <div class="chart-md">

            <Doughnut
              :data="typeChart"
              :options="doughnutOptions"
            />

          </div>

        </ReportCard>


        <ReportCard
          title="Demanda por nivel"
          subtitle="Dónde está concentrado el aprendizaje"
        >

          <div class="chart-md">

            <Bar
              :data="levelChart"
              :options="barOptions"
            />

          </div>

        </ReportCard>


        <ReportCard
          title="Progreso de estudiantes"
          subtitle="Avance dentro de las formaciones"
          span="full"
        >

          <div class="chart-md">

            <Bar
              :data="progressChart"
              :options="barOptions"
            />

          </div>

        </ReportCard>

      </section>

    </template>

  </div>

</template>


<style scoped>

.business-dashboard {
  width: 100%;
}


.business-intro {
  display: flex;

  justify-content: space-between;

  align-items: center;

  margin-bottom: 22px;

  padding:
    4px 2px;
}


.business-kicker {
  color: #6f58d9;

  font-size: 10px;

  font-weight: 800;

  letter-spacing: .13em;
}


.business-intro h2 {
  margin: 5px 0 0;

  font-size: 26px;

  letter-spacing: -.035em;

  color: #1d2536;
}


.business-intro p {
  margin: 7px 0 0;

  color: #949bad;

  font-size: 12px;
}


.business-header-icon {
  color: #6954d5;

  padding: 9px;

  width: 50px;
  height: 50px;

  border-radius: 15px;

  background:
    linear-gradient(
      135deg,
      #eef1ff,
      #f7edff
    );
}

</style>