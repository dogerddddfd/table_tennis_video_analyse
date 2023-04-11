import axios from "axios";

let socket = null

export function socket_UploadVideo(file) {
   return new Promise((resolve, reject) => {
      socket = new WebSocket('ws://127.0.0.1:8080/api/WS_upload_video')

      let upload_file = async function (file) {
         const fileChunks = createFileChunks(file)
         await uploadFileChunks(fileChunks, file.name)
      }

      socket.onopen = () => {
         console.log('sw open');
         upload_file(file)
      }

      socket.onmessage = async (e) => {
         let respose = JSON.parse(e.data)
         console.log(respose);
      }

      socket.onerror = (e) => { console.log('sw error') }

      socket.onclose = (e) => {
         console.log('sw close')
         resolve()
      }

   })
}





// 创建切片
function createFileChunks(file, size = 1024 * 1024 * 15) {
   console.log('createFileChunks')
   let fileChunks = [];
   for (let cur = 0; cur < file.size; cur += size) {
      fileChunks.push(file.slice(cur, cur + size));
   }
   console.log('length：' + fileChunks.length)
   return fileChunks;
}


// 上传切片
async function uploadFileChunks(fileChunks) {
   fileChunks.map((chunk, index) => {
      const reader = new FileReader();
      reader.onload = (e) => {
         let buffer = e.target.result;
         let data = JSON.stringify({
            hash: index,
            length: fileChunks.length
         })
         console.log(data)
         socket.send(data)
         socket.send(buffer);
      }
      reader.readAsArrayBuffer(chunk);
   });

}



// // 合并切片
// const mergeFileChunks = async function (filename) {
//    const res = await axios({
//       method: 'get',
//       url: '/api/upload_video/merge/',
//       params: {
//          filename
//       }
//    });
//    console.log(res)
// }

async function mergeFileChunks(filename) {
   let formData = {
      flag: 'MERGE'
   }
   console.log('mergeFileChunks')
   socket.send(JSON.stringify(formData))
}