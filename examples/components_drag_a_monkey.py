import pilas

mono = pilas.actors.Monkey()
mono.mixin(pilas.comportamientos.Draggable)

pilas.bucle()
