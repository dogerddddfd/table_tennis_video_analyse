import axios from "axios";

export async function init(){
  const res = await axios.get('api/show_demo/init/')
  console.log(res)
  return res
}


export async function run_demo(filename){
  const res = await axios({
    method: 'get',
    url: `api/show_demo/run_demo`,
    params: {
      filename
    }
  })
  console.log(res)
  return res
}

export async function show_demo_img(){
  const url = null
  const res = axios({
    method: 'get',
    url: `api/show_demo/img`,
    responseType: 'blob',
  }).then(res=>{
    console.log(res)
    url = window.URL.createObjectURL(res.data)
  })
  console.log(url)
  return window.URL.createObjectURL(res.data)
}



export async function control_demo(){
  const res = await axios({
    url:'/api/show_demo/control',
    method:'get',
  })
}