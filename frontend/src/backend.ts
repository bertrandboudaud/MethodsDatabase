import axios from 'axios'

let $axios = axios.create({
  // TODO: for some reasone devServer.proxy setting
  // in the vue.config.js doesn't work
  // https://cli.vuejs.org/config/#devserver
  // So temporary, we set the full URL here
  // baseURL: 'http://localhost:5000/api/',
  baseURL: 'http://localhost:5000/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' },
})

// Request Interceptor
$axios.interceptors.request.use(function(config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(
  function(response) {
    return response
  },
  function(error) {
    // Handle Error
    return Promise.reject(error)
  },
)

export interface User {
  id: String
  username: String
  email: String
}

export interface Instrument {
  id: String
  name: String
  model: String
}

export interface Compound {
  id: String
  name: String
  iupac: String
  method_id: String
}

export interface Eluent {
  id: String
  name: String
}

export interface Column {
  id: String
  name: String
}

export interface Method {
  id: String
  name: String
  technique: String
  comment: String
  analysis_method: String
  eluent_a_id: String
  eluent_b_id: String
  instrument_id: String
  column_id: String
  lod: Number
}

export let backend = {

  // ---------------------
  // Users
  // ---------------------

  getUsers() {
    return $axios.get(`users/`).then((response) => response.data)
  },

  getUser(id) {
    return $axios.get(`user/${id}`).then((response) => response.data)
  },

  createUser(data) {
    let user = {
      username: data.username,
      email: data.email,
    }
    return $axios.post(`users/`, user).then((response) => response.data)
  },

  updateUser(id, data) {
    let user = {
      username: data.username,
      email: data.email,
    }
    return $axios.post(`users/${id}`, user).then((response) => response.data)
  },

  deleteUser(id) {
    return $axios.delete(`users/${id}`).then((response) => response.data)
  },

  // ---------------------
  // Instruments
  // ---------------------

  getInstruments() {
    return $axios.get(`instruments/`).then((response) => response.data)
  },

  getInstrument(id) {
    return $axios.get(`instruments/${id}`).then((response) => response.data)
  },

  createInstrument(data) {
    let instrument = {
      name: data.name,
      model: data.model,
    }
    return $axios.post(`instruments/`, instrument).then((response) => response.data)
  },

  updateInstrument(id, data) {
    let instrument = {
      name: data.name,
      model: data.model,
    }
    return $axios.post(`instruments/${id}`, instrument).then((response) => response.data)
  },

  deleteInstrument(id) {
    return $axios.delete(`instruments/${id}`).then((response) => response.data)
  },

  // ---------------------
  // Compounds
  // ---------------------

  getCompounds(filter = null) {
    return $axios.get(`compounds/`, {params: filter}).then((response) => response.data)
  },

  getCompound(id) {
    return $axios.get(`compounds/${id}`).then((response) => response.data)
  },

  createCompound(data) {
    let compound = {
      name: data.name,
      iupac: data.iupac,
      method_id : data.method_id,
    }
    return $axios.post(`compounds/`, compound).then((response) => response.data)
  },

  updateCompound(id, data) {
    let compound = {
      id: id,
      name: data.name,
      iupac: data.iupac,
      method_id : data.method_id,
    }
    return $axios.post(`compounds/${id}`, compound).then((response) => response.data)
  },

  deleteCompound(id) {
    return $axios.delete(`compounds/${id}`).then((response) => response.data)
  },

  // ---------------------
  // Eluents
  // ---------------------

  getEluents() {
    return $axios.get(`eluents/`).then((response) => response.data)
  },

  getEluent(id) {
    return $axios.get(`eluents/${id}`).then((response) => response.data)
  },

  createEluent(data) {
    let eluent = {
      name: data.name,
    }
    return $axios.post(`eluents/`, eluent).then((response) => response.data)
  },

  updateEluent(id, data) {
    let eluent = {
      name: data.name,
    }
    return $axios.post(`eluents/${id}`, eluent).then((response) => response.data)
  },

  deleteEluent(id) {
    return $axios.delete(`eluents/${id}`).then((response) => response.data)
  },

  // ---------------------
  // Columns
  // ---------------------

  getColumns() {
    return $axios.get(`columns/`).then((response) => response.data)
  },

  getColumn(id) {
    return $axios.get(`columns/${id}`).then((response) => response.data)
  },

  createColumn(data) {
    let column = {
      name: data.name,
    }
    return $axios.post(`columns/`, column).then((response) => response.data)
  },

  updateColumn(id, data) {
    let column = {
      name: data.name,
    }
    return $axios.post(`columns/${id}`, column).then((response) => response.data)
  },

  deleteColumn(id) {
    return $axios.delete(`columns/${id}`).then((response) => response.data)
  },

  // ---------------------
  // Methods
  // ---------------------

  getMethods() {
    return $axios.get(`methods/`).then((response) => response.data)
  },

  getMethod(id) {
    return $axios.get(`methods/${id}`).then((response) => response.data)
  },

  createMethod(data) {
    let method = {
      name: data.name,
      technique: data.technique,
      comment: data.comment,
      analysis_method: data.analysis_method,
      eluent_a_id : data.eluent_a_id,
      eluent_b_id : data.eluent_b_id,
      instrument_id : data.instrument_id,
      column_id : data.column_id,
      lod : data.lod,
    }
    return $axios.post(`methods/`, method).then((response) => response.data)
  },

  updateMethod(id, data) {
    let method = {
      name: data.name,
      technique: data.technique,
      comment: data.comment,
      analysis_method: data.analysis_method,
      eluent_a_id : data.eluent_a_id,
      eluent_b_id : data.eluent_b_id,
      instrument_id : data.instrument_id,
      column_id : data.column_id,
      lod : data.lod,
    }
    return $axios.post(`methods/${id}`, method).then((response) => response.data)
  },

  deleteMethod(id) {
    return $axios.delete(`methods/${id}`).then((response) => response.data)
  },
}
