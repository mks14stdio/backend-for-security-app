<template>
  <div class="flex flex-col gap-4 items-center-safe pt-10">
    <div class="bg-white p-4 rounded shadow-md gap-2 flex flex-col w-80">
        <h1>Авторизация</h1>
        <form class="flex flex-col gap-2" @submit.prevent="login">
            <input type="email" v-model="form.email" placeholder="Почта" required />
            <input type="password" v-model="form.password" placeholder="Пароль" required />
            <input class="bg-neutral-200 hover:bg-neutral-100" type="submit" value="Войти"/>
            <span v-show="error">Неверный логин или пароль</span>
        </form>
      </div>
  </div>
</template>

<script>

import service from "@/api/service"
import router from "@/router";

export default {
  data() {
    return {
      form: {
        email: "",
        password: "",
      },
      error: false

    }
  },

  methods: {
    async login() {
      console.log(this.form.email);
      console.log(this.form.password);

      const flag = await service.authService.login(this.form.email, this.form.password);

      if (flag) {
        router.push("/");
      } else {
        this.error = true;
      }

    }
  }

}
</script>
<style lang="">
    
</style>