<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Eluents</h1>
      <b-alert :show="isLoading" variant="info">Loading...</b-alert>
      <b-row>
        <b-col>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>name</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="eluent in eluents" :key="eluent.id">
                <td>{{ eluent.id }}</td>
                <td>{{ eluent.name }}</td>
                <td class="text-right">
                  <a href="#" @click.prevent="populateEluentToEdit(eluent)">Edit</a>
                  -
                  <a href="#" @click.prevent="deleteEluent(eluent.id)">Delete</a>
                </td>
              </tr>
            </tbody>
          </table>
        </b-col>
        <b-col lg="3">
          <b-card :title="model.id ? 'Edit Eluent ID#' + model.id : 'New Eluent'">
            <form @submit.prevent="saveEluent">
              <b-form-group label="name">
                <b-form-input
                  v-model="model.name"
                  type="text"
                ></b-form-input>
              </b-form-group>
              <div>
                <b-btn type="submit" variant="success">Save Eluent</b-btn>
              </div>
            </form>
          </b-card>
          <div v-if="errors">
            <span v-for="error in errors" :key="error">
              {{ error }}
            </span>
          </div>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { backend, Eluent } from '../backend'

const NO_INSTRUMENT = { id: '', name: '', iupac: '' }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  eluents: Array<Eluent> = []
  model: Eluent = NO_INSTRUMENT
  error: Object = null
  errors: Array<String> = []

  async beforeMount() {
    this.refreshEluents()
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

  async populateEluentToEdit(eluent) {
    this.model = Object.assign({}, eluent)
  }

  async saveEluent() {
    try {
      if (this.model.id) {
        await backend.updateEluent(this.model.id, this.model)
      } else {
        await backend.createEluent(this.model)
      }
      this.model = NO_INSTRUMENT // reset form
      await this.refreshEluents()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteEluent(id) {
    if (confirm('Are you sure you want to delete this eluent?')) {
      // if we are editing a eluents we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = NO_INSTRUMENT
      }
      await backend.deleteEluent(id)
      await this.refreshEluents()
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
}
</script>
