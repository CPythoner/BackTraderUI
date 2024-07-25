<template>
  <div class="common-layout" id="app">
    <el-container class="full-height">
      <el-aside width="200px">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-vertical-demo"
          @select="handleSelect"
        >
          <el-menu-item index="1">
            <i class="el-icon-data-analysis"></i>
            <span>股票数据</span>
          </el-menu-item>
          <el-menu-item index="2">
            <i class="el-icon-s-operation"></i>
            <span>策略</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-s-operation"></i>
            <span>指标</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: '1' // 默认选中“股票数据”
    };
  },
 methods: {
    handleSelect(key) {
      if (key === '1') {
        this.$router.push({ name: 'stock-data' });
      } else if (key === '2') {
        this.$router.push({ name: 'home' });
      } else if (key === '3') {
        this.$router.push('/indicators');
      }
    }
  }
}
</script>

<style scoped>
.el-header {
  background-color: var(--el-color-primary-light-7);
}

.el-header,
.el-main {
  display: flex;
  justify-content: center;
  align-items: center;
}

.full-height {
  height: 100%; /* 确保高度为100% */
}

.full-width {
  width: 100%; /* 确保宽度为100% */
}

.el-menu {
  height: 100%;
}
</style>
