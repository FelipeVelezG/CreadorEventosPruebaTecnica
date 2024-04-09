import datetime
import threading
import time
# Esta función se encarga de alertar al usuario sobre los eventos próximos( este fragmento es )
def alert_upcoming_events(user):#Funcion ejecutada en bucle infinito 
    while True:
        current_time = datetime.datetime.now()#obtener la hora actual 
        for event in user.events:# recorre todos los eventos del usuario 
            time_difference = (event.start_time - current_time).total_seconds()# Calcula la diferencia de tiempo entre la hora
            # de inicio del evento y la hora actual en segundos
            if 0 <= time_difference <= 3600:  
                print(f"Recordatorio: El evento '{event.name}' empieza en {time_difference // 60} minutos.")
        for event_id in user.shared_event_ids:#Recorre todos los IDs de eventos compartidos con el usuario.
            event = next((event for event in Event.events if event.event_id == event_id), None)#Busca el evento correspondiente al ID en la lista de todos los eventos.
            if event and event.start_time >= current_time:#Verifica si el evento existe y si su hora de inicio es en el futuro.
                #Verifica si el usuario tiene permiso para editar el evento.
                can_edit = "puede editar" if event.creator == self or event.shared_users_permissions.get(self, False) else "no puede editar"
                # Imprime los detalles del evento y si el usuario puede editarlo.
                print(f"- {event.name} ({event.start_time.strftime('%Y-%m-%d %H:%M')}), {can_edit}")
        time.sleep(60)  # Esperar un minuto antes de revisar de nuevo

# Clase para representar a un usuari
class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.events = []  # Lista para almacenar los eventos del usuario
        self.shared_event_ids = []  # Lista para almacenar los IDs de los eventos compartidos
    # Funcion para enumerar los eventos del usuario
    def list_events(self):
        # Obtiene la hora actual
        current_time = datetime.datetime.now()
        print("\nEventos del usuario:")
        # Recorre todos los eventos del usuario.
        for event in self.events:
            if event.start_time >= current_time:# Verifica si el evento está programado para comenzar en el futuro.
                print(f"- {event.name} ({event.start_time.strftime('%Y-%m-%d %H:%M')})")# imprime detalles del evento

        print("\nEventos compartidos:")
        # Recorre todos los IDs de eventos compartidos con el usuario.
        for event_id in self.shared_event_ids:
            # Busca el evento correspondiente al ID en la lista de todos los eventos.
            event = next((event for event in Event.events if event.event_id == event_id), None)
            #Verifica si el usuario tiene permisos para editar
            if event and event.start_time >= current_time:
                can_edit = "puede editar" if event.creator == self or event.shared_users_permissions.get(self, False) else "no puede editar"
                print(f"- {event.name} ({event.start_time.strftime('%Y-%m-%d %H:%M')}), {can_edit}")
    # Funcion para eliminar eventos
    def eliminar_evento(self):
        print("Eventos que puedes editar:")
        # Recorre eventos del usuario
        for event in self.events:
            # Imprime el ID y el nombre de cada evento del usuario.
            print(f"{event.event_id}: {event.name}")
            #Recorre todos los IDs de eventos compartidos con el usuario.
        for event_id in self.shared_event_ids:
            #Busca el evento correspondiente al ID en la lista de todos los eventos.
            event = next((event for event in Event.events if event.event_id == event_id), None)
            # Verifica si el evento existe y si el usuario tiene permiso para editarlo.
        if event and event.shared_users_permissions.get(self, False):
            # Imprime el ID y el nombre de cada evento compartido que el usuario puede editar.
            print(f"{event.event_id}: {event.name} (compartido)")
        evento_id = int(input("Por favor, ingresa el ID del evento que deseas eliminar: "))
        # Busca el evento con el ID proporcionado en la lista de eventos del usuario
        evento = next((evento for evento in self.events if evento.event_id == evento_id), None)
        # Si no se encuentra el evento en la lista de eventos del usuario, busca en la lista de todos los eventos.
        if evento is None:
            
            evento = next((evento for event in Event.events if event.event_id == evento_id and event.shared_users_permissions.get(self, False)), None)
        # Si se encuentra el evento, verifica si el usuario es el creador del evento o si tiene permiso para editarlo.
        if evento:
            if self == evento.creator or evento.shared_users_permissions.get(self, False):
                #Si el usuario tiene permiso para editar el evento, lo elimina de la lista de eventos.
                self.events.remove(evento)
                print(f"Evento '{evento.name}' eliminado exitosamente.")
            else:
                print("No tienes permiso para eliminar este evento.")
        else:
            print("No se encontró ningún evento con el ID proporcionado.")

# Clase para representar a un evento
class Event:
    id_counter = 0
    events = []  # Lista para almacenar todos los eventos
    # Constructor de eventos
    def __init__(self, name, description, start_time, duration, creator):
        Event.id_counter += 1
        self.event_id = Event.id_counter
        self.name = name
        self.description = description
        self.start_time = start_time
        self.duration = duration
        self.creator = creator
        self.shared_users = []# lista para almacenar usuarios a quienes se les comparte el evento
        self.shared_users_permissions = {}# diccionario clave los usuarios valor booleano referente al permiso de edición
        Event.events.append(self)# Almacena en lista de eventos  
    #Funcionan para compartir evento
    def share_event(self, user, can_edit):
        # Agregar usuario a la listade usuarios con los que se ha compartido el evento 
        self.shared_users.append(user)
        # Agrega el permiso al usuario 
        self.shared_users_permissions[user] = can_edit
        # Compartir el ID del evento en lugar del evento en sí
        user.shared_event_ids.append(self.event_id)  
    # Función para editar un evento
    def edit_event(self, user, new_name):
        # verificación si es creador o tiene permisos de edición 
        if user == self.creator or self.shared_users_permissions.get(user, False):
            self.name = new_name
        else: 
            print("No tienes permiso para editar este evento")
    
