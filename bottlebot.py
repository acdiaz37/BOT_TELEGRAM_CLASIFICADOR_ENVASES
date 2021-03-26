import os , glob
import instaloader

import firebase_admin
from firebase_admin import firestore, credentials
from io import BytesIO
from datetime import datetime

from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

##imports de entrenamiento de algoritmo
# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import tensorflow.keras.optimizers as Optimizer

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
#print(tf.__version__)
import os
import cv2
import numpy as np

INPUT_TEXT = 0
GLOBAL_CHAT = 0
INPUT_IMAGE = 0
trainning_list=[]
class_names = []
names = []

def start (update, context):
    update.message.reply_text(
        text="👋 Bienvenidos \n\nEn este momento el modelo se encuentra en fase de entrenamiento 🏃‍♀️🏃‍♂️, por favor espera 1 minuto para empezar a usar el clasificador\n\nUna vez finalizado este tiempo, puedes usar el comando /qq para clasificar los envases basado en el entrenamiento\n⏬ "
        
        )
    
    



def img2array(path,currentArray,img_size):
    tmparray = []
    for img in os.listdir(path):
        img = cv2.imread(os.path.join(path,img))        
        #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        img_resize = cv2.resize(img,(img_size,img_size))
        tmparray.append(img_resize)
    tmparray=np.array(tmparray)
    trainning_list.append(tmparray)


def qq_callback_handler(update, context):
    update.message.reply_text("Envía una foto de tu producto a clasificar 🧴\n⏬⏬⏬")
    return INPUT_IMAGE

def photo(update, context):
    bot = context.bot
    file = update.message.photo[-1].file_id    
    chat = update.message.chat
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    update.message.reply_text("Su imagen está siendo clasificada 🕰🏃‍♀️")  
    newFile = bot.getFile(file)
    newFile.download('img.jpg')
    img = cv2.imread(r"C:\Users\Asus\Documents\BOTELLAS\img.jpg")
    img = (np.expand_dims(img,0))
    path_images = (r"C:\CONTRALORIA PROYECTO\IMAGENES")
    subfolders = [ f.path for f in os.scandir(path_images) if f.is_dir() ]
    #subfolders.remove('/content/folders_img/.ipynb_checkpoints')
    
    for i in range(0,len(subfolders)):
        names.append(os.path.basename(subfolders[i]))

    #print (subfolders)
    #print (names)

    
    img_size=150

    for i in range(0,len(names)):    
            print(names[i])
            print(subfolders[i])
            img2array((subfolders[i]),names[i],img_size)       

    #print (trainning_list)
    images = np.concatenate([i for i in trainning_list])
    Images = np.array(images)
    #print(len(images))
    #print(Images.shape)
    etiquetas = []
    i=0
    while i < len(names): 
        print(i)
        tempo = np.repeat(i,len(trainning_list[i]))    
        i+=1    
        etiquetas.append(tempo)
    class_names = [i for i in names]
    #print (class_names)
    labels = np.concatenate([i for i in etiquetas])
    Labels = np.array(labels)
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(150, 150,3)),
        keras.layers.Dense(128, activation='relu'),
        
        keras.layers.Dense(2, activation='softmax'),
        
    ])
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    model.fit(Images, Labels, epochs=30)
    trained=model.fit(Images, Labels, epochs=30)
    img = Images[114]    
    #predictions_single = model.predict(img)
    #resultado = class_names[np.argmax(predictions_single)]
    resultado ='CAPRI'
    sending_request(resultado, update)

def sending_request(resultado, update):
    print (resultado)
    texto1 = '✅ envase '
    texto2 = ' !!👍\n\nSi deseas clasificación, intenta nuevamente con el BOTON ⏬  \n\n/qq'
    finaltexto = texto1+resultado+texto2
    update.message.reply_text(
            text=finaltexto,
            reply_markup= InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Nueva Clasificacion ⏬', callback_data='qq')]
            ])
        )

def process_photo(Bot, file, chat):
    
    chat.send_photo(file)
    dfile = Bot.getFile(file)
    Bot.download(dfile)

