/* global getComputedStyle */

import { ClickButton, HoldButton, RadioButtons } from './button.js'
import { BotProxy } from './bot_proxy.js'

let current = null
const faceElements = document.querySelectorAll('.face')
const lookButtons = document.querySelectorAll('.look-button')
const colorElements = document.querySelectorAll('.color')

const bot = new BotProxy()

const pressedColor = getComputedStyle(document.documentElement).getPropertyValue('--control-toggled')

function onColorSelect (target) {
  target.style.borderColor = pressedColor

  const colorStr = window.getComputedStyle(target, null).getPropertyValue('background-color')
  console.log("setting color : " + colorStr)
  const rgbStr = colorStr.slice(4, -1)
  const rgb = rgbStr.split(',').map(x => parseInt(x))

  bot.setColor(rgb[0], rgb[1], rgb[2])
}

function onColorDeSelect (target) {
  target.style.borderColor = null
}

const colorButtons = new RadioButtons(colorElements, onColorSelect, onColorDeSelect)

function onFaceSelect (target) {
  target.style.backgroundColor = pressedColor
  target.style.borderColor = pressedColor

  const face = target.textContent
  bot.setFace(face)
}

function onFaceDeSelect (target) {
  target.style.backgroundColor = null
  target.style.borderColor = null
}

const faceButtons = new RadioButtons(faceElements, onFaceSelect, onFaceDeSelect)

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

lookButtons.forEach(bindLookButtons)
