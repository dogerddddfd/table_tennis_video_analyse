<template>
   <el-container class="home-container">
      <img
         class="background-img"
         src="https://img.mp.itc.cn/upload/20161107/666cf760b12e41d09ae816e23dce0fd5_th.jpeg"
         alt=""
      />
      <el-header class="home-header">
         <div class="header-context">
            <img class="icon-img" src="../../assets/pp-icon.jpg" alt="" />
            <p>乒乓球视频分析系统</p>
         </div>
      </el-header>
      <el-main class="home-main">
         <div class="main-context" v-loading="!pingSuccess">
            <div class="introduction-text">
               <p>介绍标题</p>
               <span
                  >介绍文案: Lorem ipsum, dolor sit amet consectetur adipisicing
                  elit. Illum iusto qui, dolorum harum necessitatibus fugiat
                  maxime dicta praesentium quam nostrum facilis magnam voluptate
                  quod velit nam. Quos, ratione. Similique, incidunt!
               </span>
            </div>
            <div
               class="confirm-btn"
               @click="
                  () => {
                     this.$router.push('/choose_video');
                  }
               "
            >
               进入系统
            </div>
         </div>
      </el-main>
   </el-container>
</template>

<script setup>
import { ping } from "./require.js";
// import { socket_ping } from "./WSRequire.js";
import { onMounted, ref } from "vue";

let pingSuccess = ref(true);

onMounted(async () => {
   await ping()
   const res = await ping();
   // await socket_ping()
   // console.log(res)
   if (res.status >= 200 && res.status < 300) {
      pingSuccess.value = true;
   } else {
      ElMessageBox.confirm("无法连接至服务器，请稍后再尝试！", "连接失败", {
         confirmButtonText: "刷新",
         cancelButtonText: "返回",
         type: "error",
      })
         .then(() => {
            location.reload();
         })
         .catch(() => {});
   }
});
</script>

<style lang="less" scoped>
.home-container {
   width: 100%;
   height: 100%;
   z-index: -1;
   .background-img {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: -999;
      filter: blur(5px);
   }
   .home-header {
      padding: 0;
      height: 70px;
      z-index: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      .header-context {
         width: 30%;
         height: 70%;

         background-color: rgba(248, 248, 248, 0.5);
         border-radius: 10px;

         display: flex;
         align-items: center;
         .icon-img {
            position: absolute;
            padding: 0 0 0 15px;
            width: 45px;
            height: 45px;
            border-radius: 50%;
         }
         p {
            display: block;
            // text-align: center;
            margin: 0 auto;
            line-height: 50px;
            font-size: 18px;
            font-weight: 800;
            font: sans-serif;
         }
      }
   }
   .home-main {
      padding: 0;
      width: 100%;
      height: 100%;

      display: flex;
      justify-content: center;
      align-items: center;
      .main-context {
         width: 500px;
         height: 500px;

         background-color: rgba(255, 255, 255, 0.4);
         border-radius: 20px;

         display: flex;
         justify-content: space-evenly;
         align-items: center;
         flex-direction: column;
         .introduction-text {
            width: 85%;
            height: 65%;
            background-color: rgba(255, 255, 255, 0.4);
            border-radius: 20px;
            padding: 10px;
            p {
               line-height: 50px;
               text-align: center;
            }
            span{

            }
         }
         .confirm-btn {
            background-color: rgba(88, 169, 255, 0.65);
            width: 130px;
            height: 50px;

            border-radius: 20px;
            cursor: pointer;

            line-height: 50px;
            text-align: center;
         }
      }
   }
}
</style>