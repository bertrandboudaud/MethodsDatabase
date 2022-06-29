
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendEluent } from '../backend'
import { EluentDescription } from '../descriptions'

@Component
export default class EluentsList extends Main {
  eluents: Array<BackendEluent> = []

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: EluentDescription.getFields(),
      edit_modelname : "",
      edit_id : ""
    }
  }

  loadData() {
    this.refreshEluents();
  }

  async beforeMount() {
    this.loadData();
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
    this.edit_modelname = "eluent"
    this.edit_id = ""
    this.showEditor = true
  }

  editItem(column_name, row_id) {
    console.log("editItem " + column_name)
    let eluent = this.eluents.find(eluent => eluent.id === row_id)
    this.edit_modelname = "eluent"
    this.edit_id = eluent.id
    this.showEditor = true;
  }

}
</script>

