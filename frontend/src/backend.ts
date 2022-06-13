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

  getCompounds() {
    return $axios.get(`compounds/`).then((response) => response.data)
  },

  getCompound(id) {
    return $axios.get(`compounds/${id}`).then((response) => response.data)
  },

  createCompound(data) {
    let instrument = {
      name: data.name,
      iupac: data.iupac,
    }
    return $axios.post(`compounds/`, instrument).then((response) => response.data)
  },

  updateCompound(id, data) {
    let instrument = {
      name: data.name,
      iupac: data.iupac,
    }
    return $axios.post(`compounds/${id}`, instrument).then((response) => response.data)
  },

  deleteCompound(id) {
    return $axios.delete(`compounds/${id}`).then((response) => response.data)
  },
}
