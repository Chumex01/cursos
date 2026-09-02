<script setup>
import {
  ref,
  computed,
  onMounted,
  watch,
  markRaw
} from "vue"

import {
  ShieldCheck,
  Megaphone,
  MousePointerClick,
  Users,
  Activity,
  CalendarDays,
  Database,
  Globe,
  MousePointer,
  BarChart3,
  UserPlus,
  BookOpen,
  BriefcaseBusiness,
  TrendingUp
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

import CursosDashboard from "./CursosDashboard.vue"
import ServiciosDashboard from "./ServiciosDashboard.vue"

import {
  getAuditoriaDashboard,
  getFuentesDashboard,
  getEventosDashboard,
  getVisitantesDashboard,
  getSesionesDashboard,

  getAuditoriaFiltros,
  getFuentesFiltros,
  getEventosFiltros,
  getVisitantesFiltros,
  getSesionesFiltros
} from "../services/api"


// ============================================================
// CHART.JS
// ============================================================

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

ChartJS.defaults.font.family =
  "Inter, ui-sans-serif, system-ui, sans-serif"

ChartJS.defaults.color = "#7d8497"

ChartJS.defaults.borderColor = "#edf0f6"

ChartJS.defaults.elements.line.borderWidth = 3

ChartJS.defaults.elements.point.radius = 3

ChartJS.defaults.elements.point.hoverRadius = 5


// ============================================================
// COLORES
// ============================================================

const chartColors = [
  "#5574E8",
  "#7651D8",
  "#D25896",
  "#EB9350",
  "#47B98A",
  "#52A6D8",
  "#D2A33E",
  "#8490E8"
]


// ============================================================
// REPORTES
// ============================================================

const reports = [

  // ----------------------------------------------------------
  // ANALÍTICA
  // ----------------------------------------------------------

  {
    id: "auditoria",
    section: "ANALÍTICA",
    name: "Auditoría",
    description: "Actividad administrativa",
    icon: markRaw(ShieldCheck)
  },

  {
    id: "fuentes",
    section: "ANALÍTICA",
    name: "Fuentes de tráfico",
    description: "Origen de visitantes",
    icon: markRaw(Megaphone)
  },

  {
    id: "eventos",
    section: "ANALÍTICA",
    name: "Eventos",
    description: "Comportamiento",
    icon: markRaw(MousePointerClick)
  },

  {
    id: "visitantes",
    section: "ANALÍTICA",
    name: "Visitantes",
    description: "Audiencia",
    icon: markRaw(Users)
  },

  {
    id: "sesiones",
    section: "ANALÍTICA",
    name: "Sesiones",
    description: "Navegación",
    icon: markRaw(Activity)
  },


  // ----------------------------------------------------------
  // NEGOCIO
  // ----------------------------------------------------------

  {
    id: "cursos",
    section: "NEGOCIO",
    name: "Academia / Cursos",
    description: "Formación y aprendizaje",
    icon: markRaw(BookOpen)
  },
]


// ============================================================
// ESTADO
// ============================================================

const activeReport = ref("visitantes")

const loading = ref(false)

const error = ref(null)

const dashboard = ref(null)

const filterOptions = ref(null)


// ============================================================
// REPORTES DE NEGOCIO
// ============================================================

const businessReports = [
  "cursos",
  "servicios"
]


const isBusinessReport = computed(() => {
  return businessReports.includes(
    activeReport.value
  )
})


// ============================================================
// FILTROS
// ============================================================

const filters = ref({
  desde: "",
  hasta: ""
})


const extraFilters = ref({})


// ============================================================
// REPORTE ACTUAL
// ============================================================

const currentReport = computed(() => {

  return reports.find(
    report =>
      report.id === activeReport.value
  )

})


const reportTitle = computed(() => {

  return currentReport.value?.name ||
    "Dashboard"

})


const reportDescription = computed(() => {

  return currentReport.value?.description ||
    ""

})


// ============================================================
// FORMATO
// ============================================================

function formatNumber(value) {

  if (
    value === null ||
    value === undefined
  ) {
    return "0"
  }

  return new Intl.NumberFormat(
    "es-BO"
  ).format(value)

}


function formatDecimal(value) {

  return Number(
    value || 0
  ).toLocaleString(
    "es-BO",
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }
  )

}


