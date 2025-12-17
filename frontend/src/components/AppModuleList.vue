<template lang="">
    <details class="bg-white p-4 rounded shadow-md">
        <summary><slot></slot></summary>
        <div class="flex flex-col">
            <a
            v-for="item in module_items" 
            :key="item.order_index">{{item.order_index}} {{item.title}}</a>
        </div>
    </details>
</template>
<script>
export default {
    
    props: {
        module_items: {
            type: Array,
            default: []
        }
    },

    methods: {
        getArticleUrl(item) {

        }
    }

}
</script>
<style>    

    
</style>