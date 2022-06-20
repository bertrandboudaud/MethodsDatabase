
<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">Methods</h1>
      <b-alert :show="isLoading" variant="info">Loading...</b-alert>

    <div class="btn-group">
        <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown">Primary</button>
        <div class="dropdown-menu">
            <a href="#" class="dropdown-item">Action</a>
            <a href="#" class="dropdown-item">Another action</a>
            <div class="dropdown-divider"></div>
            <a href="#" class="dropdown-item">Separated link</a>
        </div>
    </div>

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
            <div class="btn-group">
              <button type="button" class="btn btn-secondary dropdown-toggle" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                Show Column
              </button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                <li v-for="(column, index) in table_columns" :key="column.key" >
                  <a class="dropdown-item" href="#">
                 <!-- <a href="#" class="small" tabIndex="-1" @click.prevent="toggleColumn( index, $event )">
                  <input :checked="!column.hidden" type="checkbox"/>-->
                    <!--&nbsp;{{column.label}}-->
                    {{ index }}: {{ column.key }}
                  <!--</a> -->
                  </a>
                </li>
              </ul>
            </div>
            <b-button @click="newMethod()">New Method</b-button>
          </div>
        </div>
        </vue-good-table>
      </div>

      <b-modal
        id="modal-edit"
        ref="modal"
        v-model="modalShow"
        :title="model.id ? 'Edit Method ID#' + model.id : 'New Compound'"
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
          <b-form-group label="column">
            <v-select
              v-model="model.column_id"
              :options="columns" 
              :reduce="column => column.id"
              label="name"
            ></v-select>
          </b-form-group>
          <b-form-group label="lod">
            <b-form-input
              v-model="model.lod"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="lloq">
            <b-form-input
              v-model="model.lloq"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="uloq">
            <b-form-input
              v-model="model.uloq"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="precision">
            <b-form-input
              v-model="model.precision"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="preferred_sample_volume">
            <b-form-input
              v-model="model.preferred_sample_volume"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="runtime">
            <b-form-input
              v-model="model.runtime"
              type="number"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="price">
            <b-form-input
              v-model="model.price"
              type="number"
            ></b-form-input>
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

import { backend, Method, Eluent, Instrument, Column } from '../backend'

const NO_METHOD = { 
  id: '', 
  name: '', 
  technique: '', 
  comment: '', 
  analysis_method: '', 
  eluent_a_id: '', 
  eluent_b_id: '',
  instrument_id: '',
  lod: 0,
  lloq: 0,
  uloq: 0,
  precision: 0,
  preferred_sample_volume: 0,
  runtime: 0,
  price: 0
 }

@Component
export default class Home extends Vue {
  isLoading: Boolean = false
  methods: Array<Method> = []
  eluents: Array<Eluent> = [] // TODO: optimize, we actually only need id and names
  instruments: Array<Instrument> = [] // TODO: optimize, we actually only need id and names
  columns: Array<Column> = [] // TODO: optimize, we actually only need id and names
  model: Method = NO_METHOD
  error: Object = null
  errors: Array<String> = []
  filter: Object = { name: '' }
  showError : Boolean = false
  table_data = []
  modalShow : Boolean = false
  table_columns = []

  data() {
    return {
      modalShow : false,
      showError : false,
      sortOption: {
          sortChange: (params) => {
              console.log("sortChange::", params);
              this.sortChange(params);
          },
      },
      table_columns : [
        {
            field: "id",
            key: "id",
            label: "id",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "name",
            key: "name",
            label: "name",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "technique",
            key: "technique",
            label: "technique",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "comment",
            key: "comment",
            label: "comment",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "analysis_method",
            key: "analysis_method",
            label: "analysis_method",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "eluent_a",
            key: "eluent_a",
            label: "eluent_a",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "eluent_b",
            key: "eluent_b",
            label: "eluent_b",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "instrument",
            key: "instrument",
            label: "instrument",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "column",
            key: "column",
            label: "column",
            align: "center",
            sortBy: "",
            type: 'string',
            sortFunction: this.compareString,
            hidden: false
        },
        {
            field: "lod",
            key: "lod",
            label: "lod",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "lloq",
            key: "lloq",
            label: "lloq",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "uloq",
            key: "uloq",
            label: "uloq",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "precision",
            key: "precision",
            label: "precision",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "preferred_sample_volume",
            key: "preferred_sample_volume",
            label: "preferred_sample_volume",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "runtime",
            key: "runtime",
            label: "runtime",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
        {
            field: "price",
            key: "price",
            label: "price",
            align: "center",
            sortBy: "",
            type: 'decimal',
            sortFunction: this.compareNumber,
            hidden: false
        },
      ],
      table_data: []
    }
  }

  toggleColumn( index, event ){
      // Set hidden to inverse of what it currently is
      this.$set( this.table_columns[ index ], 'hidden', ! this.table_columns[ index ].hidden );
  }

  compareString(order, a, b)
  {
    if (order === "asc") {
        return a.localeCompare(b);
    } else if (order === "desc") {
        return b.localeCompare(a);
    } else {
        return 0;
    }
  }

  compareNumber(order, a, b)
  {
    if (order === "asc") {
        return a - b;
    } else if (order === "desc") {
        return b - a;
    } else {
        return 0;
    }
  }

  sortChange(params) {
    for (let table_column_index in this.table_columns) {
      let table_column = this.table_columns[table_column_index]
      console.log(table_column)
      let table_column_name = table_column.field
      if (params[table_column_name])
      {
        this.table_data.sort((a, b) => {
          return table_column.sortFunction(params[table_column_name], a[table_column_name], b[table_column_name])
        })
        break
      }
    }
  }

  async beforeMount() {
    this.filter = { name: '' };
    this.refreshMethods();
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.methods)
    {
      let method = this.methods[index]
      let row = JSON.parse(JSON.stringify(method))
      console.log(method);
      console.log(row);
      row.eluent_a = this.getEluentNameFromEluentId(method.eluent_a_id)
      row.eluent_b = this.getEluentNameFromEluentId(method.eluent_b_id)
      row.instrument = this.getInstrumentNameFromInstrumentId(method.instrument_id)
      row.column = this.getColumnNameFromColumnId(method.column_id)
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
    console.log(this.table_data)
  }

  async refreshMethods() {
    this.isLoading = true
    try {
      let response = await backend.getMethods()
      this.methods = response.data
      await this.refreshEluents();
      await this.refreshInstruments();
      await this.refreshColumns();
    } catch (err) {
      this.parseError(err)
    }
    this.refreshTableData();
    this.isLoading = false
  }

  async refreshEluents() {
    try {
      let response = await backend.getEluents()
      this.eluents = response.data
    } catch (err) {
      this.parseError(err)
    }
  }

  async refreshInstruments() {
    try {
      let response = await backend.getInstruments()
      this.instruments = response.data
    } catch (err) {
      this.parseError(err)
    }
  }

  async refreshColumns() {
    try {
      let response = await backend.getColumns()
      this.columns = response.data
    } catch (err) {
      this.parseError(err)
    }
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

  getInstrumentNameFromInstrumentId(instrument_id)
  {
    var instrument =  this.instruments.find(instrument => instrument.id === instrument_id)
    if (typeof instrument !== 'undefined')
    {
      return instrument.name
    }
    else
    {
      return ""
    }
  }

  getColumnNameFromColumnId(column_id)
  {
    var column =  this.columns.find(column => column.id === column_id)
    if (typeof column !== 'undefined')
    {
      return column.name
    }
    else
    {
      return ""
    }
  }
}
</script>
