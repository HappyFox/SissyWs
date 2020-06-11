/* global querySelectorAll WebSocket getComputedStyle */

import { TouchManager } from './touch_manager.js'

let current = null
const faceButtons = document.querySelectorAll('.face')
const lookButtons = document.querySelectorAll('.look-button')
const websocket = new WebSocket('ws://' + window.location.hostname + ':6789/')
const pressedColor = getComputedStyle(document.documentElement).getPropertyValue('--control-toggled')

const touchManager = new TouchManager()

/*
const on_move_handlers = new Map()
const on_stop_handlers = new Map()

function on_touch (event) {
  const touches = event.changedTouches

  console.log(event.type)

  let handlers = null
  if (event.type === 'touchend') {
    event.preventDefault()
    handlers = on_stop_handlers
  } else if (event.type === 'touchmove') {
    handlers = on_move_handlers
  } else {
    console.log('returning!')
    return
  }

  for (let idx = 0; idx < touches.length; idx++) {
    const touch = touches[idx]
    if (handlers.has(touch.identifier)) {
      handlers.get(touch.identifier)(touch)
    }
  }
}

document.addEventListener('touchmove', on_touch, false)
document.addEventListener('touchend', on_touch, false)
*/

function handle_face_btn (event) {
  if (current !== null) {
    current.style.backgroundColor = null
  }

  const face = event.target.textContent
  websocket.send(JSON.stringify({ action: 'face', face: face }))

  event.target.style.backgroundColor = pressedColor
  current = event.target
  console.log(face)
}

function start_look (target) {
  const direction = target.textContent
  console.log('Start looking : ' + direction)
  target.style.backgroundColor = pressedColor
}

function stop_look (target) {
  const direction = target.textContent
  console.log('Stop looking : ' + direction)
  target.style.backgroundColor = null
}


function handle_look_touch_start (event) {
  console.log('TOUCH START!')
  console.log(event.changedTouches[0].identifier)
  event.preventDefault()

  const target = event.target
  start_look(target)
  
  const touch = event.changedTouches[0]

  touchManager.register(touch.identifier, { onStop:stop_look })
  //function handle_stop (touch) {
  //  console.log(touch.identifier)
  //  stop_look(target)
  //  on_stop_handlers.delete(touch.identifier)
  //}

  //on_stop_handlers.set(event.changedTouches[0].identifier, handle_stop)
}

function handle_look_touch_end (event) {
  console.log('TOUCH END!')
  console.log(event.changedTouches[0].identifier)
  event.preventDefault()
}

function bind_look_handers (button) {
  console.log('binding ! : ' + button)
  button.addEventListener('touchstart', handle_look_touch_start, false)
  // button.onmousedown = handle_look_touch_start;

  // button.addEventListener("touchend", handle_look_touch_end, false);
  // button.addEventListener("touchcancel", handle_look_touch_end, false);
}
faceButtons.forEach((element) => element.onclick = handle_face_btn)
lookButtons.forEach((element) => bind_look_handers(element))
