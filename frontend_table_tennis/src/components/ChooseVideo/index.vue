<template>
   <el-container class="choose-container">
      <el-header class="choose-header">
         <img
            class="icon-img"
            src="../../assets/pp-icon.jpg"
            alt=""
            @click="this.$router.push('/welcome')"
         />
         <p>乒乓球视频分析系统</p>
      </el-header>
      <el-main class="choose-main">
         <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/' }">首页 </el-breadcrumb-item>
            <el-breadcrumb-item>上传视频</el-breadcrumb-item>
         </el-breadcrumb>
         <el-card
            shadow="never"
            class="main-card"
            v-loading="!uploadSuccess"
            element-loading-text="上传视频中，请稍候..."
            element-loading-svg-view-box="-10, -10, 50, 50"
            element-loading-background="rgba(122, 122, 122, 0.8)"
         >
            <el-card class="video-choose-card">
               <el-row :gutter="20">
                  <el-col :span="12">
                     <div class="upload-context">
                        <div class="upload-info">
                           <p class="p-info">上传视频</p>
                           <p class="p-tip">请上传mp4文件</p>
                        </div>
                        <div class="upload-component-warpper">
                           <el-upload
                              :limit="1"
                              :on-exceed="handleExceed"
                              ref="uploadRef"
                              :auto-upload="false"
                              :http-request="upload"
                           >
                              <template #trigger>
                                 <el-button class="select-btn" type="primary"
                                    >选择文件</el-button
                                 >
                              </template>
                              <el-button
                                 class="ml-3 submit-btn"
                                 type="success"
                                 @click="submitUpload"
                              >
                                 上传至服务器
                              </el-button>

                              <!-- <template #tip v-if="show_tip">
                                 <div  class="el-upload__tip">请上传mp4文件</div>
                              </template> -->
                           </el-upload>
                        </div>
                     </div>
                  </el-col>
                  <el-col :span="12">
                     <div class="choose-context">
                        <p>预设视频:</p>
                        <div class="choose-btns">
                           <el-button
                              type="primary"
                              @click="show_video('video_1.mp4')"
                              >视频1</el-button
                           >
                           <el-button
                              type="primary"
                              @click="show_video('video_2.mp4')"
                              >视频2</el-button
                           >
                           <el-button
                              type="primary"
                              @click="show_video('video_3.mp4')"
                              >视频3</el-button
                           >
                           <el-button
                              type="primary"
                              @click="show_video('video_4.mp4')"
                              >视频4</el-button
                           >
                        </div>
                     </div>
                  </el-col>
               </el-row>
            </el-card>
            <el-card class="play-video">
               <el-row :gutter="20">
                  <el-col :span="24"></el-col>
                  <div class="info-warpper">
                     <p>视频预览</p>
                     <br />
                     <p>正在播放：</p>
                     <p>{{ video_name }}</p>
                     <br /><br /><br /><br /><br />
                     <el-button
                        type="primary"
                        @click="
                           this.$router.push(
                              `/show_demo?video=${next_page_video_name}`
                           )
                        "
                        >分析视频</el-button
                     >
                  </div>
                  <div class="player-warpper" v-if="hasUploadVideo">
                     <video-player
                        class="video-player vjs-custom-skin"
                        ref="videoPlayer"
                        :playsinline="true"
                        :options="playerOptions"
                     ></video-player>
                  </div>
               </el-row>
            </el-card>
         </el-card>
      </el-main>
   </el-container>
</template>

<script setup>
import { ref } from "vue";
import { genFileId } from "element-plus";
import { uploadVideo, init } from "./require.js";
// import {socket_UploadVideo} from './WSRequire.js'

import { onMounted, nextTick } from "vue";
import { VideoPlayer } from "@videojs-player/vue";
import "video.js/dist/video-js.css";

let uploadRef = ref();

let show_tip = ref(true);

let hasUploadVideo = ref(true);

let video_name = ref("");

let next_page_video_name = ref("");

let uploadSuccess = ref(true);

const playerOptions = ref({
   controls: true,
   autoplay: true, // 如果true,浏览器准备好时开始回放。
   muted: true, // 默认情况下将会消除任何音频。
   loop: false, // 导致视频一结束就重新开始。
   preload: "auto", // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
   language: "zh-CN",
   aspectRatio: "4:3", // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
   fluid: true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
   sources: [
      {
         src: "",
         type: "video/mp4",
      },
   ],
   width: document.documentElement.clientWidth,
   notSupportedMessage: "加载视频失败，请稍后再试", // 允许覆盖Video.js无法播放媒体源时显示的默认信息。
   controlBar: {
      timeDivider: true,
      durationDisplay: true,
      remainingTimeDisplay: false,
      fullscreenToggle: true, // 全屏按钮
   },
});

onMounted(async () => {
   await init();
   show_video("video_2.mp4");
});

function handleExceed(files) {
   uploadRef.value.clearFiles();
   const file = files[0];
   file.uid = genFileId();
   uploadRef.value.handleStart(file);
}

async function upload(params) {
   uploadSuccess.value = false;
   const file = params.file;
   // await socket_UploadVideo(file)
   await uploadVideo(file);

   show_video("user_video.mp4");

   nextTick(() => {
      next_page_video_name.value = "user_video.mp4";
      video_name.value = file.name;

      uploadRef.value.clearFiles();
      uploadSuccess.value = true;
   });
}

function submitUpload() {
   uploadRef.value.submit();
}

function show_video(video) {
   hasUploadVideo.value = false;
   const videoSrc = ``;
   nextTick(() => {
      const videoSrc = `/api/example_video/?video=${video}`;
      playerOptions.value.sources[0].src = videoSrc;
      hasUploadVideo.value = true;

      video_name.value = video;
      next_page_video_name.value = video;
   });
}
</script>

<style lang="less" scoped>
.choose-container {
   width: 100%;
   height: 100%;
   .choose-header {
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
   .choose-main {
      padding: 0;
      .el-breadcrumb {
         margin: 10px 0 10px 10px;
      }
      .main-card {
         height: 94%;
         --el-card-padding: 5px;
         .video-choose-card {
            width: 100%;
            height: 70px;
            --el-card-padding: 0px;
            margin: 0 0 10px 0;
            .upload-context {
               width: 100%;
               height: 70px;
               display: flex;
               align-items: center;
               .upload-info {
                  width: 120px;
                  height: 100%;
                  padding: 0 15px;
                  .p-info {
                     width: 120px;
                     height: 45px;
                     line-height: 45px;
                     text-align: center;
                     display: block;
                  }
                  .p-tip {
                     width: 120px;
                     height: 20px;
                     display: block;
                     font-size: 10px;
                     text-align: center;
                  }
               }

               .upload-component-warpper {
                  height: 70px;
                  width: 300px;
                  .select-btn {
                     margin: 5px 10px 0 0;
                  }
                  .submit-btn {
                  }
               }
            }
            .choose-context {
               width: 100%;
               height: 70px;
               display: flex;
               align-items: center;
               p {
                  display: block;
                  width: 130px;
                  height: 70px;

                  margin: 0 10px;

                  line-height: 70px;
               }
               .choose-btns {
                  width: 100%;
                  height: 70px;
                  display: flex;
                  align-items: center;
               }
            }
         }
         .play-video {
            height: 100%;
            --el-card-padding: 10px;
            .player-warpper {
               display: block;
               width: 850px;
               .video-player {
                  width: 100%;
               }
            }

            .info-warpper {
               margin: 10px 0 0 0;
               padding: 0 20px;
               width: 200px;
               .el-button {
                  margin: 0 0 0 30px;
               }
            }
         }
      }
   }
}
</style>