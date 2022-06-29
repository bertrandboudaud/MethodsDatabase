
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendColumn } from '../backend'
import { ColumnDescription } from '../descriptions'

@Component
export default class ColumnsList extends Main {
  columns: Array<BackendColumn> = []

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: ColumnDescription.getFields(),
      edit_modelname : "",
      edit_id : ""
    }
  }

  loadData() {
    this.refreshColumns();
  }

  async beforeMount() {
    this.loadData();
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.columns) {
      let column = this.columns[index]
      let row = JSON.parse(JSON.stringify(column))
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
  }

  async refreshColumns() {
    this.isLoading = true
    try {
      let response = await backend.getColumns()
      this.columns = response.data
    } catch (err) {
      this.parseError(err)
    }
    this.refreshTableData();
    this.isLoading = false
  }

  async newItem() {
    this.edit_modelname = "column"
    this.edit_id = ""
    this.showEditor = true
  }

  editItem(column_name, row_id) {
    console.log("editItem " + column_name)
    let column = this.columns.find(column => column.id === row_id)
    this.edit_modelname = "column"
    this.edit_id = column.id
    this.showEditor = true;
  }

}
</script>

