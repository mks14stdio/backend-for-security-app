import Main from "../views/Main.vue";
import Article from "../views/Article.vue";
import Login from "../views/Login.vue";
import Module from "../views/Module.vue";
import Tests from "../views/Tests.vue";

import { createRouter, createWebHistory } from "vue-router";

const routes = [  // ← исправлено: routes вместо routers
    {
        path: '/',
        name: "Main",
        component: Main
    },
    {
        path: '/article',
        name: "Article",
        component: Article
    },
    {
        path: '/login',
        name: "Login",
        component: Login
    },
    {
        path: '/module',
        name: "Module",
        component: Module
    },
    {
        path: '/tests',
        name: "Tests",
        component: Tests
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes  // ← исправлено: routes вместо routers
})

export default router;