
<template>
  <header class="header p-4">
    <div class="flex flex-row">
      <img src="/home.svg"/>

    <h1 class="ml-1.5 header-title"><slot></slot></h1>
    <AppButton>Войти</AppButton>
    </div>
  </header>
</template>

<script>
import AppButton from './AppButton.vue';
import { RouterLink } from 'vue-router'

export default {
  components: {
    AppButton,

  }
}
</script>

<style lang="">
    
</style>