function formatSeconds(seconds) {

  const total = Math.round(
    Number(seconds || 0)
  )

  const minutes = Math.floor(
    total / 60
  )

  const secs = total % 60

  return `${minutes}m ${secs}s`

}


// ============================================================
// API
// ============================================================

async function loadDashboard() {

  if (isBusinessReport.value) {
    return
  }

  loading.value = true

  error.value = null

  dashboard.value = null

  try {

    const params = {
      ...filters.value,
      ...extraFilters.value
    }

    switch (activeReport.value) {

      case "auditoria":

        dashboard.value =
          await getAuditoriaDashboard(
            params
          )

        break


      case "fuentes":

        dashboard.value =
          await getFuentesDashboard(
            params
          )

        break


      case "eventos":

        dashboard.value =
          await getEventosDashboard(
            params
          )

        break


      case "visitantes":

        dashboard.value =
          await getVisitantesDashboard(
            params
          )

        break


      case "sesiones":

        dashboard.value =
          await getSesionesDashboard(
            params
          )

        break

    }

  } catch (err) {

    console.error(
      "Error cargando dashboard:",
      err
    )

    error.value =
      err?.message ||
      "No se pudo cargar el dashboard."

  } finally {

    loading.value = false

  }

}


// ============================================================
// FILTROS
// ============================================================

async function loadFilters() {

  if (isBusinessReport.value) {
    filterOptions.value = null
    return
  }

  try {

    switch (activeReport.value) {

      case "auditoria":

        filterOptions.value =
          await getAuditoriaFiltros()

        break


      case "fuentes":

        filterOptions.value =
          await getFuentesFiltros()

        break


      case "eventos":

        filterOptions.value =
          await getEventosFiltros()

        break


      case "visitantes":

        filterOptions.value =
          await getVisitantesFiltros()

        break


      case "sesiones":

        filterOptions.value =
          await getSesionesFiltros()

        break

    }

  } catch (err) {

    console.error(
      "No se pudieron cargar los filtros:",
      err
    )

    filterOptions.value = null

  }

}


// ============================================================
// CAMBIAR REPORTES
// ============================================================

async function changeReport(reportId) {

  if (
    reportId ===
    activeReport.value
  ) {
    return
  }

  activeReport.value = reportId

  extraFilters.value = {}

  dashboard.value = null

  error.value = null

  filterOptions.value = null


  if (
    businessReports.includes(
      reportId
    )
  ) {
    return
  }

  await loadFilters()

  await loadDashboard()

}


// ============================================================
// FILTROS
// ============================================================

async function applyFilters() {

  if (isBusinessReport.value) {
    return
  }

  await loadDashboard()

}


async function clearFilters() {

  filters.value = {
    desde: "",
    hasta: ""
  }

  extraFilters.value = {}

  if (
    isBusinessReport.value
  ) {
    return
  }

  await loadDashboard()

}


// ============================================================
// CHART HELPERS
// ============================================================

function chartLabels(items = []) {

  return items.map(
    item => item.nombre
  )

}


function chartValues(
  items = [],
  key = "valor"
) {

  return items.map(
    item => item[key]
  )

}


// ============================================================
// CHART OPTIONS
// ============================================================

const chartOptions = {

  responsive: true,

  maintainAspectRatio: false,

  interaction: {
    intersect: false,
    mode: "index"
  },

  plugins: {

    legend: {
      display: false
    },

    tooltip: {
      backgroundColor: "#20283a",

      padding: 11,

      titleFont: {
        size: 11,
        weight: "700"
      },

      bodyFont: {
        size: 11
      },

      cornerRadius: 9
    }

  },

  scales: {

    x: {

      grid: {
        display: false
      },

      ticks: {
        font: {
          size: 9
        },

        color: "#9aa1b2"
      }

    },

    y: {

      beginAtZero: true,

      grid: {
        color: "#edf0f6"
      },

      ticks: {

        font: {
          size: 9
        },

        color: "#9aa1b2"
      }

    }

  }

}


const genericBarOptions = computed(() => ({
  ...chartOptions
}))


