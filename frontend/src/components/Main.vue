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
      <item :model="model" :options="getOptions" :description="getTableColumn()" />
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

  getTableColumn()
  {
    return this.table_columns;
  }

  components: {
    Item
  }

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
