<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'


import { backend, BackendCompound, BackendMethod } from '../backend'
import { CompoundDescription, MethodDescription, InstrumentDescription, EluentDescription, ColumnDescription } from '../descriptions'
import axios from 'axios'

export default {
  model : {},
  props: ['modelname', 'id', 'modalref'],

  data() {
    console.log("data()")
    console.log("this.modelname = " + this.modelname)
    return {
      descriptions:[],
      model: {},
      methods: [],
      instruments: [],
      eluents: [],
      columns: [],
      self: {},
      showEditor: false,
      search_words : "",
      search_namespace: "name",
      search_compounds: []
    }
  },

  watch: { 
    show: {
      deep: true,
      handler(newValue, oldValue) {
        this.showEditor = true
      }     
    }
  },

  methods: {
    async getModel()
    {
      try {
        console.log("getModel this.modelname = " + this.modelname)
        this.self = this
        if (this.modelname === "method")
        {
          if (this.id === "") {
            this.model = {
              id: '',
              column_id: '',
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
          }
          else {
            let response = await backend.getMethod(this.id)
            this.model = response.data
          }
          await this.refreshEluents()
          await this.refreshColumns()
          await this.refreshInstruments()
          this.descriptions = MethodDescription.getFields()
        }
        else if (this.modelname === "compound")
        {
          if (this.id === "") {
            this.model = {
              id: '',
              column_id: '',
              name: '',
              iupac: '',
              method_id: ''
            }
          }
          else {
            let response = await backend.getCompound(this.id)
            this.model = response.data        
          }
          await this.refreshMethods()
          this.descriptions = CompoundDescription.getFields()
        }
        else if (this.modelname === "instrument")
        {
          if (this.id === "") {
            this.model = {
              id: '',
              name: '',
              model: ''
            }
          }
          else {
            let response = await backend.getInstrument(this.id)
            this.model = response.data        
          }
          this.descriptions = InstrumentDescription.getFields()
        }
        else if (this.modelname === "eluent")
        {
          if (this.id === "") {
            this.model = {
              id: '',
              name: ''
            }
          }
          else {
            let response = await backend.getEluent(this.id)
            this.model = response.data        
          }
          this.descriptions = EluentDescription.getFields()
        }
        else if (this.modelname === "column")
        {
          if (this.id === "") {
            this.model = {
              id: '',
              name: ''
            }
          }
          else {
            let response = await backend.getColumn(this.id)
            this.model = response.data        
          }
          this.descriptions = ColumnDescription.getFields()
        }
      } catch (err) {
        this.parseError(err)
      }
    },

    async refreshMethods() {
      try {
        let response = await backend.getMethods()
        this.methods = response.data
      } catch (err) {
        this.parseError(err)
      }
    },

    async refreshEluents() {
      try {
        let response = await backend.getEluents()
        this.eluents = response.data
      } catch (err) {
        this.parseError(err)
      }
    },

    async refreshInstruments() {
      try {
        let response = await backend.getInstruments()
        this.instruments = response.data
      } catch (err) {
        this.parseError(err)
      }
    },

    async refreshColumns() {
      try {
        let response = await backend.getColumns()
        this.columns = response.data
      } catch (err) {
        this.parseError(err)
      }
    },

    parseError(error) {
      //  this.error = error
      //  this.errors = []
      //  if (error) {
      //    for (let idx in error.response.data.errors) {
      //      this.errors.push(idx + ': ' + error.response.data.errors[idx])
      //    }
      //  }
      console.log(error)
    },

    hideModal() {
      this.modalref().hide();
    },

    async deleteItem() {
      console.log("deleteItem")
      this.$emit('onModelChanged');
      this.hideModal()
    },

    getPubChemProperty(compound, property_label, property_name, value_type) {
      let properties = compound['props']
      for (let property_index in properties)
      {
        let property = properties[property_index]
        console.log(property)
        if ((property['urn']['label'] == property_label) && (property['urn']['name'] == property_name))
        {
          return property['value'][value_type]
        }
      }
    },

    searchPubChem() {
      console.log("search in PubChem Database: " + this.search_words)
      let $axios = axios.create({
        baseURL: 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/',
        timeout: 5000,
        headers: { 'Content-Type': 'application/json' },
      })

      // Response Interceptor to handle and log errors
      $axios.interceptors.response.use(
        function(response) {
          return response
        },
        function(error) {
          // Handle Error
          return Promise.reject(error)
        },
      )

      $axios.get( this.search_namespace + '/' + this.search_words + '/JSON').then((response) => 
      {
        console.log(response.data)
        let pubchem_compounds = response.data['PC_Compounds']
        console.log(pubchem_compounds)
        for (let pubchem_compound_index in pubchem_compounds)
        {
          console.log(pubchem_compound_index)
          let compound = {} 
          let pubchem_compound = pubchem_compounds[pubchem_compound_index]
          console.log(pubchem_compound)
          compound['iupac'] = this.getPubChemProperty(pubchem_compound, 'IUPAC Name', 'Preferred', 'sval')
          console.log(compound)
        }
      })
    },

    async saveItem() {
      console.log("saveItem")
      try {
        if (this.modelname === "compound")
        {
          if (this.model["id"]) {
            await backend.updateCompound(this.model["id"], this.model)
          } else {
            await backend.createCompound(this.model)
          }
        }
        else if (this.modelname === "method")
        {
          if (this.model["id"]) {
            await backend.updateMethod(this.model["id"], this.model)
          } else {
            await backend.createMethod(this.model)
          }
        }
        else if (this.modelname === "instrument")
        {
          if (this.model["id"]) {
            await backend.updateInstrument(this.model["id"], this.model)
          } else {
            await backend.createInstrument(this.model)
          }
        }
        else if (this.modelname === "eluent")
        {
          if (this.model["id"]) {
            await backend.updateEluent(this.model["id"], this.model)
          } else {
            await backend.createEluent(this.model)
          }
        }
        else if (this.modelname === "column")
        {
          if (this.model["id"]) {
            await backend.updateColumn(this.model["id"], this.model)
          } else {
            await backend.createColumn(this.model)
          }
        }
      } catch (err) {
        this.parseError(err)
      }
      this.$emit('onModelChanged');
      this.hideModal()
    }

  },

  beforeMount() {
    this.getModel();
  }
}

</script>

<template>
  <div>
    <form @submit.prevent="saveItem">
      
      <div>
        <b-form-group label="Import from PubChem">
          <div class="form-row">
            <div class="col">
              <b-form-input
                v-model="search_words"
                type="text"
              >
              </b-form-input> 
            </div>
            <div class="col">
              <v-select 
                v-model="search_namespace"
                :options="['cid', 'name', 'smiles', 'sdf', 'inchi', 'inchikey', 'formula']"
                label="namespace"
              ></v-select>
            </div>
            <div class="col">
              <button type="button" class="btn btn-outline-primary btn-sm" @click="searchPubChem()">&#x1f50e;</button>
            </div>
          </div>
        </b-form-group>
      </div>
      <hr/>

      <div v-for="description in descriptions" :key="description.field">
        <b-form-group v-if="(description.field in model) && description.editable" :label="description.label">
          <v-select v-if="'options' in description"
            v-model="model[description.field]"
            :options=description.options(self) 
            :reduce=description.reduce
            label="name"
          ></v-select>
          <b-form-input v-else
            v-model="model[description.field]"
            type="text"
          >
          </b-form-input> 
        </b-form-group>
      </div>
    </form>
    <button type="submit" class="btn btn-secondary" @click="hideModal()">Cancel</button>
    <button type="submit" class="btn btn-danger" @click="deleteItem()">Delete</button>
    <button type="submit" class="btn btn-primary" @click="saveItem()">OK</button>
  </div>
</template>


