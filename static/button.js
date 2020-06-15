
export class Button {
  constructor (element, {onDown = undefined, onUp = undefined, onMove = undefined } ) {
    this.element = element
    
    this.onDown = onDown
    this.onUp = onUp
    this.onMove = onMove

    this.upHandler = undefined
    this.moveHandler = undefined
    
    this.element.addEventListener('pointerdown', (event) => this.onPointerDown(event), false)
  }

  onPointerDown (event) {
    console.log("DOWN") 
    this.upHandler = (event) => this.onPointerUp(event)
    this.moveHandler = (event) => this.onPointerMove(event)

    this.element.addEventListener('pointerup', this.upHandler , false)
    this.element.addEventListener('pointercancel', this.upHandler, false)
    this.element.addEventListener('pointermove', this.moveHandler , false)
  }

  onPointerUp (event) {
    console.log("UP!!!")
    this.element.removeEventListener('pointerup', this.upHandler, false)
    this.element.removeEventListener('pointercancel', this.upHandler, false)

    this.upHandler = undefined

    this.element.removeEventListener('pointermove', this.moveHandler, false)
    this.moveHandler = undefined
  }

  onPointerMove (event) {
    console.log("MOVE!!!")
  }
}
