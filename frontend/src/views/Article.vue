<template lang="">
    <AppHeader>Статьи</AppHeader>
    
    <AppModuleList :module_items="arr">Модуль Первый</AppModuleList>

</template>

<script>
import AppHeader from "../components/AppHeader.vue"
import AppModuleList from "@/components/AppModuleList.vue";

export default {
    components: {
        AppHeader,
        AppModuleList
    },

    data() {
        return {
            arr: [
                {
                    order_index: 0,
                    title: "Hello World",
                    article_id: 0,
                },
                {
                    order_index: 0,
                    title: "Hello World",
                    article_id: 0,
                },
                {
                    order_index: 3,
                    title: "World",
                    article_id: 0,
                },
                {
                    order_index: 1,
                    title: "Hello",
                    article_id: 0,
                }
            ]
        }
    }
}
</script>

<style></style>