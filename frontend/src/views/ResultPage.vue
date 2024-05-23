<template>
  <div>
    <h1>策略结果</h1>
    <result-chart :data="chartData"></result-chart>
    <result-table :data="tableData"></result-table>
  </div>
</template>

<script>
import ResultChart from '../components/ResultChart.vue';
import ResultTable from '../components/ResultTable.vue';
import axios from 'axios';

export default {
  components: {
    ResultChart,
    ResultTable
  },
  data() {
    return {
      chartData: {
        dates: [],
        values: []
      },
      tableData: []
    };
  },
  async created() {
    const strategyId = this.$route.query.id;
    const response = await axios.get(`/api/strategy_result/${strategyId}`);
    this.chartData = response.data.chartData;
    this.tableData = response.data.tableData;
  }
};
</script>