# Función para crear un evento
def create_event(creator, event_name, description, start_time, duration):
    event = Event(event_name, description, start_time, duration, creator)
    creator.events.append(event)
    return event
#Funcion principal 
def main():
    users = []  # Lista para almacenar objetos de usuario
 
    while True:
        print("\n1. Crear Usuario")
        print("2. Ingresar")
        print("3. Salir")
        choice = input("Ingrese su opción: ")
        # Crear un nuevo usuario
        if choice == "1":
            user_id = len(users) + 1
            name = input("Ingrese su nombre: ")
            password = input("Ingrese su contraseña: ")
            user = User(user_id, name, password)
            users.append(user)
            print(f"Usuario {name} creado exitosamente!")
        # Iniciar sesión
        elif choice == "2":
            name = input("Ingrese su nombre: ")
            password = input("Ingrese su contraseña: ")
            user_found = False
            for user in users:
                if user.name == name and user.password == password:
                    print(f"Bienvenido, {user.name}!")
                    threading.Thread(target=alert_upcoming_events, args=(user,)).start()
                    user_found = True
                    while True:
                        print("\n1. Crear Evento")
                        print("2. Listar Eventos")
                        print("3. Compartir evento")
                        print("4. Editar evento")
                        print("5. Eliminar evento")
                        print("6. Salir")
                        user_choice = input("Ingrese su opción: ")
                        
                        if user_choice == "1":
                            event_name = input("Ingrese el nombre del evento: ")
                            description = input("Ingrese la descripción del evento: ")
                            start_time_str = input("Ingrese la hora de inicio (formato: YYYY-MM-DD HH:MM): ")
                            duration = float(input("Ingrese la duración del evento (en horas): "))
                            start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                            event = create_event(user, event_name, description, start_time, duration)
                            print(f"Evento '{event_name}' creado exitosamente!")
 
                        elif user_choice == "2":
                            user.list_events()
 
                        elif user_choice == "3":
                            print("Eventos creados por ti:")
                            for event in user.events:
                                print(f"{event.event_id}: {event.name}")
 
                            selected_event_id = int(input("Ingrese el ID del evento que desea compartir: "))
                            selected_event = next((event for event in user.events if event.event_id == selected_event_id), None)
                            if selected_event:
                                print(f"Seleccionaste el evento: '{selected_event.name}' sera la fecha: { selected_event.start_time}")
                            else:
                                print("Evento no encontrado. Inténtalo nuevamente.")
 
                            print("Usuarios existentes:")
                            for other_user in users:
                                if other_user != user:
                                    print(f"{other_user.user_id}: {other_user.name}")
 
                            selected_user_id = int(input("Ingrese el ID del usuario al que desea compartir el evento: "))
                            selected_user = next((other_user for other_user in users if other_user.user_id == selected_user_id), None)
                            if selected_user:
                                print(f"Seleccionaste al usuario: {selected_user.name}")
                            else:
                                print("Usuario no encontrado. Inténtalo nuevamente.")
 
                            print("¿Quiere otorgar permiso de edición a este usuario?")
                            edit_selected_user = int(input("1.Si o 2.No"))
                             
                            if edit_selected_user == 1:
                                selected_event.share_event(selected_user, True)
                            else:
                                selected_event.share_event(selected_user, False)
                            print(f"Evento '{selected_event.name}' compartido exitosamente!")
 
                        elif user_choice == "4":
                            print("Eventos que puedes editar:")
                            for event in user.events:
                                print(f"{event.event_id}: {event.name}")
                            for event_id in user.shared_event_ids:
                                event = next((event for event in Event.events if event.event_id == event_id), None)
                                if event and event.shared_users_permissions.get(user, False):
                                    print(f"{event.event_id}: {event.name} (compartido)")

                            selected_event_id = int(input("Ingrese el ID del evento que desea editar: "))
                            selected_event = next((event for event in user.events if event.event_id == selected_event_id), None)
                            if selected_event is None:
                                selected_event = next((event for event in Event.events if event.event_id == selected_event_id and event.shared_users_permissions.get(user, False)), None)

                            if selected_event:
                                new_name = input("Ingrese el nuevo nombre del evento: ")
                                selected_event.edit_event(user, new_name)
                                print(f"Evento '{selected_event.name}' editado exitosamente!")
                            else:
                                print("Evento no encontrado o no tienes permisos para editarlo. Inténtalo nuevamente.")
                        elif user_choice == "5":  # Nueva opción para eliminar eventos
                            user.eliminar_evento()

                        elif user_choice == "6":
                            break
            if not user_found:
                print("Nombre de usuario o contraseña incorrectos. Inténtalo nuevamente")
                    
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
