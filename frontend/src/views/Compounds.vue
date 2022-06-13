<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Compounds</h1>
      <b-alert :show="isLoading" variant="info">Loading...</b-alert>
      <b-row>
        <b-col>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>name</th>
                <th>iupac</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="compound in compounds" :key="compound.id">
                <td>{{ compound.id }}</td>
                <td>{{ compound.name }}</td>
                <td>{{ compound.iupac }}</td>
                <td class="text-right">
                  <a href="#" @click.prevent="populateCompoundToEdit(compound)">Edit</a>
                  -
                  <a href="#" @click.prevent="deleteCompound(compound.id)">Delete</a>
                </td>
              </tr>
            </tbody>
          </table>
        </b-col>
        <b-col lg="3">
          <b-card :title="model.id ? 'Edit Compound ID#' + model.id : 'New Compound'">
            <form @submit.prevent="saveCompound">
              <b-form-group label="name">
                <b-form-input
                  v-model="model.name"
                  type="text"
                ></b-form-input>
              </b-form-group>
              <b-form-group label="iupac">
                <b-form-input
                  v-model="model.iupac"
                  type="text"
                ></b-form-input>
              </b-form-group>
              <div>
                <b-btn type="submit" variant="success">Save Compound</b-btn>
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

import { backend, Compound } from '../backend'

const NO_INSTRUMENT = { id: '', name: '', iupac: '' }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  compounds: Array<Compound> = []
  model: Compound = NO_INSTRUMENT
  error: Object = null
  errors: Array<String> = []

  async beforeMount() {
    this.refreshCompounds()
  }

  async refreshCompounds() {
    this.isLoading = true
    try {
      let response = await backend.getCompounds()
      this.compounds = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async populateCompoundToEdit(compound) {
    this.model = Object.assign({}, compound)
  }

  async saveCompound() {
    try {
      if (this.model.id) {
        await backend.updateCompound(this.model.id, this.model)
      } else {
        await backend.createCompound(this.model)
      }
      this.model = NO_INSTRUMENT // reset form
      await this.refreshCompounds()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteCompound(id) {
    if (confirm('Are you sure you want to delete this compound?')) {
      // if we are editing a compounds we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = NO_INSTRUMENT
      }
      await backend.deleteCompound(id)
      await this.refreshCompounds()
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