const doughnutOptions = {

  responsive: true,

  maintainAspectRatio: false,

  cutout: "64%",

  plugins: {

    legend: {

      position: "bottom",

      labels: {

        boxWidth: 10,

        boxHeight: 10,

        padding: 15,

        font: {
          size: 10
        }

      }

    },

    tooltip: {
      backgroundColor: "#20283a",
      padding: 10,
      cornerRadius: 9
    }

  }

}


// ============================================================
// EVOLUCION GENERICA
// ============================================================

const evolutionChart = computed(() => {

  if (
    !dashboard.value ||
    !dashboard.value.evolucion
  ) {

    return {
      labels: [],
      datasets: []
    }

  }


  const data =
    dashboard.value.evolucion


  return {

    labels: data.map(
      item => item.fecha
    ),

    datasets: [

      {

        label: "Valor",

        data: data.map(
          item => item.valor
        ),

        borderColor: "#5574E8",

        backgroundColor:
          "rgba(85, 116, 232, 0.10)",

        borderWidth: 3,

        tension: 0.35,

        fill: true,

        pointBackgroundColor:
          "#5574E8",

        pointBorderColor:
          "#ffffff",

        pointBorderWidth: 2,

        pointRadius: 3,

        pointHoverRadius: 6

      }

    ]

  }

})


// ============================================================
// AUDITORIA
// ============================================================

