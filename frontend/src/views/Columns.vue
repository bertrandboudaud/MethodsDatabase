<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Columns</h1>
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
              <tr v-for="column in columns" :key="column.id">
                <td>{{ column.id }}</td>
                <td>{{ column.name }}</td>
                <td class="text-right">
                  <a href="#" @click.prevent="populateColumnToEdit(column)">Edit</a>
                  -
                  <a href="#" @click.prevent="deleteColumn(column.id)">Delete</a>
                </td>
              </tr>
            </tbody>
          </table>
        </b-col>
        <b-col lg="3">
          <b-card :title="model.id ? 'Edit Column ID#' + model.id : 'New Column'">
            <form @submit.prevent="saveColumn">
              <b-form-group label="name">
                <b-form-input
                  v-model="model.name"
                  type="text"
                ></b-form-input>
              </b-form-group>
              <div>
                <b-btn type="submit" variant="success">Save Column</b-btn>
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

import { backend, Column } from '../backend'

const NO_INSTRUMENT = { id: '', name: '', iupac: '' }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  columns: Array<Column> = []
  model: Column = NO_INSTRUMENT
  error: Object = null
  errors: Array<String> = []

  async beforeMount() {
    this.refreshColumns()
  }

  async refreshColumns() {
    this.isLoading = true
    try {
      let response = await backend.getColumns()
      this.columns = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.isLoading = false
  }

  async populateColumnToEdit(column) {
    this.model = Object.assign({}, column)
  }

  async saveColumn() {
    try {
      if (this.model.id) {
        await backend.updateColumn(this.model.id, this.model)
      } else {
        await backend.createColumn(this.model)
      }
      this.model = NO_INSTRUMENT // reset form
      await this.refreshColumns()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteColumn(id) {
    if (confirm('Are you sure you want to delete this column?')) {
      // if we are editing a columns we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = NO_INSTRUMENT
      }
      await backend.deleteColumn(id)
      await this.refreshColumns()
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
