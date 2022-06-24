
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendColumn } from '../backend'
import { ColumnDescription } from '../descriptions'

const EMPTY_ITEM = {
  id: '',
  name: ''
}

@Component
export default class ColumnsList extends Main {
  columns: Array<BackendColumn> = []
  model: BackendColumn = EMPTY_ITEM

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: ColumnDescription.getFields(),
    }
  }

  async beforeMount() {
    this.refreshColumns();
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
    this.model = EMPTY_ITEM // reset form
    this.showEditor = true;
  }

  editItem(column_name, row_id) {
    let column = this.columns.find(column => column.id === row_id)
    this.model = Object.assign({}, column)
    this.showEditor = true;
  }

  async saveItem() {
    try {
      if (this.model.id) {
        await backend.updateColumn(this.model.id, this.model)
      } else {
        await backend.createColumn(this.model)
      }
      this.model = EMPTY_ITEM // reset form
      await this.refreshColumns()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteItem(id) {
    if (confirm('Are you sure you want to delete this column?')) {
      if (this.model.id === id) {
        this.model = EMPTY_ITEM
      }
      await backend.deleteColumn(id)
      await this.refreshColumns()
    }
  }

}
</script>

