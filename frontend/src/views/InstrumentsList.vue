
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendInstrument } from '../backend'
import { InstrumentDescription } from '../descriptions'

@Component
export default class InstrumentsList extends Main {
  instruments: Array<BackendInstrument> = []

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: InstrumentDescription.getFields(),
      edit_modelname : "",
      edit_id : ""
    }
  }

  loadData() {
    this.refreshInstruments();
  }

  async beforeMount() {
    this.loadData();
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.instruments) {
      let instrument = this.instruments[index]
      let row = JSON.parse(JSON.stringify(instrument))
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
  }

  async refreshInstruments() {
    this.isLoading = true
    try {
      let response = await backend.getInstruments()
      this.instruments = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.refreshTableData();
    this.isLoading = false
  }

  async newItem() {
    this.edit_modelname = "instrument"
    this.edit_id = ""
    this.showEditor = true
  }

  editItem(column_name, row_id) {
    console.log("editItem " + column_name)
    let instrument = this.instruments.find(instrument => instrument.id === row_id)
    this.edit_modelname = "instrument"
    this.edit_id = instrument.id
    this.showEditor = true;
  }

}
</script>