const auditoriaAccionesChart = computed(() => {

  const data =
    dashboard.value?.por_accion || []


  return {

    labels:
      chartLabels(data),

    datasets: [

      {

        data:
          chartValues(data),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


const auditoriaTablasChart = computed(() => {

  const data =
    dashboard.value?.por_tabla || []


  return {

    labels:
      chartLabels(data),

    datasets: [

      {

        data:
          chartValues(data),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


// ============================================================
// FUENTES
// ============================================================

const fuentesChart = computed(() => {

  const data =
    dashboard.value?.por_fuente || []


  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: data.map(
          item => item.sesiones
        ),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderColor: "#ffffff",

        borderWidth: 3,

        hoverOffset: 7

      }

    ]

  }

})


const mediosChart = computed(() => {

  const data =
    dashboard.value?.por_medio || []


  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: data.map(
          item => item.sesiones
        ),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


// ============================================================
// EVENTOS
// ============================================================

const eventosTipoChart = computed(() => {

  const data =
    dashboard.value?.por_tipo || []


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
          chartColors.slice(
            0,
            data.length
          ),

        borderColor: "#ffffff",

        borderWidth: 3,

        hoverOffset: 7

      }

    ]

  }

})


const eventosPaginasChart = computed(() => {

  const data =
    dashboard.value?.por_pagina || []


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
          chartColors.slice(
            0,
            data.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


// ============================================================
// VISITANTES
// ============================================================

const visitantesPaisChart = computed(() => {

  const data =
    dashboard.value?.por_pais || []


  const top =
    data.slice(0, 8)


  return {

    labels: top.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: top.map(
          item => item.visitantes
        ),

        backgroundColor:
          chartColors.slice(
            0,
            top.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


const dispositivosChart = computed(() => {

  const data =
    dashboard.value?.por_dispositivo || []


  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: data.map(
          item => item.visitantes
        ),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderColor: "#ffffff",

        borderWidth: 3,

        hoverOffset: 7

      }

    ]

  }

})


const sistemasChart = computed(() => {

  const data =
    dashboard.value?.por_sistema_operativo
    || []


  return {

    labels: data.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: data.map(
          item => item.visitantes
        ),

        backgroundColor:
          chartColors.slice(
            0,
            data.length
          ),

        borderColor: "#ffffff",

        borderWidth: 3,

        hoverOffset: 7

      }

    ]

  }

})


// ============================================================
// SESIONES
// ============================================================

const sesionesFuenteChart = computed(() => {

  const data =
    dashboard.value?.por_fuente || []


  const top =
    data.slice(0, 10)


  return {

    labels: top.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: top.map(
          item => item.valor
        ),

        backgroundColor:
          chartColors.slice(
            0,
            top.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


const entradaChart = computed(() => {

  const data =
    dashboard.value?.paginas_entrada || []


  const top =
    data.slice(0, 10)


  return {

    labels: top.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: top.map(
          item => item.valor
        ),

        backgroundColor:
          chartColors.slice(
            0,
            top.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


const salidaChart = computed(() => {

  const data =
    dashboard.value?.paginas_salida || []


  const top =
    data.slice(0, 10)


  return {

    labels: top.map(
      item => item.nombre
    ),

    datasets: [

      {

        data: top.map(
          item => item.valor
        ),

        backgroundColor:
          chartColors.slice(
            0,
            top.length
          ),

        borderRadius: 8,

        borderSkipped: false

      }

    ]

  }

})


const rebotesChart = computed(() => {

  const data =
    dashboard.value?.rebotes_por_dia
    || []


  return {

    labels: data.map(
      item => item.fecha
    ),

    datasets: [

      {

        label: "Rebotes",

        data: data.map(
          item => item.valor
        ),

        borderColor: "#D25896",

        backgroundColor:
          "rgba(210, 88, 150, .10)",

        borderWidth: 3,

        tension: .35,

        fill: true,

        pointBackgroundColor:
          "#D25896",

        pointBorderColor:
          "#ffffff",

        pointBorderWidth: 2,

        pointRadius: 3,

        pointHoverRadius: 6

      }

    ]

  }

})


// ============================================================
// WATCH
// ============================================================

watch(
  activeReport,
  async () => {

    if (
      isBusinessReport.value
    ) {
      return
    }

    await loadFilters()

    await loadDashboard()

  }
)


// ============================================================
// INITIAL LOAD
// ============================================================

onMounted(async () => {

  await loadFilters()

  await loadDashboard()

})
</script>


<template>

  <div class="app-shell">


    <!-- ======================================================
         SIDEBAR
    ======================================================= -->

    <aside class="sidebar">


      <!-- BRAND -->

      <div class="brand">

        <div class="brand-icon">

          <BarChart3 :size="20" />

        </div>


        <div class="brand-text">

          <strong>
            NexByte
          </strong>

          <span>
            Analytics
          </span>

        </div>

      </div>


      <!-- NAV -->

      <nav class="sidebar-nav">


        <template
          v-for="(report, index) in reports"
          :key="report.id"
        >


          <!-- SECTION -->

          <div
            v-if="
              index === 0 ||
              reports[index - 1].section !==
                report.section
            "

            class="sidebar-label"
          >

            {{ report.section }}

          </div>


          <!-- REPORT -->

          <button

            class="nav-item"

            :class="{
              active:
                activeReport === report.id,

              business:
                report.section === 'NEGOCIO'
            }"

            @click="
              changeReport(report.id)
            "
          >

            <component
              :is="report.icon"
              :size="18"
            />


            <div class="nav-text">

              <strong>
                {{ report.name }}
              </strong>

              <span>
                {{ report.description }}
              </span>

            </div>

          </button>

        </template>

      </nav>


      <!-- STATUS -->

      <div class="sidebar-bottom">

        <div class="system-status">

          <span></span>

          API conectada

        </div>

      </div>

    </aside>



    <!-- ======================================================
         MAIN
    ======================================================= -->

    <main class="main-content">


      <!-- ====================================================
           NEGOCIO
      ===================================================== -->

      <template
        v-if="activeReport === 'cursos'"
      >

        <CursosDashboard />

      </template>


      <template
        v-else-if="
          activeReport === 'servicios'
        "
      >

        <ServiciosDashboard />

      </template>


      <!-- ====================================================
           ANALÍTICA
      ===================================================== -->

      <template v-else>


        <!-- HEADER -->

        <header class="topbar">

          <div>

            <div class="breadcrumb">

              ANALÍTICA

            </div>


            <h1>

              {{ reportTitle }}

            </h1>


            <p>

              {{ reportDescription }}

            </p>

          </div>


          <div class="topbar-right">

            <div class="last-update">

              <TrendingUp
                :size="15"
              />

              Datos en tiempo real

            </div>

          </div>

        </header>


        <!-- ==================================================
             FILTERS
        =================================================== -->

        <section class="filters-card">


          <div class="filter-header">

            <div>

              <h3>
                Filtros
              </h3>

              <span>
                Personaliza el período y las dimensiones
              </span>

            </div>


            <CalendarDays
              :size="19"
            />

          </div>


          <div class="filters-grid">


            <!-- DESDE -->

            <label class="filter-field">

              <span>
                Desde
              </span>

              <input
                type="datetime-local"
                v-model="filters.desde"
              />

            </label>


            <!-- HASTA -->

            <label class="filter-field">

              <span>
                Hasta
              </span>

              <input
                type="datetime-local"
                v-model="filters.hasta"
              />

            </label>


            <!-- =================================================
                 AUDITORIA
            ================================================== -->

            <label
              v-if="
                activeReport === 'auditoria' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Acción
              </span>


              <select
                v-model="extraFilters.accion"
              >

                <option value="">
                  Todas
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.acciones
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <label
              v-if="
                activeReport === 'auditoria' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Tabla
              </span>


              <select
                v-model="extraFilters.tabla"
              >

                <option value="">
                  Todas
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.tablas
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <!-- =================================================
                 FUENTES
            ================================================== -->

            <label
              v-if="
                activeReport === 'fuentes' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Fuente
              </span>


              <select
                v-model="extraFilters.fuente"
              >

                <option value="">
                  Todas
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.fuentes
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <label
              v-if="
                activeReport === 'fuentes' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Medio
              </span>


              <select
                v-model="extraFilters.medio"
              >

                <option value="">
                  Todos
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.medios
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <!-- =================================================
                 EVENTOS
            ================================================== -->

            <label
              v-if="
                activeReport === 'eventos' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Tipo de evento
              </span>


              <select
                v-model="
                  extraFilters.tipo_evento
                "
              >

                <option value="">
                  Todos
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.tipos_evento
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <label
              v-if="
                activeReport === 'eventos' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Curso
              </span>


              <select
                v-model="
                  extraFilters.id_curso
                "
              >

                <option value="">
                  Todos
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.cursos
                  "

                  :key="item.id_curso"

                  :value="item.id_curso"
                >

                  {{ item.titulo }}

                </option>

              </select>

            </label>


            <!-- =================================================
                 VISITANTES
            ================================================== -->

            <label
              v-if="
                activeReport === 'visitantes' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                País
              </span>


              <select
                v-model="extraFilters.pais"
              >

                <option value="">
                  Todos
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.paises
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <label
              v-if="
                activeReport === 'visitantes' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Dispositivo
              </span>


              <select
                v-model="
                  extraFilters.dispositivo
                "
              >

                <option value="">
                  Todos
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.dispositivos
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <!-- =================================================
                 SESIONES
            ================================================== -->

            <label
              v-if="
                activeReport === 'sesiones' &&
                filterOptions
              "

              class="filter-field"
            >

              <span>
                Fuente
              </span>


              <select
                v-model="
                  extraFilters.fuente
                "
              >

                <option value="">
                  Todas
                </option>

                <option
                  v-for="
                    item in
                    filterOptions.fuentes
                  "

                  :key="item"

                  :value="item"
                >

                  {{ item }}

                </option>

              </select>

            </label>


            <label
              v-if="
                activeReport === 'sesiones'
              "

              class="filter-field"
            >

              <span>
                Rebote
              </span>


              <select
                v-model="
                  extraFilters.rebote
                "
              >

                <option value="">
                  Todos
                </option>

                <option value="true">
                  Solo rebotes
                </option>

                <option value="false">
                  Sin rebote
                </option>

              </select>

            </label>

          </div>


          <!-- BUTTONS -->

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


        <!-- ==================================================
             LOADING
        =================================================== -->

        <div
          v-if="loading"
          class="state-card"
        >

          <div class="spinner"></div>

          <p>
            Cargando información...
          </p>

        </div>


        <!-- ==================================================
             ERROR
        =================================================== -->

        <div
          v-else-if="error"
          class="state-card error-state"
        >

          <div class="error-icon">
            !
          </div>


          <strong>
            No se pudo cargar el dashboard
          </strong>


          <p>
            {{ error }}
          </p>


          <button
            class="button primary"
            @click="loadDashboard"
          >

            Reintentar

          </button>

        </div>


        <!-- ==================================================
             DASHBOARD
        =================================================== -->

        <template
          v-else-if="dashboard"
        >


          <!-- =================================================
               AUDITORIA
          ================================================== -->

          <template
            v-if="
              activeReport === 'auditoria'
            "
          >

            <section class="kpi-grid">


              <KpiCard
                title="Acciones totales"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .total_acciones
                  )
                "
                subtitle="Registros auditados"
                :icon="Database"
              />


              <KpiCard
                title="Usuarios activos"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .usuarios_activos
                  )
                "
                subtitle="Administradores"
                :icon="Users"
              />


              <KpiCard
                title="Tablas afectadas"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .tablas_afectadas
                  )
                "
                subtitle="Entidades modificadas"
                :icon="Database"
              />


              <KpiCard
                title="Acciones del período"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .acciones_periodo
                  )
                "
                subtitle="Según filtros"
                :icon="Activity"
              />

            </section>


            <section class="reports-grid">


              <ReportCard
                title="Evolución de actividad"
                subtitle="Acciones registradas por día"
                span="full"
              >

                <div class="chart-lg">

                  <Line
                    :data="evolutionChart"
                    :options="chartOptions"
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Acciones"
                subtitle="Distribución por tipo"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      auditoriaAccionesChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Tablas afectadas"
                subtitle="Actividad por entidad"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      auditoriaTablasChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>

            </section>

          </template>


          <!-- =================================================
               FUENTES
          ================================================== -->

          <template
            v-else-if="
              activeReport === 'fuentes'
            "
          >

            <section class="kpi-grid">


              <KpiCard
                title="Sesiones"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .total_sesiones
                  )
                "
                subtitle="Tráfico total"
                :icon="Activity"
              />


              <KpiCard
                title="Fuentes"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .fuentes_distintas
                  )
                "
                subtitle="Orígenes diferentes"
                :icon="Globe"
              />


              <KpiCard
                title="Campañas"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .campanias_distintas
                  )
                "
                subtitle="Campañas registradas"
                :icon="Megaphone"
              />


              <KpiCard
                title="Mejor fuente"
                :value="
                  dashboard.kpis
                    .mejor_fuente ||
                  'N/D'
                "
                subtitle="Mayor tráfico"
                :icon="BarChart3"
              />

            </section>


            <section class="reports-grid">


              <ReportCard
                title="Evolución del tráfico"
                subtitle="Sesiones por día"
                span="full"
              >

                <div class="chart-lg">

                  <Line
                    :data="evolutionChart"
                    :options="chartOptions"
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Sesiones por fuente"
                subtitle="Origen del tráfico"
              >

                <div class="chart-md">

                  <Doughnut
                    :data="
                      fuentesChart
                    "
                    :options="
                      doughnutOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Sesiones por medio"
                subtitle="Distribución de medios"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      mediosChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>

            </section>

          </template>


          <!-- =================================================
               EVENTOS
          ================================================== -->

          <template
            v-else-if="
              activeReport === 'eventos'
            "
          >

            <section class="kpi-grid">


              <KpiCard
                title="Eventos"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .total_eventos
                  )
                "
                subtitle="Eventos registrados"
                :icon="MousePointerClick"
              />


              <KpiCard
                title="Sesiones con eventos"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .sesiones_con_eventos
                  )
                "
                subtitle="Sesiones activas"
                :icon="Activity"
              />


              <KpiCard
                title="Evento principal"
                :value="
                  dashboard.kpis
                    .tipo_principal ||
                  'N/D'
                "
                subtitle="Más frecuente"
                :icon="MousePointer"
              />


              <KpiCard
                title="Página principal"
                :value="
                  dashboard.kpis
                    .pagina_principal ||
                  'N/D'
                "
                subtitle="Mayor interacción"
                :icon="Globe"
              />

            </section>


            <section class="reports-grid">


              <ReportCard
                title="Evolución de eventos"
                subtitle="Actividad diaria"
                span="full"
              >

                <div class="chart-lg">

                  <Line
                    :data="evolutionChart"
                    :options="chartOptions"
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Tipos de evento"
                subtitle="Eventos registrados"
              >

                <div class="chart-md">

                  <Doughnut
                    :data="
                      eventosTipoChart
                    "
                    :options="
                      doughnutOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Páginas"
                subtitle="Interacción por página"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      eventosPaginasChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>

            </section>

          </template>


          <!-- =================================================
               VISITANTES
          ================================================== -->

          <template
            v-else-if="
              activeReport === 'visitantes'
            "
          >

            <section class="kpi-grid">


              <KpiCard
                title="Visitantes"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .total_visitantes
                  )
                "
                subtitle="Usuarios identificados"
                :icon="Users"
              />


              <KpiCard
                title="Nuevos"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .nuevos_visitantes
                  )
                "
                subtitle="Primera visita"
                :icon="UserPlus"
              />


              <KpiCard
                title="Recurrentes"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .visitantes_recurrentes
                  )
                "
                subtitle="Visitantes recurrentes"
                :icon="Activity"
              />


              <KpiCard
                title="País principal"
                :value="
                  dashboard.kpis
                    .pais_principal ||
                  'N/D'
                "
                subtitle="Mayor audiencia"
                :icon="Globe"
              />

            </section>


            <section class="reports-grid">


              <ReportCard
                title="Evolución de visitantes"
                subtitle="Visitantes por día"
                span="full"
              >

                <div class="chart-lg">

                  <Line
                    :data="
                      evolutionChart
                    "
                    :options="
                      chartOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Visitantes por país"
                subtitle="Distribución geográfica"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      visitantesPaisChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Dispositivos"
                subtitle="Tipo de dispositivo"
              >

                <div class="chart-md">

                  <Doughnut
                    :data="
                      dispositivosChart
                    "
                    :options="
                      doughnutOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Sistemas operativos"
                subtitle="Plataformas utilizadas"
              >

                <div class="chart-md">

                  <Doughnut
                    :data="
                      sistemasChart
                    "
                    :options="
                      doughnutOptions
                    "
                  />

                </div>

              </ReportCard>

            </section>

          </template>


          <!-- =================================================
               SESIONES
          ================================================== -->

          <template
            v-else-if="
              activeReport === 'sesiones'
            "
          >

            <section class="kpi-grid">


              <KpiCard
                title="Sesiones"
                :value="
                  formatNumber(
                    dashboard.kpis
                      .total_sesiones
                  )
                "
                subtitle="Sesiones registradas"
                :icon="Activity"
              />


              <KpiCard
                title="Duración promedio"
                :value="
                  formatSeconds(
                    dashboard.kpis
                      .duracion_promedio_segundos
                  )
                "
                subtitle="Tiempo medio"
                :icon="CalendarDays"
              />


              <KpiCard
                title="Páginas / sesión"
                :value="
                  formatDecimal(
                    dashboard.kpis
                      .paginas_promedio
                  )
                "
                subtitle="Promedio"
                :icon="Globe"
              />


              <KpiCard
                title="Tasa de rebote"
                :value="
                  `${formatDecimal(
                    dashboard.kpis
                      .tasa_rebote
                  )}%`
                "
                subtitle="Sesiones sin interacción"
                :icon="Activity"
              />

            </section>


            <section class="reports-grid">


              <ReportCard
                title="Evolución de sesiones"
                subtitle="Sesiones por día"
                span="full"
              >

                <div class="chart-lg">

                  <Line
                    :data="
                      evolutionChart
                    "
                    :options="
                      chartOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Fuentes"
                subtitle="Sesiones por origen"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      sesionesFuenteChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Páginas de entrada"
                subtitle="Principales landings"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      entradaChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Páginas de salida"
                subtitle="Dónde terminan las sesiones"
              >

                <div class="chart-md">

                  <Bar
                    :data="
                      salidaChart
                    "
                    :options="
                      genericBarOptions
                    "
                  />

                </div>

              </ReportCard>


              <ReportCard
                title="Rebotes"
                subtitle="Evolución diaria"
              >

                <div class="chart-md">

                  <Line
                    :data="
                      rebotesChart
                    "
                    :options="
                      chartOptions
                    "
                  />

                </div>

              </ReportCard>

            </section>

          </template>

        </template>

      </template>

    </main>

  </div>

</template>