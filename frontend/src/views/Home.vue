<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'


import { backend, BackendCompound, BackendMethod } from '../backend'
import { CompoundDescription, MethodDescription, InstrumentDescription, EluentDescription, ColumnDescription } from '../descriptions'
import axios from 'axios'

export default {

  data() {
    return {
      username : "",
      password : ""
    }
  },

  methods: {
    async login(username, password) {
      await backend.login(username, password)
    }
  }
}

</script>

<template>
  <div>
    <div class="container-fluid mt-4">
      <h1 class="h1">DTU Methods Database</h1>

        <b-card :title="Login">
          <form @submit.prevent="login(username, password)">
            <b-form-group label="Username">
              <b-form-input
                v-model="username"
                type="text"
              ></b-form-input>
            </b-form-group>
            <b-form-group label="password">
              <b-form-textarea
                v-model="password"
                type="text"
              ></b-form-textarea>
            </b-form-group>
            <div>
              <b-btn type="submit" variant="success">Login</b-btn>
            </div>
          </form>
        </b-card>
    </div>
  </div>
</template>
