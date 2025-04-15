class Cart:

    def __init__(self,request): #se le entrega el request que viene de la peticion hacia mi servidor a esta clase
        self.request = request # se crea un objeto tipo request dentro de esta clase llamada Cart
        self.session = request.session # con el request.session se obtiene la sesion del navegador

        cart = self.session.get('cart') # el .get sirve para invocar una variable de sesion, si se crea una variable llamada nombre en la sesion, se puede invocar con el .get('nombre') y obtener su valor
        montoTotal = self.session.get('cartMontoTotal') # se obtiene el monto total de la sesion, si no existe se asigna un valor vacio
        if not cart: # si no existe la variable cart en la sesion, se crea una nueva, con un valor vacio en este caso un diccionario
            cart = self.session['cart'] = {} # se crea la variable cart en la sesion y se le asigna un diccionario vacio, para que se pueda usar como un carrito de compras, que esta alamacenado en la sesion, se llama con session.get('cart') 
            montoTotal = self.session['cartMontoTotal'] = 0 # se crea la variable montoTotal en la sesion y se le asigna un valor de 0, para que se pueda usar como un carrito de compras, que esta alamacenado en la sesion, se llama con session.get('montoTotal')      
        self.cart = cart
        self.montoTotal = float(montoTotal)

    def add(self, producto,cantidad): # se crea un metodo para agregar productos al carrito
        if str(producto.id) not in self.cart.keys():
            self.cart[producto.id] = {
                "producto_id": producto.id,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': str(producto.precio),
                "imagen": producto.imagen.url,
                "categoria": producto.categoria.nombre,
                'subtotal': str(cantidad * producto.precio),
            }
        else:
            # actializamos el producto en el carrito
            for key, value in self.cart.items():
                if key == str(producto.id):
                    value['cantidad'] = str(int(value['cantidad']) + int(cantidad)) # se convierte a entero para poder sumar
                    value['subtotal'] = str(float(value['cantidad']) * float(value['precio'])) # se convierte a float para poder multiplicar
                    break
        self.save()

    def delete(self, producto): # se crea un metodo para eliminar productos del carrito
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
        self.save()

    def clear(self): # se crea un metodo para limpiar el carrito
        self.session['cart'] = {} # se limpia la variable cart en la sesion
        self.session['cartMontoTotal'] = '0' # se limpia la variable montoTotal en la sesion

    def save(self):
        """ guarda cambios en el carrito de compras """

        montoTotal = 0
        for key, value in self.cart.items():
            montoTotal += float(value['subtotal'])

        self.session['cartMontoTotal'] = montoTotal
        self.session['cart'] = self.cart # se guarda el carrito en la sesion
        self.session.modified = True

