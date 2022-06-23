
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendInstrument } from '../backend'

const EMPTY_ITEM = {
  id: '',
  name: '',
  model: ''
}

@Component
export default class InstrumentsList extends Main {
  instruments: Array<BackendInstrument> = []
  model: BackendInstrument = EMPTY_ITEM

  data() {
    return {
      showEditor: false,
      showError: false,
      table_columns: [
        {
          label: 'action',
          field: 'before'
        },
        {
          field: "id",
          label: "id",
          align: "center",
          type: 'string',
          hidden: true,
          editable: false
        },
        {
          field: "name",
          label: "name",
          align: "center",
          type: 'string',
          hidden: false,
          editable: true
        },
        {
          field: "model",
          label: "model",
          align: "center",
          type: 'string',
          hidden: false,
          editable: true
        }
      ],
      table_data: []
    }
  }

  async beforeMount() {
    this.refreshInstruments();
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
    this.model = EMPTY_ITEM // reset form
    this.showEditor = true;
  }

  editItem(id) {
    let instrument = this.instruments.find(instrument => instrument.id === id)
    this.model = Object.assign({}, instrument)
    this.showEditor = true;
  }

  async saveItem() {
    try {
      if (this.model.id) {
        await backend.updateInstrument(this.model.id, this.model)
      } else {
        await backend.createInstrument(this.model)
      }
      this.model = EMPTY_ITEM // reset form
      await this.refreshInstruments()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteItem(id) {
    if (confirm('Are you sure you want to delete this instrument?')) {
      if (this.model.id === id) {
        this.model = EMPTY_ITEM
      }
      await backend.deleteInstrument(id)
      await this.refreshInstruments()
    }
  }

}
</script>

