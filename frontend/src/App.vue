<template>
  <div id="app">
    <b-navbar id="nav">
      <b-navbar-nav>
        <b-nav-item to="/">Home</b-nav-item> |
        <b-nav-item to="/compounds">Compounds</b-nav-item> |
        <b-nav-item to="/methods">Methods</b-nav-item> |
        <b-nav-item to="/users">Users</b-nav-item> |
        <b-nav-item to="/instruments">Instruments</b-nav-item> |
        <b-nav-item to="/eluents">Eluents</b-nav-item> |
        <b-nav-item to="/columns">Columns</b-nav-item> |
      </b-navbar-nav>
    </b-navbar>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
