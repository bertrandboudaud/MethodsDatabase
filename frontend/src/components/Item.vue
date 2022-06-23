<script lang="ts">

export default {
  props: ['description', 'model', 'options']
}

</script>

<template>
  <div>
    <form @submit.prevent="saveItem">
      <div v-for="column in description" :key="column.field">
        <b-form-group v-if="(column.field in model) && column.editable" :label="column.label">
          <v-select v-if="'options' in column"
            v-model="model[column.field]"
            :options=options(column) 
            :reduce=column.reduce
            label="name"
          ></v-select>
          <b-form-input v-else
            v-model="model[column.field]"
            type="text"
          >
          </b-form-input> 
        </b-form-group>
      </div>
    </form>
  </div>
</template>


