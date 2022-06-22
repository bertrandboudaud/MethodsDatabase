
<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import Main from '@/components/Main.vue'
import { backend, Compound, Eluent, Instrument, Column } from '../backend'

const EMPTY_ITEM = {
  id: '',
  column_id: '',
  name: '',
  iupac: '',
  method_id: ''
}

@Component
export default class Compounds extends Main {
  compounds: Array<Compound> = []
  methods: Array<Method> = [] // TODO: optimize, we actually only need id and names
  model: Compound = EMPTY_ITEM

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
          field: "iupac",
          label: "iupac",
          align: "center",
          type: 'string',
          hidden: false,
          editable: true
        },
        {
          field: "method_id",
          label: "method",
          align: "center",
          type: 'string',
          hidden: true,
          editable: true,
          options: function (self) { return self.methods },
          reduce: function (method) { return method.id; } 
        },
        {
          field: "method_name",
          label: "method",
          align: "center",
          type: 'string',
          hidden: false,
          editable: false
        }
      ],
      table_data: []
    }
  }

  async beforeMount() {
    this.refreshCompounds();
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
      await this.refreshMethods();
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
    this.model = EMPTY_ITEM // reset form
    this.showEditor = true;
  }

  editItem(id) {
    let compound = this.compounds.find(compound => compound.id === id)
    this.model = Object.assign({}, compound)
    this.showEditor = true;
  }

  async saveItem() {
    try {
      if (this.model.id) {
        await backend.updateCompound(this.model.id, this.model)
      } else {
        await backend.createCompound(this.model)
      }
      this.model = EMPTY_ITEM // reset form
      await this.refreshCompounds()
    } catch (err) {
      this.parseError(err)
    }
  }

  async deleteItem(id) {
    if (confirm('Are you sure you want to delete this compound?')) {
      // if we are editing a compounds we deleted, remove it from the form
      if (this.model.id === id) {
        this.model = EMPTY_ITEM
      }
      await backend.deleteCompound(id)
      await this.refreshCompounds()
    }
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
