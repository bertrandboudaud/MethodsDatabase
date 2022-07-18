<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'


import { backend, BackendCompound, BackendMethod } from '../backend'
import { CompoundDescription, MethodDescription, InstrumentDescription, EluentDescription, ColumnDescription } from '../descriptions'
import axios from 'axios'

export default {

  data() {
    return {
    }
  },

  methods: {
    async login() {
      await backend.login("user", "password")
    }
  }
}

</script>

<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">DTU Methods Database</h1>
      <button type="button" class="btn btn-outline-primary btn-sm" @click="login()">Login</button>
    </div>
  </div>
</template>
