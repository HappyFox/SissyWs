/* global querySelectorAll WebSocket getComputedStyle */

// import { TouchManager } from './touch_manager.js'
import { Button } from './button.js'

let current = null
const faceButtons = document.querySelectorAll('.face')
const lookButtons = document.querySelectorAll('.look-button')
const websocket = new WebSocket('ws://' + window.location.hostname + ':6789/')
const pressedColor = getComputedStyle(document.documentElement).getPropertyValue('--control-toggled')

// const touchManager = new TouchManager()

function handleFaceButton (event) {
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

function stopLook (touch) {
  const target = touch.target
  const direction = target.textContent
  console.log('Stop looking : ' + direction)
  target.style.backgroundColor = null
}

function handleLookTouchStart (event) {
  console.log('TOUCH START!')
  console.log(event2.changedTouches[0].identifier)
  event.preventDefault()

  const target = event.target
  start_look(target)

  const touch = event.changedTouches[0]

  touchManager.register(touch.identifier, { onStop: stopLook })
  // function handle_stop (touch) {
  //  console.log(touch.identifier)
  //  stopLook(target)
  //  on_stop_handlers.delete(touch.identifier)
  // }

  // on_stop_handlers.set(event.changedTouches[0].identifier, handle_stop)
}

function handleLookTouchEnd (event) {
  console.log('TOUCH END!')
  console.log(event.changedTouches[0].identifier)
  event.preventDefault()
}

function bind_look_handers (button, idx, array) {
  console.log('binding ! : ' + button)
  button.addEventListener('touchstart', handleLookTouchStart, false)
  // button.onmousedown = handleLookTouchStart;

  // button.addEventListener("touchend", handleLookTouchEnd, false);
  // button.addEventListener("touchcancel", handleLookTouchEnd, false);
}

function bindButtons (button, idx, array) {
  var button_ = new Button(button, {}) 
}
faceButtons.forEach((element, _, __) => element.onclick = handleFaceButton)
//lookButtons.forEach(bind_look_handers)
lookButtons.forEach(bindButtons)
