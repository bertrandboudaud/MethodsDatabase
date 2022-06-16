<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Methods</h1>
      <b-alert :show="isLoading" variant="info">Loading...</b-alert>

      <b-container fluid>
        <b-row>
          <b-col sm="3">
            <label>name</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
              v-model="filter.name"
              type="text"
            ></b-form-input>
          </b-col>
        </b-row>
        <b-button @click="filterMethod()" variant="success">Filter</b-button>
      </b-container>

      <b-button @click="newMethod()">New Method</b-button>
      
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>name</th>
            <th>technique</th>
            <th>comment</th>
            <th>analysis_method</th>
            <th>eluent_a</th>
            <th>eluent_b</th>
            <th>instrument</th>
            <th>&nbsp;</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="method in methods" :key="method.id">
            <td>{{ method.id }}</td>
            <td>{{ method.name }}</td>
            <td>{{ method.technique }}</td>
            <td>{{ method.comment }}</td>
            <td>{{ method.analysis_method }}</td>
            <td>{{ getEluentNameFromEluentId(method.eluent_a_id) }}</td>
            <td>{{ getEluentNameFromEluentId(method.eluent_b_id) }}</td>
            <td>{{ getInstrumentNameFromInstrumentId(method.instrument_id) }}</td>
            <td class="text-right">
              <a href="#" @click="modalShow = !modalShow" @click.prevent="populateMethodToEdit(method)">Edit</a>
              -
              <a href="#" @click.prevent="deleteMethod(method.id)">Delete</a>
            </td>
          </tr>
        </tbody>
      </table>

      <b-modal
        id="modal-edit"
        ref="modal"
        v-model="modalShow"
        :title="model.id ? 'Edit Compound ID#' + model.id : 'New Compound'"
        @ok="saveMethod"
      >
        <form @submit.prevent="saveMethod">
          <b-form-group label="name">
            <b-form-input
              v-model="model.name"
              type="text"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="technique">
            <b-form-input
              v-model="model.technique"
              type="text"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="comment">
            <b-form-input
              v-model="model.comment"
              type="text"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="analysis_method">
            <b-form-input
              v-model="model.analysis_method"
              type="text"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="eluent a">
            <v-select
              v-model="model.eluent_a_id"
              :options="eluents" 
              :reduce="eluent => eluent.id"
              label="name"
            ></v-select>
          </b-form-group>
          <b-form-group label="eluent b">
            <v-select
              v-model="model.eluent_b_id"
              :options="eluents" 
              :reduce="eluent => eluent.id"
              label="name"
            ></v-select>
          </b-form-group>
          <b-form-group label="instrument">
            <v-select
              v-model="model.instrument_id"
              :options="instruments" 
              :reduce="instrument => instrument.id"
              label="name"
            ></v-select>
          </b-form-group>
        </form>
      </b-modal>

      <div v-if="errors">
        <b-alert variant="danger" v-model="showError" dismissible>
          <span v-for="error in errors" :key="error">
              {{ error }}
          </span>
        </b-alert>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { backend, Method } from '../backend'

const NO_METHOD = { 
  id: '', 
  name: '', 
  technique: '', 
  comment: '', 
  analysis_method: '', 
  eluent_a_id: '', 
  eluent_b_id: '',
  instrument_id: ''
 }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  methods: Array<Method> = []
  eluents: Array<Method> = [] // TODO: optimize, we actually only need id and names
  instruments: Array<Method> = [] // TODO: optimize, we actually only need id and names
  model: Method = NO_METHOD
  error: Object = null
  errors: Array<String> = []
  filter: Object = { name: '' }
  showError : Boolean = false

  data() {
    return {
      modalShow : false,
      showError : false,
    }
  }

  async beforeMount() {
    this.filter = { name: '' };
    this.refreshMethods()
    this.refreshEluents()
    this.refreshInstruments()
  }

  async refreshMethods() {
    this.isLoading = true
    try {
      let response = await backend.getMethods()
      this.methods = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async refreshEluents() {
    this.isLoading = true
    try {
      let response = await backend.getEluents()
      this.eluents = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async refreshInstruments() {
    this.isLoading = true
    try {
      let response = await backend.getInstruments()
      this.instruments = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async newMethod() {
     this.model = NO_METHOD // reset form
     this.modalShow = true;
  }

  async populateMethodToEdit(method) {
    this.model = Object.assign({}, method)
  }

  async saveMethod() {
    try {
      if (this.model.id) {
        await backend.updateMethod(this.model.id, this.model)
      } else {
        await backend.createMethod(this.model)
      }
      this.model = NO_METHOD // reset form
      await this.refreshMethods()
    } catch (err) {
      this.parseError(err)
    }
  }

  async filterMethod() {
    this.isLoading = true
    try {
      let response = await backend.getCompounds(this.filter)
      this.methods = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async deleteMethod(id) {
    if (confirm('Are you sure you want to delete this method?')) {
      // if we are editing a methods we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = NO_METHOD
      }
      await backend.deleteMethod(id)
      await this.refreshMethods()
    }
  }

  parseError(error) {
    this.error = error
    this.errors = []
    if (error) {
      for (let idx in error.response.data.errors) {
        this.errors.push(idx + ': ' + error.response.data.errors[idx])
      }
    }
  }

  getEluentNameFromEluentId(eluent_id)
  {
    var eluent =  this.eluents.find(eluent => eluent.id === eluent_id)
    if (typeof eluent !== 'undefined')
    {
      return eluent.name
    }
    else
    {
      return ""
    }
  }

  getInstrumentNameFromInstrumentId(eluent_id)
  {
    var instrument =  this.instruments.find(instrument => instrument.id === eluent_id)
    if (typeof instrument !== 'undefined')
    {
      return instrument.name
    }
    else
    {
      return ""
    }
  }
}
</script>
