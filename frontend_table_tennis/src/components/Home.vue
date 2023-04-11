<template>
   <div class="common-layout">
      <div class="router-warpper">
         <router-view></router-view>
      </div>
   </div>
</template>

<script>
export default {};
</script>

<style lang="less" scoped>
.common-layout {
   width: 100%;
   height: 100%;
   .router-warpper {
      width: 100%;
      height: 100%;
   }
}
</style>