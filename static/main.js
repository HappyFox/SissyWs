/* global getComputedStyle */

// import { TouchManager } from './touch_manager.js'
import { ClickButton, HoldButton } from './button.js'
import { BotProxy } from './bot_proxy.js'

let current = null
const faceButtons = document.querySelectorAll('.face')
const lookButtons = document.querySelectorAll('.look-button')

// const websocket = new WebSocket('ws://' + window.location.hostname + ':6789/')

const bot = new BotProxy()

const pressedColor = getComputedStyle(document.documentElement).getPropertyValue('--control-toggled')

function handleFaceButton (event) {
  if (current !== null) {
    current.style.backgroundColor = null
  }

  const face = event.target.textContent

  bot.setFace(face)

  event.target.style.backgroundColor = pressedColor
  current = event.target
  console.log(face)
}

function startLook (event) {
  const target = event.target
  const direction = target.textContent

  console.log('Start looking : ' + direction)
  bot.setLook(direction)

  target.style.backgroundColor = pressedColor
}

function stopLook (event) {
  const target = event.target
  const direction = target.textContent

  console.log('Stop looking : ' + direction)
  bot.clearLook()

  target.style.backgroundColor = null
}

function bindLookButtons (button, idx, array) {
  new HoldButton(button, startLook, stopLook)
}

function bindFaceButtons (button, idx, array) {
  new ClickButton(button, handleFaceButton)
}

faceButtons.forEach(bindFaceButtons)
lookButtons.forEach(bindLookButtons)
