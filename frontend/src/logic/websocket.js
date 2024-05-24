import {logic} from './main.js';
import { io } from "socket.io-client";

let socket = null;


// export function connect(){
//     socket = io('http://localhost:3000/ws');
//     socket.on('connect', () => {
//         console.log('connected to server');
//     });
// }

export function emitEvent(event, data){
    socket.emit(event, data);
}

export function disconnect(){
    socket.disconnect();
    socket = null;
}