
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendMethod, BackendEluent, BackendInstrument, BackendColumn } from '../backend'
import { MethodDescription } from '../descriptions'

@Component
export default class MethodsList extends Main {
  methods: Array<BackendMethod> = []
  eluents: Array<BackendEluent> = [] // TODO: optimize, we actually only need id and names
  instruments: Array<BackendInstrument> = [] // TODO: optimize, we actually only need id and names
  columns: Array<BackendColumn> = [] // TODO: optimize, we actually only need id and names

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: MethodDescription.getFields(),
      edit_modelname : "",
      edit_id : ""
    }
  }

  loadData() {
    this.refreshMethods();
  }

  async beforeMount() {
    this.loadData();
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
    this.edit_modelname = "method"
    this.edit_id = ""
    this.showEditor = true
  }

  editItem(column_name, row_id) {
    console.log("editItem " + column_name)
    let method = this.methods.find(method => method.id === row_id)
    if (column_name === "eluent_a_name")
    {
      this.edit_modelname = "eluent"
      this.edit_id = method.eluent_a_id
    }
    else if (column_name === "eluent_b_name")
    {
      this.edit_modelname = "eluent"
      this.edit_id = method.eluent_b_id
    }
    else if (column_name === "instrument_name")
    {
      this.edit_modelname = "instrument"
      this.edit_id = method.instrument_id
    }
    else if (column_name === "column_name")
    {
      this.edit_modelname = "column"
      this.edit_id = method.column_id
    }
    else
    {
      this.edit_modelname = "method"
      this.edit_id = method.id
    }
    this.showEditor = true;
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
