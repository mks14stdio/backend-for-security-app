<template lang="">
    <details class="mt-3 group bg-white rounded-xl shadow-lg overflow-hidden transition-all duration-300">
      <summary class="cursor-pointer select-none px-5 py-4 font-semibold text-lg
             bg-linear-to-r from-slate-100 to-slate-200
             hover:from-slate-200 hover:to-slate-300
             transition-all duration-300"><slot></slot></summary>
      <div class="flex flex-col gap-2 px-4 py-3
             animate-fade-in" v-for="item in sortedItems" :key="item.order_index">
        <a
          class="group/item flex items-center gap-3
                p-4 rounded-xl bg-white
                shadow-sm border border-slate-200
                hover:shadow-md hover:-translate-y-0.5
                transition-all duration-300 ease-out">
          <span
            class="flex items-center justify-center
                  w-8 h-8 rounded-full
                  bg-slate-100 text-slate-600 font-bold
                  group-hover/item:bg-blue-500
                  group-hover/item:text-white
                  transition-colors duration-300">
            {{ item.order_index }}
          </span>
          <span class="text-slate-800 font-medium">
            {{ item.title }}
          </span>
        </a>
      </div>
      
      <div class="flex flex-col gap-2 px-4 py-3
             animate-fade-in">
                <button @click="add_new_artcle"
          class="m-auto group/item flex items-center gap-3
                p-4 rounded-xl bg-white
                shadow-sm border border-slate-200
                hover:shadow-md hover:-translate-y-0.5
                transition-all duration-300 ease-out">
            +
    </button>
    </div>

    </details>
</template>
<script>
export default {

  props: {
    module_items: {
      type: Array,
      default: () => []
    }
  },

  methods: {
    getArticleUrl(item) {

    },

    add_new_artcle() {
        console.log("Hello World");
    }

  },

  computed: {
    sortedItems() {
      return [...this.module_items].sort(
        (a, b) => a.order_index - b.order_index
      )
    }
  }

}
</script>
<style>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.35s ease-out;
}

/* Плавное раскрытие details */
details>div {
  transition: all 0.3s ease;
}

details:not([open])>div {
  opacity: 0;
  transform: translateY(-6px);
  pointer-events: none;
}
</style>