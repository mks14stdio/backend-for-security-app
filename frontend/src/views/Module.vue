<template lang="">
    <AppHeader>Модуль</AppHeader>
    
  <n-card content-style="padding: 0;">
    <n-h1>Hello World</n-h1>
  </n-card>

</template>
<script>
import AppHeader from "@/components/AppHeader.vue"
import AppModuleList from "@/components/AppModuleList.vue";

import { articleService } from "@/api/service";
import { NButton } from "naive-ui";
import { NCard, NTabs, NTabPane } from "naive-ui";


export default {

    methods: {
        async fetchData() {
            try {
                const responce = await articleService.get_all(10, 0); 
            } catch(e) {
                console.log(e);
            }
        }
    },

    components: {
        AppHeader,
        AppModuleList,
        NCard, NTabs, NTabPane
    },

    mounted() {
        console.log("Module view mounted");
    },
    

    data() {
        return {
            arr: [
                {
                    order_index: 4,
                    title: "Hello World",
                    article_id: 0,
                },
                {
                    order_index: 3,
                    title: "Hello World",
                    article_id: 0,
                },
                {
                    order_index: 2,
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
<style lang="">
    
</style>