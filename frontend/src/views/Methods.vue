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
      
      <ve-table :columns="table_columns" :table-data="table_data" :sort-option="sortOption" ></ve-table>

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
            title: "id",
            align: "center",
            sortBy: "",
        },
        {
            field: "name",
            key: "name",
            title: "name",
            align: "center",
            sortBy: "",
        },
        {
            field: "technique",
            key: "technique",
            title: "technique",
            align: "center",
            sortBy: "",
        },
        {
            field: "comment",
            key: "comment",
            title: "comment",
            align: "center",
            sortBy: "",
        },
        {
            field: "analysis_method",
            key: "analysis_method",
            title: "analysis_method",
            align: "center",
            sortBy: "",
        },
        {
            field: "eluent_a",
            key: "eluent_a",
            title: "eluent_a",
            align: "center",
            sortBy: "",
        },
        {
            field: "eluent_b",
            key: "eluent_b",
            title: "eluent_b",
            align: "center",
            sortBy: "",
        },
        {
            field: "instrument",
            key: "instrument",
            title: "instrument",
            align: "center",
            sortBy: "",
        },
        {
            field: "column",
            key: "column",
            title: "column",
            align: "center",
            sortBy: "",
        },
        {
            field: "lod",
            key: "lod",
            title: "lod",
            align: "center",
            sortBy: "",
        },
        {
            field: "lloq",
            key: "lloq",
            title: "lloq",
            align: "center",
            sortBy: "",
        },
        {
            field: "uloq",
            key: "uloq",
            title: "uloq",
            align: "center",
            sortBy: "",
        },
        {
            field: "precision",
            key: "precision",
            title: "precision",
            align: "center",
            sortBy: "",
        },
        {
            field: "preferred_sample_volume",
            key: "preferred_sample_volume",
            title: "preferred_sample_volume",
            align: "center",
            sortBy: "",
        },
        {
            field: "runtime",
            key: "runtime",
            title: "runtime",
            align: "center",
            sortBy: "",
        },
        {
            field: "price",
            key: "price",
            title: "price",
            align: "center",
            sortBy: "",
        },
      ],
      table_data: []
    }
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

  compare(order, a, b)
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
      console.log(this.table_data)
      this.table_data.sort((a, b) => {
        if (params.name)
        {
          return this.compareString(params.name, a.name, b.name)
        }
        else if (params.technique)
        {
          return this.compareString(params.technique, a.technique, b.technique)
        }
        else if (params.id)
        {
          return this.compareString(params.id, a.id, b.id)
        }
        else if (params.comment)
        {
          return this.compareString(params.comment, a.comment, b.comment)
        }
        else if (params.analysis_method)
        {
          return this.compareString(params.analysis_method, a.analysis_method, b.analysis_method)
        }
        else if (params.eluent_a)
        {
          return this.compareString(params.eluent_a, a.eluent_a, b.eluent_a)
        }
        else if (params.eluent_b)
        {
          return this.compareString(params.eluent_b, a.eluent_b, b.eluent_b)
        }
        else if (params.instrument)
        {
          return this.compareString(params.instrument, a.instrument, b.instrument)
        }
        else if (params.column)
        {
          return this.compareString(params.column, a.column, b.column)
        }
        else if (params.lod)
        {
          return this.compare(params.lod, a.lod, b.lod)
        }
        else if (params.lloq)
        {
          return this.compare(params.lloq, a.lloq, b.lloq)
        }
        else if (params.uloq)
        {
          return this.compare(params.uloq, a.uloq, b.uloq)
        }
        else if (params.precision)
        {
          return this.compare(params.precision, a.precision, b.precision)
        }
        else if (params.preferred_sample_volume)
        {
          return this.compare(params.preferred_sample_volume, a.preferred_sample_volume, b.preferred_sample_volume)
        }
        else if (params.runtime)
        {
          return this.compare(params.runtime, a.runtime, b.runtime)
        }
        else if (params.price)
        {
          return this.compare(params.price, a.price, b.price)
        }
      });
      console.log(this.table_data)
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
