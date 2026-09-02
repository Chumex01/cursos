const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"


// ============================================================
// HELPERS
// ============================================================

function buildQuery(params = {}) {
  const search = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (
      value !== undefined &&
      value !== null &&
      value !== ""
    ) {
      search.append(key, value)
    }
  })

  const query = search.toString()

  return query ? `?${query}` : ""
}


// ============================================================
// REQUEST
// ============================================================

async function request(url, options = {}) {
  const response = await fetch(
    `${API_URL}${url}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {})
      },
      ...options
    }
  )

  if (!response.ok) {
    let message = `Error HTTP ${response.status}`

    try {
      const data = await response.json()

      if (data?.detail) {
        message = data.detail
      }
    } catch {
      // No pasa nada
    }

    throw new Error(message)
  }

  return response.json()
}


// ============================================================
// DASHBOARDS
// ============================================================

export async function getAuditoriaDashboard(filters = {}) {
  return request(
    `/reportes/auditoria/dashboard${buildQuery(filters)}`
  )
}


export async function getFuentesDashboard(filters = {}) {
  return request(
    `/reportes/fuentes-trafico/dashboard${buildQuery(filters)}`
  )
}


export async function getEventosDashboard(filters = {}) {
  return request(
    `/reportes/eventos/dashboard${buildQuery(filters)}`
  )
}


export async function getVisitantesDashboard(filters = {}) {
  return request(
    `/reportes/visitantes/dashboard${buildQuery(filters)}`
  )
}


export async function getSesionesDashboard(filters = {}) {
  return request(
    `/reportes/sesiones/dashboard${buildQuery(filters)}`
  )
}


// ============================================================
// FILTROS
// ============================================================

export async function getAuditoriaFiltros() {
  return request(
    "/reportes/auditoria/filtros"
  )
}


export async function getFuentesFiltros() {
  return request(
    "/reportes/fuentes-trafico/filtros"
  )
}


export async function getEventosFiltros() {
  return request(
    "/reportes/eventos/filtros"
  )
}


export async function getVisitantesFiltros() {
  return request(
    "/reportes/visitantes/filtros"
  )
}


export async function getSesionesFiltros() {
  return request(
    "/reportes/sesiones/filtros"
  )
}


// ============================================================
// DETALLE
// ============================================================

export async function getAuditoriaDetalle(filters = {}) {
  return request(
    `/reportes/auditoria/detalle${buildQuery(filters)}`
  )
}


export async function getFuentesDetalle(filters = {}) {
  return request(
    `/reportes/fuentes-trafico/detalle${buildQuery(filters)}`
  )
}


export async function getEventosDetalle(filters = {}) {
  return request(
    `/reportes/eventos/detalle${buildQuery(filters)}`
  )
}


export async function getVisitantesDetalle(filters = {}) {
  return request(
    `/reportes/visitantes/detalle${buildQuery(filters)}`
  )
}


export async function getSesionesDetalle(filters = {}) {
  return request(
    `/reportes/sesiones/detalle${buildQuery(filters)}`
  )
}

// ============================================================
// NEGOCIO - CURSOS
// ============================================================

export async function getCursosDashboard(filters = {}) {
  return request(
    `/reportes/negocio/cursos/dashboard${buildQuery(filters)}`
  )
}


export async function getCursosFiltros() {
  return request(
    "/reportes/negocio/cursos/filtros"
  )
}


// ============================================================
// NEGOCIO - SERVICIOS
// ============================================================

export async function getServiciosDashboard(filters = {}) {
  return request(
    `/reportes/negocio/servicios/dashboard${buildQuery(filters)}`
  )
}


export async function getServiciosFiltros() {
  return request(
    "/reportes/negocio/servicios/filtros"
  )
}

// ============================================================
// CURSOS (PÚBLICOS & ESTUDIANTES)
// ============================================================

export async function getCursos(filters = {}) {
  return request(`/public/cursos${buildQuery(filters)}`)
}

export async function getCursoBySlug(slug) {
  return request(`/public/cursos/${slug}`)
}

export async function inscribirCursoGratis(idCurso, payload) {
  return request(`/cursos/${idCurso}/inscribir-gratis`, {
    method: "POST",
    body: JSON.stringify(payload)
  })
}

export async function procesarCheckout(payload) {
  return request(`/checkout/procesar`, {
    method: "POST",
    body: JSON.stringify(payload)
  })
}

export async function actualizarProgresoLeccion(idInscripcion, idLeccion, porcentaje) {
  return request(`/inscripciones/${idInscripcion}/lecciones/${idLeccion}`, {
    method: "PUT",
    body: JSON.stringify({ porcentaje })
  })
}