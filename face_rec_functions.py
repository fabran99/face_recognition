from os import listdir
from os.path import isfile, join, splitext
import face_recognition
from shutil import copyfile
import re


def img_filter(known_img_path, unknown_img_path, matches_path, change_label, difference=0.5):

    # expresion regular para filtrar las imagenes
    reg_extension = "\.jpg|\.png|\.jpeg|\.gif|\.JPG|\.PNG|\.JPEG|\.GIF$"
    print_txt = "Buscando rostros a identificar"
    change_label(print_txt)

    # tomo los archivos de la carpeta de identificados
    known_images = [f for f in listdir(known_img_path) if isfile(
        join(known_img_path, f)) and re.search(reg_extension, f)]

    if len(known_images) == 0:
        print_txt = "No se encontraron rostros en la carpeta de conocidos"
        change_label(print_txt)
        return None

    # creo un modelo por cada imagen y lo agrego a la lista
    known_models = []

    for image_name in known_images:
        # ruta completa de la imagen
        route = join(known_img_path, image_name)
        # agrego el modelo
        img_load = face_recognition.load_image_file(route)
        img_model = face_recognition.face_encodings(img_load)
        if img_model:
            for x in img_model:
                known_models.append(x)

    print_txt = "{} rostros identificados".format(len(known_models))
    change_label(print_txt)

    print_txt = "Buscando imagenes a identificar"
    change_label(print_txt)
    # tomo los archivos de la carpeta de no identificados
    unknown_images = [f for f in listdir(unknown_img_path) if isfile(
        join(unknown_img_path, f)) and re.search(reg_extension, f)]

    print_txt = "{} imagenes sin identificar".format(len(unknown_images))
    change_label(print_txt)

    found = 0
    # por cada imagen de la carpeta comparo todos los modelos
    # img_model es un array vacio en caso de que la imagen no tenga caras
    for numero, image_name in enumerate(unknown_images):
        # armo la ruta de la imagen
        print_txt = "Revisando imagen: {} de {}. {} encontrados".format(
            numero, len(unknown_images), found)
        change_label(print_txt)

        route = join(unknown_img_path, image_name)
        # creo el modelo de la imagen
        img_load = face_recognition.load_image_file(route)
        img_model = face_recognition.face_encodings(img_load)

        # si hay caras en la imagen, reviso si alguna es similar a la de los conocidos
        if len(img_model) > 0:
            # por cada cara encontrada
            for unknown_face in img_model:
                # comparo con las imagenes conocidas
                face_distances = face_recognition.face_distance(
                    known_models, unknown_face)
                # si la distancia entre la cara desconocida y la conocida es menor a 0.5 entonces la copio
                # cuanta menor sea la distancia mas parecido tienen
                for i, face_distance in enumerate(face_distances):
                    if face_distance < float(difference):
                        found += 1
                        dst_route = join(matches_path, image_name)
                        copyfile(route, dst_route)
                        break

    print_txt = "{} encontrados, finalizado con éxito".format(found)
    print(print_txt)

    change_label(print_txt)
