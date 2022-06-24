
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, BackendCompound, BackendMethod } from '../backend'
import { CompoundDescription, MethodDescription } from '../descriptions'

@Component
export default class CompoundsList extends Main {
  compounds: Array<BackendCompound> = []
  methods: Array<BackendMethod> = [] // TODO: optimize, we actually only need id and names

  data() {
    return {
      showEditor: false,
      showError: false,
      table_data: [],
      descriptions: CompoundDescription.getFields(),
      edit_modelname : "",
      edit_id : ""
    }
  }

  loadData() {
    this.refreshCompounds();
  }

  async beforeMount() {
    this.loadData()
  }

  refreshTableData() {
    let new_table_data = []
    for (let index in this.compounds) {
      let compound = this.compounds[index]
      let row = JSON.parse(JSON.stringify(compound))
      row.method_name = this.getMethodNameFromMethodId(compound.method_id)
      new_table_data.push(row)
    };
    this.table_data = new_table_data;
  }

  async refreshCompounds() {
    this.isLoading = true
    try {
      let response = await backend.getCompounds()
      this.compounds = response.data
      await this.refreshMethods()
    } catch (err) {
      this.parseError(err)
    }
    this.refreshTableData();
    this.isLoading = false
  }

  async refreshMethods() {
    try {
      let response = await backend.getMethods()
      this.methods = response.data
    } catch (err) {
      this.parseError(err)
    }
  }

  async newItem() {
    this.edit_modelname = "compound"
    this.edit_id = ""
    this.showEditor = true
  }

  editItem(column_name, row_id) {
    console.log("editItem " + column_name)
    let compound = this.compounds.find(compound => compound.id === row_id)
    if (column_name === "method_name")
    {
      this.edit_modelname = "method"
      this.edit_id = compound.method_id
    }
    else
    {
      this.edit_modelname = "compound"
      this.edit_id = compound.id
    }
    this.showEditor = true;
  }

  getMethodNameFromMethodId(method_id) {
    var method = this.methods.find(method => method.id === method_id)
    if (typeof method !== 'undefined') {
      return method.name
    }
    else {
      return ""
    }
  }

}
</script>
