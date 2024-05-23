<template>
  <el-container>
    <el-header>
      <h1>策略输入</h1>
    </el-header>
    <el-main>
      <el-card>
        <strategy-form></strategy-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
import StrategyForm from '../components/StrategyForm.vue';

export default {
  components: {
    StrategyForm
  }
};
</script>

<style scoped>
h1 {
  margin: 0;
  padding: 20px;
  text-align: center;
}
</style>
