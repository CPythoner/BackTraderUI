<template>
  <el-table :data="data" style="width: 100%">
    <el-table-column prop="date" label="日期"></el-table-column>
    <el-table-column prop="value" label="数值"></el-table-column>
  </el-table>
</template>

<script>
export default {
  props: ['data']
};
</script>
