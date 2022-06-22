<template>
  <div>
    <div class="container-fluid mt-4">
      
      <div v-if="errors">
        <b-alert variant="danger" v-model="showError" dismissible>
          <span v-for="error in errors" :key="error">
              {{ error }}
          </span>
        </b-alert>
      </div>

      <b-alert :show="isLoading" variant="info">Loading...</b-alert>

      <div>
        <vue-good-table
          :columns="table_columns"
          :rows="table_data"
          :search-options="{
            enabled: true
          }"
          :pagination-options="{
            enabled: true
          }">
        >
        <div slot="table-actions">
          	<div slot="table-actions">
            <b-button @click="newItem()">New Method</b-button>
          </div>
        </div>
        
        <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field == 'before'">
            <div class="btn-group" role="group" aria-label="Basic example">
              <button type="button" class="btn btn-primary btn-sm" @click="editItem(props.row.id)">Edit</button>
              <button type="button" class="btn btn-danger btn-sm" @click="deleteItem(props.row.id)">Delete</button>
            </div>
          </span>
          <span v-else>
            {{props.formattedRow[props.column.field]}}
          </span>
        </template>

        </vue-good-table>
      </div>

      <b-modal
        id="modal-edit"
        ref="modal"
        v-model="showEditor"
        :title="model.id ? 'Edit Method ID#' + model.id : 'New Method'"
        @ok="saveItem"
      >
      <form @submit.prevent="saveItem">
        <div v-for="column in table_columns" :key="column.field">
          <b-form-group v-if="(column.field in model) && column.editable" :label="column.label">
            <v-select v-if="'options' in column"
              v-model="model[column.field]"
              :options=getOptions(column) 
              :reduce=column.reduce
              label="name"
            ></v-select>
            <b-form-input v-else
              v-model="model[column.field]"
              type="text"
            >
            </b-form-input> 
          </b-form-group>
        </div>
      </form>
      </b-modal>

    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class Main extends Vue {

  isLoading: Boolean = false
  error: Object = null
  errors: Array<String> = []
  showError : Boolean = false
  table_data = []
  showEditor : Boolean = false
  table_columns = []

  getOptions(column) {
    return column.options(this)
  }

  async newItem() {
  }
  
  editItem(id) {
  }

  async saveItem() {
  }

  async deleteItem(id) {
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
