import axios from "axios";

export async function uploadVideo(file) {
  const fileChunks = createFileChunks(file)
  await uploadFileChunks(fileChunks, file.name)
  await mergeFileChunks(file.name);

}

// 创建切片
function createFileChunks(file, size = 1024 * 1024 * 50) {
  let fileChunks = [];
  for (let cur = 0; cur < file.size; cur += size) {
    fileChunks.push(file.slice(cur, cur + size));
  }
  console.log('length：' + fileChunks.length)
  return fileChunks;
}

// 上传切片
async function uploadFileChunks(fileChunks, filename) {
  const chunksList = fileChunks.map((chunk, index) => {
    let formData = new FormData();
    formData.append('filename', filename);
    formData.append('hash', index);
    formData.append('chunk', chunk);
    return {
      formData
    };
  });

  const uploadList = chunksList.map(async ({ formData }) => {
    const res = await axios({
      method: 'post',
      url: 'api/upload_video/upload/',
      data: formData
    })
    // console.log(res)
  });

  await Promise.all(uploadList);
}



// 合并切片
const mergeFileChunks = async function (filename) {
  const res = await axios({
    method: 'get',
    url: 'api/upload_video/merge/',
    // params: {
    //   filename
    // }
  });
  // console.log(res)
}


export async function init(){
    const res = await axios.get('api/upload_video/init')
}