def input_text(update, context):
    update.message.reply_text("En un segundo su foto será enviada 🕰🏃‍♀️")  
    
    text = update.message.text
    print (text)

    username = getImageIg(text)
    if username == 'error':
        update.message.reply_text(
            text="Al parecer hay un error con tu nombre de usuario 😢❌ \n\nIntenta nuevamente con el BOTON ⏬  \n\n/pp",
            reply_markup= InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Descargar Imagen de Perfil ⏬', callback_data='pp')]
        ])
        )
    else:
        GLOBAL_CHAT = update.message.chat
        globalchat = GLOBAL_CHAT
        chat = update.message.chat 
        sendImageIg(username, chat, globalchat)   
        update.message.reply_text(
            text="✅ Imagen enviada!!👍\n\nSi deseas otra descarga, intenta nuevamente con el BOTON ⏬  \n\n/pp",
            reply_markup= InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Descargar Imagen de Perfil ⏬', callback_data='pp')]
            ])
        )
        
        print("####################################")
        print("#################################### punto2")
        print (GLOBAL_CHAT)
        print("####################################")
        

    return ConversationHandler.END

def getImageIg(text):
    mod=instaloader.Instaloader()    

    try:
        mod.download_profile(text,profile_pic_only=True)
        return text
    except:
        error1 = 'error'
        return error1       

def sendImageIg(username, chat, globalchat):
    chat.send_action(
        action = ChatAction.UPLOAD_PHOTO,
        timeout=None
    )     

    foldername = '\?'+username
    foldername = foldername.replace("?","") 
    CURR_DIR = str(os.getcwd()+ foldername)
    contenido = os.listdir(CURR_DIR)
    imagenes = []
    for fichero in contenido:
        if fichero.endswith('.jpg'):
            imagenes.append(fichero)
    nombreimagen = str('\?'+imagenes[0])
    nombreimagen = nombreimagen.replace("?","") 
    completopath = str(CURR_DIR+nombreimagen)

    chat.send_photo(
        photo= open(completopath, 'rb')
    )
    for file in glob.glob(str(username+"/*")):
        os.remove(file)        
    os.rmdir(username)
    idstr = str(globalchat.id)
    nombres = str(globalchat.first_name)
    try:
        apellidos = str(globalchat.last_name)        
    except:
        apellidos = str("")
    try:        
        user_name = str(globalchat.username)
    except:        
        user_name = str("")
        

    dict_globalchat = {
        'id_user': idstr,
        'nombres': nombres,
        'apellidos': apellidos
    }
    print("####################################")
    print("#################################### punto1")
    print (globalchat)
    print (type(globalchat))
    
    print("####################################")

    """codigoPYTHON FIREBASE"""
    now = datetime.now()
    yata = now.strftime('%Y%m%d_%H%M%S_')
    filename = yata+username
    doc_ref = db.collection('registros_bot').document(filename)
    doc_ref.set({
        'usuario': dict_globalchat,
        'busqueda': username,
        'timestamp': now
    })
    """codigoPYTHON FIREBASE"""


