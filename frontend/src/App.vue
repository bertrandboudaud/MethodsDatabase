<template>
  <div id="app">
    <b-navbar id="nav">
      <b-navbar-nav>
        <b-nav-item to="/">Home</b-nav-item> |
        <b-nav-item to="/compounds">CompoundsList</b-nav-item> |
        <b-nav-item to="/methods">MethodsList</b-nav-item> |
        <b-nav-item to="/instruments">InstrumentsList</b-nav-item> |
        <b-nav-item to="/eluents">EluentsList</b-nav-item> |
        <b-nav-item to="/columns">ColumnsList</b-nav-item> |
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
