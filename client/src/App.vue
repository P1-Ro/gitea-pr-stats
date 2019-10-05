<template>
  <div id="app">
    <b-navbar>
      <template slot="brand">
        <b-navbar-item tag="router-link" :to="{ path: '/report' }">
          <img
            src="https://vuejs.org/images/logo.png"
            alt="Vue.js"
          >
        </b-navbar-item>
      </template>
      <template slot="start">
        <b-navbar-item tag="router-link" :to="{path: '/report'}">
          Reports
        </b-navbar-item>
      </template>

<!--      <template slot="end">
        <b-navbar-item tag="div">
          <div class="buttons">
            <router-link class="button is-primary" to="/login">
              <strong>Log in</strong>
            </router-link>
          </div>
        </b-navbar-item>
      </template>-->
    </b-navbar>
    <router-view/>
  </div>
</template>

<style lang="less">
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;

    a {
      font-weight: bold;
      color: #2c3e50;

      &.router-link-exact-active {
        color: #42b983;
      }
    }
  }
</style>
