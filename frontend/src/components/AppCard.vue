<template>
  <a :href="url" style="display: block;">
    <div class="p-5 rounded-lg bg-neutral-300 shadow shadow-neutral-500 hover:scale-105
      transition-transform duration-200
      ease-in-out" :style="{
        width: width + 'px',
        height: height + 'px'
      }">
      <h3 class="inter-font-bold mb-0">{{ title }}</h3>
      <p class="inter-font">{{ subtitle }}</p>
    </div>
  </a>
</template>


<script>
  export default {
    props: {
      width: {
        type: Number,
        default: 300
      },
      height: {
        type: Number,
        default: 300
      },
      url: {
        type: String,
        default: "/"
      },
      title: {
        type: String,
        default: ""
      },
      subtitle: {
        type: String,
        default: ""
      }
    }
  }

</script>
<style>
.inter-font {
  font-family: "Inter", sans-serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
}

.inter-font-bold {
  font-family: "Inter", sans-serif;
  font-optical-sizing: auto;
  font-weight: 700;
  font-size: 24;
}
</style>