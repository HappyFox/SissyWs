/* global WebSocket */

export class BotProxy {
  constructor (onconnected = undefined, ondisconnected = undefined) {
    this.websocket = new WebSocket('ws://' + window.location.hostname + ':6789/')
  }

  setFace (face) {
    if (this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify({ action: 'face', face: face }))
    }
  }

  setLook (direction) {
    if (this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify({ action: 'look', face: direction }))
    }
  }

  clearLook () {
    if (this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(JSON.stringify({ action: 'clearLook' }))
    }
  }
}
