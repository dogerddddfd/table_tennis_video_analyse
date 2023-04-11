// import axios from "axios";


export async function run_demo() {
   const socket = new WebSocket('ws://127.0.0.1:8080/api/show_demo_ws/')

   socket.onopen = () => {
     console.log('sw open'); 
     let formData = {'message':'hello'}
     socket.send(JSON.stringify(formData))

   }

   socket.onerror = (e) => { console.log('sw error') }
   socket.onmessage = (e) => { console.log(e.data) }
   socket.onclose = (e) => { console.log('sw close') }
 
   return socket
 
}