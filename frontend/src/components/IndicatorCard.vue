<template>
  <el-card class="indicator-card">
    <h3>{{ indicator.name }}</h3>
    <p>{{ indicator.description }}</p>
  </el-card>
</template>

<script>
export default {
  props: {
    indicator: Object
  }
}
</script>

<style scoped>
.indicator-card {
  margin-bottom: 20px;
}
</style>
