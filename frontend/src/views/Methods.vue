<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Methods</h1>
      <b-alert :show="isLoading" variant="info">Loading...</b-alert>
      <b-row>
        <b-col>
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>name</th>
                <th>technique</th>
                <th>comment</th>
                <th>analysis_method</th>
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
                <td class="text-right">
                  <a href="#" @click.prevent="populateMethodToEdit(method)">Edit</a>
                  -
                  <a href="#" @click.prevent="deleteMethod(method.id)">Delete</a>
                </td>
              </tr>
            </tbody>
          </table>
        </b-col>
        <b-col lg="3">
          <b-card :title="model.id ? 'Edit Method ID#' + model.id : 'New Method'">
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
              <div>
                <b-btn type="submit" variant="success">Save Method</b-btn>
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

import { backend, Method } from '../backend'

const NO_METHOD = { id: '', name: '', technique: '', comment: '', analysis_method: '' }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  methods: Array<Method> = []
  model: Method = NO_METHOD
  error: Object = null
  errors: Array<String> = []

  async beforeMount() {
    this.refreshMethods()
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
}
</script>
