
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendMethod, BackendEluent, BackendInstrument, BackendColumn } from '../backend'
import { MethodDescription } from '../descriptions'

const EMPTY_ITEM = {
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

@Component
export default class MethodsList extends Main {
  methods: Array<BackendMethod> = []
  eluents: Array<BackendEluent> = [] // TODO: optimize, we actually only need id and names
  instruments: Array<BackendInstrument> = [] // TODO: optimize, we actually only need id and names
  columns: Array<BackendColumn> = [] // TODO: optimize, we actually only need id and names
  model: BackendMethod = EMPTY_ITEM

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: MethodDescription.getFields(),
    }
  }

  async beforeMount() {
    this.refreshMethods();
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.methods) {
      let method = this.methods[index]
      let row = JSON.parse(JSON.stringify(method))
      row.eluent_a_name = this.getEluentNameFromEluentId(method.eluent_a_id)
      row.eluent_b_name = this.getEluentNameFromEluentId(method.eluent_b_id)
      row.instrument_name = this.getInstrumentNameFromInstrumentId(method.instrument_id)
      row.column_name = this.getColumnNameFromColumnId(method.column_id)
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
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

  async newItem() {
    this.model = EMPTY_ITEM // reset form
    this.showEditor = true;
  }

  editItem(column_name, row_id) {
    let method = this.methods.find(method => method.id === row_id)
    this.model = Object.assign({}, method)
    this.showEditor = true;
  }

  async saveItem() {
    try {
      if (this.model.id) {
        await backend.updateMethod(this.model.id, this.model)
      } else {
        await backend.createMethod(this.model)
      }
      this.model = EMPTY_ITEM // reset form
      await this.refreshMethods()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteItem(id) {
    if (confirm('Are you sure you want to delete this method?')) {
      // if we are editing a methods we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = EMPTY_ITEM
      }
      await backend.deleteMethod(id)
      await this.refreshMethods()
    }
  }

  getEluentNameFromEluentId(eluent_id) {
    var eluent = this.eluents.find(eluent => eluent.id === eluent_id)
    if (typeof eluent !== 'undefined') {
      return eluent.name
    }
    else {
      return ""
    }
  }

  getInstrumentNameFromInstrumentId(instrument_id) {
    var instrument = this.instruments.find(instrument => instrument.id === instrument_id)
    if (typeof instrument !== 'undefined') {
      return instrument.name
    }
    else {
      return ""
    }
  }

  getColumnNameFromColumnId(column_id) {
    var column = this.columns.find(column => column.id === column_id)
    if (typeof column !== 'undefined') {
      return column.name
    }
    else {
      return ""
    }
  }
}
</script>
