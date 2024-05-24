<template>
  <el-container>
    <el-main class="main-content">
      <el-row :gutter="20">
        <el-col :span="8" v-for="indicator in indicators" :key="indicator.name">
          <indicator-card :indicator="indicator"></indicator-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
import IndicatorCard from '../components/IndicatorCard.vue';

export default {
  components: {
    IndicatorCard
  },
  data() {
    return {
      indicators: []
    };
  },
  mounted() {
    this.fetchIndicators();
  },
  methods: {
    async fetchIndicators() {
      try {
        const response = await axios.get('/api/indicators/');
        this.indicators = response.data;
      } catch (error) {
        console.error('Failed to fetch indicators:', error);
        this.$message.error('获取指标列表失败');
      }
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 20px;
}
</style>