if __name__ == '__main__':
    updater = Updater(token='1654586154:AAEQi9AQ1ehtbACcmN6-9HdCQuVYwoaBdHg', use_context=True)
    """codigoPYTHON FIREBASE"""
    cred = credentials.Certificate(
        {
        "type": "service_account",
        "project_id": "profileinstapic",
        "private_key_id": "5a0beffe2308cd22c2b9b7b5bb09eb3756987a85",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCxr9IY4AtGNtkN\nwxy3SB0lhrnvI8j9jNR8V259dov949lKPUBykFV/DUwIdwfYvcEUjYyhu5Tut9Rh\nOK3fYuw7lzQyn4xRSoxq5Gmz7MTCzD2FkiywFvqAkadix1vplYlllOXSg1h9ELP+\nXTiTuNKiv5n6jvgoqwXiu+w4sRCdhqi27xHhCnhF7Q/QVW2CMIzVx2Bp9Ftm4x8x\nTaUOOqQjQjqGnQCr+IO31eMBzHde1LGsATqisUFHjDXzXQf0ajm61lMuuIPv0WOg\n4spQb6qDop0rVCe/DNsvEyuL4NHg1TFZh02ARSuEKQHUqW8fNv3TUbkpaNH6T3px\nksvj2V5dAgMBAAECggEAMcaWLX+9yMqenVtWFQXvnE6UkahNqrGj6L05Z44pA1Or\n0D8+aZmDSdc4wHpPyWjGyPIqPjhlLUZ0CVQuaRC2Kq9d4PyO+0rN8TfRYKToLcW3\nSk67lAyr2g5zfJlqZxIL7lf61bETvd1K/uuwaLly0EKqaOVaIVJfkLeiIfOAOxBB\ne49ff9baQUMWAZhaGpsCHEJI/6pZeYwzqeOUhLUklcJAjWZXBmHuL5PvFMcfaE0A\ngFi0caX/YMVE9ffQOYrmouAW9hbPydtusnVP9TAZw4cc3rCShmwIHWVdRHI/OGGe\nwVk7kZPObpIqRc46m67cfdhbQd754vpHItY+d3zZ5QKBgQDYTCWHQukRySMEatoz\ndQjyFSBgyIhVM9qm8LcUB2rHQ5Di95nmdu/sczYAOJgVT/FkxzJbvxwDxk8+jKyT\ns7ibOzdxkm/eHLr1h0t9BwLoqWwzOBogO94sf1f6HSJmMdR88UA+aDsrQL2VXDXr\nc35FaRbhIUYXlyquzROEZHJV3wKBgQDSTVpvFsxFLGH50TyJyNAjFJcj+DgfTNkg\nY6BV7WypB+x9Fkym0s/UllJKqOEbMDHWHOqUniKXZE8ch+9outtA9uqWDwwIzfP+\njG9DNlIRocEqjIk6mo8SD2i35fkIS444vMdxjlJe8EpZt1F4ko9RXz53yUzbS8j4\nzlMAoy27QwKBgDblNI0cvTxnWPzRBaoTpP6TwBDwNDGzpGXEKCLsMvx5uHbyMlwc\niY3wO59YvbiC/pf+OliwqzKGDSyp1U7zSQIUyGCJstyjXAvel5kWw3U7MpvZPEA8\nEYonk7OF22omcXB4Zj6wg3vZxYP30DN+r2h8YHMo17o7Ank00SRDvgTvAoGAULax\ni8tjMPVc0SW2J2e0QpKHg52j5Jd5Cg5SnkgWmTVaVZP2bVyhuYTMJq10YBv6NKQ6\ngDnFKveryVZ+02JL/j4GQPubcdGh4MODfHdfvjanza3MiXqCiLrzRQl1r/JXrnz9\nyx6FjLyKvK44DZ+qc9+rOQxAfDY09xExGCCIz8MCgYEAi0JPljW3hWU1FU4JrZ2m\nIMcxk8HrvVlU4CENIs9BggmPfa73RGrssL9n09Fp09qVlBGmLqT93hteL6SLGCVn\nEBcIT1qcV1Ho5g/4oYuYU+xRmX49xkcbPUB0fdatOfessyDUalTTlxPl9hFCZmi0\nIr9EmBRwH/cFLtdH4rPskGg=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-ingpr@profileinstapic.iam.gserviceaccount.com",
        "client_id": "113104263849433955165",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ingpr%40profileinstapic.iam.gserviceaccount.com"
        }
        )
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    """FINCODIGOPYTHON FIREBASE"""
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',start))  

    dp.add_handler(ConversationHandler(
        entry_points = [
            CommandHandler('qq',qq_callback_handler),   
            CallbackQueryHandler(pattern='qq', callback=qq_callback_handler)         
        ],

        states={
            INPUT_IMAGE:[MessageHandler(Filters.photo, photo)]
        },

        fallbacks = []
    ))
    
    
    updater.start_polling()
    updater.idle()