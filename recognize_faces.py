from os import listdir
from os.path import isfile, join, splitext
import face_recognition
from shutil import copyfile

# tomo los archivos de la carpeta de identificados
known_img_path = "./img/known"
known_files = [f for f in listdir(known_img_path) if isfile(join(known_img_path, f)) ]

#filtro las imagenes
ext = [".jpg",".png",".jpeg",".gif"]
known_images=[]

for x in known_files:
    for y in ext:
        if y in x:
            known_images.append(x)


# creo un modelo por cada imagen y lo agrego al diccionario
models=[]

for image_name in known_images:
    model={}
    #ruta completa de la imagen 
    route=join(known_img_path, image_name)
    model["route"]=route
    # armo el modelo de la persona
    img_load=face_recognition.load_image_file(route)
    img_model=face_recognition.face_encodings(img_load)[0]
    model["model"]=img_model
    model["name"]=splitext(image_name)[0]
    models.append(model)

# tomo los archivos de la carpeta de no identificados
unknown_img_path = "./img/unknown"
unknown_files = [f for f in listdir(unknown_img_path) if isfile(join(unknown_img_path, f)) ]

# filtro las imagenes
unknown_images=[]

for x in unknown_files:
    for y in ext:
        if y in x:
            unknown_images.append(x)
            break

# por cada imagen de la carpeta comparo todos los modelos
# img_model es un array vacio en caso de que la imagen no tenga caras
matches = {}
for model in models:
    matches[model["name"]]=0

for image_name in unknown_images:
    # armo la ruta de la imagen
    route = join(unknown_img_path, image_name)
    # creo el modelo de la imagen
    img_load=face_recognition.load_image_file(route)
    img_model=face_recognition.face_encodings(img_load)

    # si hay caras en la imagen, reviso si alguna es similar a la de los conocidos
    if len(img_model) > 0:
        # por cada cara encontrada 
        for unknown_face in img_model:
            # por cada persona conocida
            for model in models:
                results = face_recognition.compare_faces([model["model"]], unknown_face)
                # si hacen match copio a la carpeta
                if results[0]:
                    matches[model["name"]]+=1
                    dst_route="./img/resultados/"+image_name
                    copyfile(route, dst_route)
                    break

# muestro la cantidad de cada uno
print(matches)

