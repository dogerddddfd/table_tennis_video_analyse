<template>
   <el-container class="show-demo-container">
      <el-header class="show-demo-header">
         <img
            class="icon-img"
            src="../../assets/pp-icon.jpg"
            alt=""
            @click="this.$router.push('/welcome')"
         />
         <p>乒乓球视频分析系统</p>
      </el-header>
      <el-main class="show-demo-main">
         <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/' }">首页 </el-breadcrumb-item>
            <el-breadcrumb-item :to="{ path: '/choose_video' }"
               >上传视频</el-breadcrumb-item
            >
            <el-breadcrumb-item>上传视频</el-breadcrumb-item>
         </el-breadcrumb>

         <el-card
            shadow="never"
            class="main-card"
            v-loading="!showImg"
            element-loading-text="启动中，请稍候..."
            element-loading-svg-view-box="-10, -10, 50, 50"
            element-loading-background="rgba(122, 122, 122, 0.8)"
         >
            <el-row :gutter="20">
               <el-col :span="24"></el-col>
               <div class="info-warpper">
                  <p>info</p>
                  <br />
                  <p>info</p>
                  <br /><br /><br /><br /><br />
                  <el-button v-if="!isStop" type="primary" @click="controlShow"
                     >暂停</el-button
                  >
                  <el-button v-else type="success" @click="controlShow"
                     >播放</el-button
                  >
               </div>
               <div class="img-warpper" v-if="showImg">
                  <img :src="imgSrc" />
                  <img src="api/show_demo/img" @click="controlShow" v-if="showImg" />
                  <!-- <img src="@/assets/pp-icon.jpg" @click="controlShow"/> -->
               </div>
            </el-row>
         </el-card>
      </el-main>
   </el-container>
</template>

<script setup>
import { init, run_demo, control_demo,show_demo_img } from "./require.js";
import { onUnmounted, onMounted, ref, nextTick } from "vue";
import { sleep } from "@antfu/utils";
import { useRoute } from "vue-router";

const route = useRoute();

let showImg = ref(false);
let imgSrc = ref('')

let isStop = ref(false);

var socket = null;

onMounted(async () => {
   await init();
   await run_demo(route.query.video);
   // imgSrc.value = show_demo_img()
   await sleep(1000);
   
   showImg.value = true;
});


// onMounted(async () => {
//    socket = new WebSocket('ws://127.0.0.1:8080/api/show_demo_ws/')

//    socket.onopen = () => {
//      console.log('sw open'); 
//      let formData = {
//       'flag':'START',
//       'filename':route.query.video
//    }
//      socket.send(JSON.stringify(formData))
//    }

//    socket.onerror = (e) => { console.log('sw error') }
//    socket.onmessage = (e) => { console.log(e.data) }
//    socket.onclose = (e) => { console.log('sw close') }

// });

async function controlShow() {
   await control_demo();
   isStop.value = !isStop.value;
}

onUnmounted(async () => {
   // socket.close()
   showImg.value = false;
});
</script>

<style lang="less" scoped>
.show-demo-container {
   width: 100%;
   height: 100%;
   .show-demo-header {
      height: 50px;
      background-color: #0093e9;
      background-image: linear-gradient(160deg, #0093e9 0%, #80d0c7 100%);
      display: flex;
      align-items: center;
      .icon-img {
         position: absolute;
         padding: 0 0 0 15px;
         width: 45px;
         height: 45px;
         border-radius: 50%;
         cursor: pointer;
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
   .show-demo-main {
      padding: 0;
      .el-breadcrumb {
         margin: 10px 0 10px 10px;
      }
      .main-card {
         height: 94%;
         margin: 10px 10px;
         --el-card-padding: 5px;
         .info-warpper {
            width: 180px;
            height: 300px;

            padding: 5px 20px;
         }
         .img-warpper {
            width: 1250px;
            height: 800px;
            position: relative;
            user-select: none;
            img {
               width: 100%;
               height: 100%;
               position: absolute;
               top: 50%;
               left: 50%;
               transform: translate(-50%, -50%);

               cursor: pointer;
            }
         }
      }
   }
}
</style>