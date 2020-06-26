/* global getComputedStyle */

import { ClickButton, HoldButton, RadioButtons } from './button.js'
import { BotProxy } from './bot_proxy.js'

let current = null
const faceButtons = document.querySelectorAll('.face')
const lookButtons = document.querySelectorAll('.look-button')
const colorElements = document.querySelectorAll('.color')

const bot = new BotProxy()

const pressedColor = getComputedStyle(document.documentElement).getPropertyValue('--control-toggled')

function onColorSelect (target) {
  target.style.borderColor = pressedColor
}

function onColorDeSelect (target) {
  target.style.borderColor = null
}

const colorButtons = new RadioButtons(colorElements, onColorSelect, onColorDeSelect)

function handleFaceButton (event) {
  if (current !== null) {
    current.style.backgroundColor = null
    current.style.borderColor = null
  }

  const face = event.target.textContent

  bot.setFace(face)

  event.target.style.backgroundColor = pressedColor
  event.target.style.borderColor = pressedColor
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
