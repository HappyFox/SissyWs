
export class TouchManager {
  constructor () {
    this.onMoveHandlers = new Map()
    this.onStopHandlers = new Map()

    document.addEventListener('touchmove', (event) => this.onMove(event), false)
    document.addEventListener('touchend', (event) => this.onEnd(event), false)
    document.addEventListener('touchcancel', (event) => this.onEnd(event), false)
  }

  onMove (event) {
    const touches = event.changedTouches

    for (let idx = 0; idx < touches.length; idx++) {
      const touch = touches[idx]
      if (this.onMoveHandlers.has(touch.identifier)) {
        this.onMoveHandlers.get(touch.identifier)(touch)
      }
    }
  }

  onEnd (event) {
    const touches = event.changedTouches

    for (let idx = 0; idx < touches.length; idx++) {
      const touch = touches[idx]
      const identifier = touch.identifier
      if (this.onStopHandlers.has(identifier)) {
        this.onStopHandlers.get(identifier)(touch)
      }
      this.delist(identifier)
    }
  }

  register (identifier, { onStop = undefined, onMove = undefined }) {
    if (typeof onStop === 'function') {
      this.onStopHandlers.set(identifier, onStop)
    }
    if (typeof onMove === 'function') {
      this.onMoveHandlers.set(identifier, onMove)
    }
  }

  delist (identifier) {
    if (this.onMoveHandlers.has(identifier)) {
      this.onMoveHandlers.delete(identifier)
    }

    if (this.onStopHandlers.has(identifier)) {
      this.onStopHandlers.delete(identifier)
    }
  }
}
