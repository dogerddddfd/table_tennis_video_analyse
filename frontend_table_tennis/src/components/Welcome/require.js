import axios from "axios";

export async function ping() {
  const res = await axios.get('api/welcome/ping/').then(
    req=>{
      return req
    },
    res=>{
      return res
    }
  )
  return res
}

