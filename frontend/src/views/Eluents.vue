
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, Eluent } from '../backend'

const EMPTY_ITEM = {
  id: '',
  name: ''
}

@Component
export default class Eluents extends Main {
  eluents: Array<Eluent> = []
  model: Eluent = EMPTY_ITEM

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
        }
      ],
      table_data: []
    }
  }

  async beforeMount() {
    this.refreshEluents();
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.eluents) {
      let eluent = this.eluents[index]
      let row = JSON.parse(JSON.stringify(eluent))
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
  }

  async refreshEluents() {
    this.isLoading = true
    try {
      let response = await backend.getEluents()
      this.eluents = response.data
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
    let eluent = this.eluents.find(eluent => eluent.id === id)
    this.model = Object.assign({}, eluent)
    this.showEditor = true;
  }

  async saveItem() {
    try {
      if (this.model.id) {
        await backend.updateEluent(this.model.id, this.model)
      } else {
        await backend.createEluent(this.model)
      }
      this.model = EMPTY_ITEM // reset form
      await this.refreshEluents()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteItem(id) {
    if (confirm('Are you sure you want to delete this eluent?')) {
      if (this.model.id === id) {
        this.model = EMPTY_ITEM
      }
      await backend.deleteEluent(id)
      await this.refreshEluents()
    }
  }

}
</script>

