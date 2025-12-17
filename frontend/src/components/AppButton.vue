<template lang="">
    <button class="ml-auto flex items-center border border-neutral-600 rounded-lg bg-neutral-300 shadow shadow-neutral-500 h-11 my-auto">
      <div class="flex flex-row hover:scale-105 transition-transform duration-200 ease-in-out p-2">
        <img src="/login.svg"/>
        <div class="p-2 inter-font"><slot></slot></div>
      </div>
    </button>
</template>
<script>
export default {
    
}
</script>
<style lang=""> 

</style>