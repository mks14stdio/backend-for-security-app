import Main from "../views/Main.vue";
import Article from "../views/Article.vue";
import Login from "../views/Login.vue";
import Module from "../views/Module.vue";
import Tests from "../views/Tests.vue";

import { createRouter, createWebHistory } from "vue-router";
import { requireAuth, requireEditor, requireGuest, requireAdmin, requireAdminOrEditor } from "./guards";

const routes = [
    {
        path: '/login',
        name: "Login",
        component: Login,
        beforeEnter: requireGuest
    },
    {
        path: '/',
        name: "Main",
        component: Main,

    },
    {
        path: '/article',
        name: "Article",
        component: Article,
    },
    {
        path: '/module',
        name: "Module",
        component: Module,
    },
    {
        path: '/tests',
        name: "Tests",
        component: Tests,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

/**
 * Global navigation guard to ensure auth checks
 */
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')

    if (to.path !== '/login' && !token) {
        next('/login')
    } 
    else if (to.path === '/login' && token) {
        next('/')
    } 
    else {
        next()
    }
})

export default router;