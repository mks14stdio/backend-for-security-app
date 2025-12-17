


<template>

  <AppHeader>
    Главная страница
  </AppHeader>
  
  <div class="flex flex-wrap gap-7.5">
    <AppCard url="/module"  width=300 height=170 title="Модуль" subtitle="Редактор" />
    <AppCard url="/article" width=300 height=170 title="Статьи" subtitle="Редактор" />
    <AppCard url="/tests" width=300 height=170 title="Тесты" subtitle="Редактор" />
    <AppCard url="/" width=300 height=170 title="Пользователи" subtitle="Админ" />
  </div>

</template>

<script>
import AppHeader from "../components/AppHeader.vue"
import AppCard from "../components/AppCard.vue";

export default {

  components: {
    AppHeader,
    AppCard
  },

  data() {
  },

}
</script>

<style>

.header-title {
  font-family: "Source Code Pro", monospace;
  font-optical-sizing: auto;
  font-size: 32px;
  font-weight: 400;
  font-style: normal;
}

.inter-font {
  font-family: "Inter", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

</style>
