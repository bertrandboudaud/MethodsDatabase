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
          :columns="descriptions"
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
            <b-button class="btn btn-primary" @click="newItem()">&#x1f7a2; Create New</b-button>
          </div>
        </div>
        
        <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field == 'before'">
            <div class="btn-group" role="group" aria-label="Basic example">
              <button type="button" class="btn btn-outline-primary btn-sm" @click="editItem(props.column.field, props.row.id)">&#x1f50e;</button>
            </div>
          </span>
          <span v-if="'hovered' in getDescription(props.column.field)">
            {{props.formattedRow[props.column.field]}}
            <button type="button" class="btn btn-outline-primary btn-sm" @click="editItem(props.column.field, props.row.id)">&#x1f50e;</button>
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
        hide-footer
        hide-header
        size="xl"
    >
      <item :modelname="edit_modelname" :id="edit_id" :modalref="getModalRef" v-on:onModelChanged="onModelChanged"/>
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
  descriptions = []
  edit_descriptions = []

  onModelChanged() {
    console.log("onModelChanged")
    this.showEditor = false;
    this.loadData()
  }

  loadData() {
    console.log("refreshTableData from base class")
  }

  getModalRef() {
    return this.$refs["modal"];
  }

  getEditDescription() {
    return this.edit_descriptions;
  }

  components: {
    Item
  }

  getOptions(column) {
    return column.options(this)
  }

  async newItem() {
  }
  
  editItem(column_name, row_id) {
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

  getDescription(field) {
    return this.descriptions.find(description => description.field === field)
  }
}

</script>
